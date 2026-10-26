"""Normaliza la extracción cruda (grid.py / HTML) a una malla oficial estructurada.

Uso: python3 oficial.py <raw.json|.htm> <malla_actual.json> <salida.json>
La malla actual se usa como diccionario para corregir errores de OCR en códigos.
"""
import json, re, sys, unicodedata, html as htmllib

def norm_txt(s):
    s = unicodedata.normalize("NFD", s or "")
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Z0-9 ]", "", s.upper()).strip()

def lev(a, b):
    if a == b: return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

DIG = str.maketrans({"O": "0", "o": "0", "Q": "0", "D": "0", "I": "1", "l": "1", "i": "1", "|": "1", "J": "1", "S": "5", "Z": "2", "B": "8", "G": "6", "T": "7"})

L2D = str.maketrans({"O": "0", "Q": "0", "D": "0", "I": "1", "L": "1", "J": "1", "S": "5", "Z": "2", "B": "8", "G": "6", "T": "7"})
D2L = str.maketrans({"0": "O", "1": "I", "5": "S", "8": "B", "6": "G", "2": "Z", "7": "T"})
PREFIJOS = set()

BIEN = re.compile(r"^[A-Z]{2,6}(?:[A-Z]{1,2}|P)?\d{2,4}[A-Z]?$")

def fix_code(raw, dic, malla=None):
    """Corrige un código leído por OCR.
    1) exacto en el diccionario; 2) traducción de confusiones típicas (O/0, I/1, S/5…) que cae en el diccionario;
    3) si la traducción da un código bien formado, se acepta tal cual (puede ser un código que no está en la malla actual);
    4) solo si está mal formado se aproxima a un código de la malla (distancia 1)."""
    s = re.sub(r"[^A-Za-z0-9]", "", raw or "").upper()
    if not s: return None, "vacio"
    if s in dic: return s, "ok"
    if not PREFIJOS:
        for d in dic:
            m = re.match(r"^([A-Z]+)", d)
            if m: PREFIJOS.add(m.group(1))
    cands = []
    for k in range(2, min(7, len(s) - 1)):
        pre, num = s[:k].translate(D2L), s[k:]
        m = re.fullmatch(r"([A-Z]{0,2}|P)([0-9A-Z]{2,4})([A-Z]?)", num)
        if not m: continue
        mid, dig, suf = m.groups()
        digt = dig.translate(L2D)
        if not digt.isdigit(): continue
        c = pre + mid + digt + suf
        if c in dic: return c, "corregido"
        if BIEN.match(c): cands.append((pre in PREFIJOS, len(pre), c))
    def mismo_numero(c):
        """Código bien formado pero desconocido: si difiere en una letra de un código de la malla con el mismo número, es ese."""
        if not malla: return None
        m = re.match(r"^([A-Z]+)(.*)$", c)
        if not m: return None
        hits = [d for d in malla if d.endswith(m.group(2)) and lev(re.match(r"^([A-Z]+)", d).group(1), m.group(1)) <= 1]
        return hits[0] if len(hits) == 1 else None
    if BIEN.match(s):
        h = mismo_numero(s)
        return (h, "aproximado") if h else (s, "nuevo")
    if cands:
        cands.sort(key=lambda x: (not x[0], -x[1]))
        h = mismo_numero(cands[0][2])
        return (h, "aproximado") if h else (cands[0][2], "nuevo")
    pool = malla if malla else dic
    best = sorted((lev(s, d), d) for d in pool if abs(len(d) - len(s)) <= 1)
    if best and best[0][0] <= 1 and (len(best) == 1 or best[1][0] > best[0][0]):
        return best[0][1], "aproximado"
    return s, "desconocido"

# ───────────── requisitos: texto → árbol ─────────────

TOKEN = re.compile(r"\(|\)|\b[oyOY]\b|[A-Z]{2,6}\s?(?:[A-Z]{1,2}|P)?\s?[0-9OIlSZ]{2,4}[A-Z]?\b")

def limpiar_req(lines):
    t = " ".join(lines)
    t = re.sub(r"[|\[\]{}_~'`\";:!¡,.*«»“”‘’°]", " ", t)
    t = re.sub(r"(?<![A-Za-z])[0](?=\s*\()", " o ", t)        # "0 (" → "o ("
    t = re.sub(r"(?<![A-Za-z0-9])0(?=\s+[A-Z]{2,})", " o ", t)  # "0 BIOQ" → "o BIOQ"
    t = re.sub(r"(?<![A-Za-z])([oy])(?=[A-Z(])", r" \1 ", t)    # "oICF" → "o ICF"
    t = re.sub(r"\bJo\b|\bIo\b|\blo\b", " o ", t)
    return re.sub(r"\s+", " ", t).strip()

def tokens(t):
    out = []
    for m in TOKEN.finditer(t):
        x = m.group(0)
        if x in "()": out.append(x)
        elif x.lower() in ("o", "y"): out.append(x.lower())
        else: out.append(("C", re.sub(r"\s", "", x)))
    return out

def balancear(toks):
    out, d = [], 0
    for t in toks:
        if t == "(": d += 1
        elif t == ")":
            if d == 0: continue
            d -= 1
        out.append(t)
    return out + [")"] * d

def parse(toks):
    """Gramática con Y de mayor precedencia que O; los paréntesis mandan.
    Devuelve (árbol, ambiguo) — ambiguo si un nivel mezcla y/o sin paréntesis."""
    toks = balancear(toks)
    pos, amb = 0, False
    def atom():
        nonlocal pos
        if pos < len(toks) and toks[pos] == "(":
            pos += 1; e = expr()
            if pos < len(toks) and toks[pos] == ")": pos += 1
            return e
        if pos < len(toks) and isinstance(toks[pos], tuple):
            c = toks[pos][1]; pos += 1
            return {"tipo": "curso", "codigo": c}
        pos += 1
        return None
    def expr():
        nonlocal pos, amb
        terms, ops = [atom()], []
        while pos < len(toks) and toks[pos] in ("o", "y"):
            ops.append(toks[pos]); pos += 1
            terms.append(atom())
        while pos < len(toks) and toks[pos] != ")" and (isinstance(toks[pos], tuple) or toks[pos] == "("):
            ops.append("o"); terms.append(atom())  # operador perdido por OCR: casi siempre es "o"
        if len(set(ops)) > 1: amb = True
        # Y antes que O
        grupos, cur = [], [terms[0]]
        for op, t in zip(ops, terms[1:]):
            if op == "y": cur.append(t)
            else: grupos.append(cur); cur = [t]
        grupos.append(cur)
        ands = [g[0] if len(g) == 1 else {"tipo": "todos", "de": [x for x in g if x]} for g in grupos]
        ands = [a for a in ands if a]
        uniq = []
        for a in ands:
            if a not in uniq: uniq.append(a)
        return uniq[0] if len(uniq) == 1 else {"tipo": "alguno", "de": uniq}
    tree = expr() if toks else None
    return tree, amb

def parse_lr(toks):
    """Lectura alternativa: y/o con la misma precedencia, de izquierda a derecha (para expresiones ambiguas)."""
    toks = balancear(toks); pos = 0
    def atom():
        nonlocal pos
        if pos < len(toks) and toks[pos] == "(":
            pos += 1; e = expr()
            if pos < len(toks) and toks[pos] == ")": pos += 1
            return e
        if pos < len(toks) and isinstance(toks[pos], tuple):
            c = toks[pos][1]; pos += 1; return {"tipo": "curso", "codigo": c}
        pos += 1; return None
    def expr():
        nonlocal pos
        acc = atom()
        while pos < len(toks) and toks[pos] != ")":
            op = toks[pos] if toks[pos] in ("o", "y") else "o"
            if toks[pos] in ("o", "y"): pos += 1
            r = atom()
            if acc is None: acc = r; continue
            if r is None: continue
            acc = {"tipo": "todos" if op == "y" else "alguno", "de": [acc, r]}
        return acc
    return expr() if toks else None

def codigos(t):
    if not t: return []
    if t["tipo"] == "curso": return [t["codigo"]]
    return [c for x in t["de"] for c in codigos(x)]

def podar(t, alcance):
    """Deja solo los cursos de la malla (alcance). Externo = no satisfacible en el plan vigente."""
    if not t: return None
    if t["tipo"] == "curso": return t if t["codigo"] in alcance else None
    hijos = [podar(x, alcance) for x in t["de"]]
    if t["tipo"] == "todos":
        if any(h is None for h in hijos): return None  # un Y con parte externa no se cumple en este plan
        hijos = [h for i, h in enumerate(hijos) if h not in hijos[:i]]
        return hijos[0] if len(hijos) == 1 else {"tipo": "todos", "de": hijos}
    hijos = [h for h in hijos if h is not None]
    hijos = [h for i, h in enumerate(hijos) if h not in hijos[:i]]
    if not hijos: return None
    return hijos[0] if len(hijos) == 1 else {"tipo": "alguno", "de": hijos}

def equivalencias(t, alcance, out):
    """En un O con exactamente un curso de la malla, el resto son equivalencias de ese curso."""
    if not t or t["tipo"] == "curso": return
    if t["tipo"] == "alguno":
        dentro = [x for x in t["de"] if x["tipo"] == "curso" and x["codigo"] in alcance]
        fuera = [x for x in t["de"] if not (x["tipo"] == "curso" and x["codigo"] in alcance)]
        if len(dentro) == 1:
            for f in fuera:
                cs = codigos(f)
                if cs and not any(c in alcance for c in cs):
                    out.setdefault(dentro[0]["codigo"], set()).add(" + ".join(cs))
    for x in t["de"]: equivalencias(x, alcance, out)

# ───────────── fuentes ─────────────

def unir(a, b):
    """Une líneas de una celda cortada entre páginas, quitando la línea repetida en el corte."""
    if not a or not b: return a + b
    ta, tb = a[-1].split(), b[0].split()
    for k in range(min(len(ta), len(tb)), 1, -1):
        if ta[-k:] == tb[:k]:
            resto = ta[:-k]
            return a[:-1] + ([" ".join(resto)] if resto else []) + b
    return a + b

def filas_pdf(raw):
    filas = [f for f in raw["filas"]]
    out = []
    i = 0
    while i < len(filas):
        f = filas[i]
        if f["tipo"] == "fila" and f.get("borde") == "inf" and i + 1 < len(filas) and filas[i + 1].get("borde") == "sup":
            g = filas[i + 1]
            f = dict(f)
            for k in ("codigo", "nombre", "creditos"):
                if not f[k].strip(): f[k] = g[k]
            f["req"] = unir(f["req"], g["req"]); f["coreq"] = unir(f["coreq"], g["coreq"])
            f["partes"] = [[f.get("pagina"), f.get("caja")], [g.get("pagina"), g.get("caja")]]
            i += 1
        elif f["tipo"] == "fila" and f.get("borde") == "sup" and not f["codigo"].strip() and out and out[-1]["tipo"] == "fila":
            out[-1]["req"] += f["req"]; out[-1]["coreq"] += f["coreq"]
            out[-1].setdefault("partes", [[out[-1].get("pagina"), out[-1].get("caja")]]).append([f.get("pagina"), f.get("caja")]); i += 1; continue
        out.append(f); i += 1
    return raw["cabecera"], out

def filas_html(path):
    s = open(path, encoding="utf8").read()
    cab = re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", s[: s.find("Asignatura")])))
    out = []
    for chunk in re.split(r"\n<TR>\n", s):
        txt = lambda x: re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
        m = re.search(r"(\d{3,5}-\d{1,2}S\w*\s*-\s*[^<]+)<", chunk)
        if m and "Asignatura" not in chunk[: m.start()]:
            out.append({"tipo": "titulo", "texto": m.group(1).strip()})
        tds = re.findall(r"<TD[^>]*>(.*?)</TD>", chunk, re.S)
        if not tds: continue
        code = txt(tds[0])
        if not re.match(r"^[A-Z]{2,6}\d{2,5}$", code): continue
        # bloques de requisitos: entre '<table align="left" >' y '</table>'
        bloques = re.findall(r'<table align="left" >(.*?)</table>', chunk, re.S)
        lineas = lambda b: [txt(x) for x in re.findall(r"<FONT SIZE = 1>(.*?)</FONT>", b, re.S)]
        nums = [txt(t) for t in tds[2:] if re.fullmatch(r"\d+", txt(t))]
        out.append({"tipo": "fila", "codigo": code, "nombre": txt(tds[1]), "creditos": nums[-1] if nums else "",
                    "req": lineas(bloques[0]) if bloques else [], "coreq": lineas(bloques[1]) if len(bloques) > 1 else []})
    return cab, out

MENCION_CLAVES = {"MAQ": "MAQ", "CUBIER": "CUBI", "BACIMET": "BACIMET", "IFIME": "IFIME", "IMAGEN": "IFIME", "MORFO": "MORFO",
                  "OFTA": "OFTA", "OTORR": "OTORRINO", "OTO": "OTORRINO"}

OVERRIDES = {}

def construir(fuente, actual_path, salida, clave=None):
    global OVERRIDES
    import os
    ovp = os.path.join(os.path.dirname(__file__), "overrides.json")
    OVERRIDES = json.load(open(ovp)).get(clave or "", {}) if os.path.exists(ovp) else {}
    es_texto = fuente.endswith(".htm") or "Medicina" in fuente or "TM" in fuente
    actual = json.load(open(actual_path))
    sems = actual.get("semestres") or actual.get("semestres_comunes", []) + [s for m in actual.get("menciones", {}).values() for s in m["semestres"]]
    dic_malla = {c["codigo"] for s in sems for c in s["cursos"]}
    cursos_actuales = [dict(c, semestre=s["numero"]) for s in sems for c in s["cursos"]]
    # diccionario ampliado: códigos citados en todos los textos actuales (vienen de los mismos documentos)
    import glob, os
    dic_ext = set()
    for f in glob.glob(os.path.join(os.path.dirname(actual_path), "*.json")):
        for m in re.finditer(r"\b[A-Z]{2,6} ?P?\d{2,4}[A-Z]?\b", open(f, encoding="utf8").read()):
            dic_ext.add(m.group(0).replace(" ", ""))
    dic_all = dic_malla | dic_ext
    dic_of = set()

    if fuente.endswith(".htm"):
        cab, filas = filas_html(fuente)
    else:
        cab, filas = filas_pdf(json.load(open(fuente)))

    if not es_texto:
        for f in filas:
            if f["tipo"] == "fila" and f["codigo"].strip():
                c, q = fix_code(f["codigo"], dic_malla, dic_malla)
                if c and q in ("ok", "corregido", "nuevo") and BIEN.match(c) and re.match(r"^[A-Z]{3,5}\d{3,4}$", c):
                    dic_of.add(c)
    dic_all |= dic_of
    dic_req_malla = dic_malla | dic_of
    cursos, semestre, mencion, avisos = [], None, None, []
    for f in filas:
        if f["tipo"] == "titulo":
            t = f["texto"].upper()
            m = re.search(r"[-_.]\s*(\d{1,2})\s*S", t) or re.search(r"\s(\d{1,2})\s*SEM", t)
            if m: semestre = int(m.group(1))
            resto = t.split(" - ", 1)[-1] if " - " in t else t
            mencion = next((v for k, v in MENCION_CLAVES.items() if k in resto), None)
            continue
        if f["tipo"] != "fila": continue
        if not f["codigo"].strip() and not f["req"]: continue
        if not f["req"] and not f["coreq"] and len(norm_txt(f["nombre"])) < 4: continue
        juntos = (f["codigo"] + " " + f["nombre"]).upper()
        mt = re.search(r"[-_.]\s*(\d{1,2})\s*SEM", juntos) or re.search(r"(?:^|\s)(\d{1,2})\s*SEM[_ ]", juntos)
        if mt and not f["req"]:
            semestre = int(mt.group(1)); mencion = next((v for k, v in MENCION_CLAVES.items() if k in juntos), None); continue
        cod, calidad = fix_code(f["codigo"], dic_malla, dic_malla) if not es_texto else (re.sub(r"\s", "", f["codigo"]), "ok")
        enlace = cod if cod in dic_malla else None
        if cod in OVERRIDES.get("enlaces", {}): enlace = OVERRIDES["enlaces"][cod]
        if not enlace and len(norm_txt(f["nombre"])) >= 5:
            n = norm_txt(f["nombre"])
            cand = sorted((lev(n, norm_txt(c["nombre"])[: len(n) + 3]), c["codigo"]) for c in cursos_actuales)
            if cand and cand[0][0] <= max(3, len(n) // 5):
                enlace = cand[0][1]
        if enlace and cod != enlace and lev(cod or "", enlace) <= 1 and not OVERRIDES.get("sin_enlace"):
            cod, calidad = enlace, "corregido"
        ov = OVERRIDES.get("codigos", {})
        if cod in ov: cod, calidad = ov[cod], "manual"
        elif (calidad in ("vacio", "desconocido") or not re.match(r"^[A-Z]{3,5}\d{3,4}$", cod or "")) and enlace:
            cod, calidad = enlace, "por-nombre"
        if calidad == "vacio" or cod is None:
            avisos.append(f"fila sin código (nombre: {f['nombre']!r}, req: {' '.join(f['req'])[:60]!r})"); continue
        def req(lines):
            t = limpiar_req(lines)
            toks = tokens(t)
            fixed, dudosos = [], []
            for x in toks:
                if isinstance(x, tuple):
                    c, q = (x[1], "ok") if es_texto else fix_code(x[1], dic_all, dic_req_malla)
                    if q == "desconocido": dudosos.append(c)
                    fixed.append(("C", c))
                else: fixed.append(x)
            tree, amb = parse(fixed)
            return {"texto": " ".join(x if isinstance(x, str) else x[1] for x in fixed), "arbol": tree, "arbolLR": parse_lr(fixed) if amb else None, "ambiguo": amb, "dudosos": dudosos}
        cr = re.sub(r"\D", "", f.get("creditos", ""))
        cursos.append({"codigo": cod, "enlace": enlace, "calidadCodigo": calidad, "nombre": f["nombre"], "sct": int(cr) if cr else None,
                       "semestre": semestre, "mencion": mencion, "req": req(f["req"]), "coreq": req(f["coreq"]),
                       "partes": f.get("partes") or [[f.get("pagina"), f.get("caja")]]})
    prog = re.search(r"PROGRAMA:?\s*(UNAB\d+)\s*-\s*(.+?)\s+PERIODO", cab)
    cat = re.search(r"CAT[AÁ]LOGO:?\s*(\d{6})\s*-\s*(.+?)\s+PERIODO", cab)
    out = {"ocr": not es_texto,
           "programa": prog.group(1) if prog else None, "carrera": prog.group(2).strip() if prog else None,
           "catalogo": cat.group(1) if cat else None, "catalogoTexto": cat.group(2).strip() if cat else None,
           "cursos": cursos, "avisos": avisos}
    json.dump(out, open(salida, "w"), ensure_ascii=False, indent=1)
    return out

if __name__ == "__main__":
    o = construir(*sys.argv[1:4], clave=sys.argv[3].split("/")[-1].replace(".json", ""))
    print(sys.argv[3], o["programa"], o["catalogo"], len(o["cursos"]), "cursos", len(o["avisos"]), "avisos")
