"""Compara la malla oficial extraída con el JSON actual de Malla Pro.
Uso: python3 comparar.py <oficial.json> <actual.json> <salida.json>
"""
import json, sys, re
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from oficial import podar, codigos, equivalencias, norm_txt, lev

def aplanar(a):
    if "semestres_comunes" in a:
        out = [dict(c, semestre=s["numero"], mencion=None) for s in a["semestres_comunes"] for c in s["cursos"]]
        for k, m in a["menciones"].items():
            out += [dict(c, semestre=s["numero"], mencion=k) for s in m["semestres"] for c in s["cursos"]]
        return out
    return [dict(c, semestre=s["numero"], mencion=None) for s in a["semestres"] for c in s["cursos"]]

def forma(t):
    """Texto legible de un árbol podado."""
    if not t: return "—"
    if t["tipo"] == "curso": return t["codigo"]
    sep = " y " if t["tipo"] == "todos" else " o "
    return sep.join(forma(x) if x["tipo"] == "curso" else f"({forma(x)})" for x in t["de"])

def solo_y(t):
    return t is None or t["tipo"] == "curso" or (t["tipo"] == "todos" and all(x["tipo"] == "curso" for x in t["de"]))

def comparar(of, ac):
    A = aplanar(ac)
    porId = {c["id"]: c for c in A}
    key = lambda c: (c["codigo"], c["mencion"])
    amap = {key(c): c for c in A}
    omap = {(c.get("enlace") or c["codigo"], c["mencion"]): c for c in of["cursos"]}
    codigo_distinto = [f"{o['codigo']} (oficial) ↔ {k[0]} (actual): {o['nombre']}" for k, o in omap.items() if o.get("enlace") and o["enlace"] != o["codigo"]]
    menciones = {c["mencion"] for c in of["cursos"]} | {c["mencion"] for c in A}
    of2ac = {c["codigo"]: c["enlace"] for c in of["cursos"] if c.get("enlace")}
    def traducir(t):
        if not t: return t
        if t["tipo"] == "curso": return {"tipo": "curso", "codigo": of2ac.get(t["codigo"], t["codigo"])}
        if "de" in t: return {"tipo": t["tipo"], "de": [traducir(x) for x in t["de"]]}
        return t
    def alcance(m):
        return {c["codigo"] for c in of["cursos"] if c["mencion"] in (None, m)} | {c["codigo"] for c in A if c["mencion"] in (None, m)}
    res = {"programa": of["programa"], "catalogo": of["catalogoTexto"], "soloOficial": [], "soloActual": [],
           "nombre": [], "sct": [], "semestre": [], "prerrequisitos": [], "correquisitos": [], "ambiguos": [],
           "equivalencias": {}, "dudosos": set(), "avisos": of["avisos"], "codigo": codigo_distinto}
    # cursos que no calzan por mención pero sí por código (mención mal detectada)
    for k, o in omap.items():
        if k not in amap:
            res["soloOficial"].append(f"{o['codigo']} {o['nombre']} (sem {o['semestre']}{', ' + o['mencion'] if o['mencion'] else ''})")
    for k, a in amap.items():
        if k not in omap:
            res["soloActual"].append(f"{a['codigo']} {a['nombre']} (sem {a['semestre']}{', ' + a['mencion'] if a['mencion'] else ''})")
    for k, o in omap.items():
        a = amap.get(k)
        if not a: continue
        o["_k"] = k
        etq = o["codigo"] + (f" ({o['mencion']})" if o["mencion"] else "")
        n1, n2 = norm_txt(o["nombre"]), norm_txt(a["nombre"])
        if not of.get("ocr") and n1 and n1 != n2 and lev(n1, n2) > max(2, len(n2) // 8):
            res["nombre"].append(f"{etq}: oficial «{o['nombre']}» / actual «{a['nombre']}»")
        perdida_ocr = of.get("ocr") and o["sct"] is not None and str(a["sct"]).endswith(str(o["sct"]))
        if o["sct"] is not None and o["sct"] != a["sct"] and not perdida_ocr:
            res["sct"].append(f"{etq}: oficial {o['sct']} / actual {a['sct']}")
        if o["semestre"] != a["semestre"]:
            res["semestre"].append(f"{etq}: oficial {o['semestre']} / actual {a['semestre']}")
        alc = alcance(o["mencion"])
        for campo, idk, dest in (("req", "prerrequisitos", "prerrequisitos"), ("coreq", "correquisitos", "correquisitos")):
            r = o[campo]
            res["dudosos"].update(r["dudosos"])
            arbol = podar(traducir(r["arbol"]), alc - {o["codigo"], k[0]})
            equivalencias(traducir(r["arbol"]), alc, res["equivalencias"])
            of_set = set(codigos(arbol))
            ac_set = {porId[i]["codigo"] for i in a.get(idk) or [] if i in porId}
            lectura = "única"
            if r["ambiguo"]:
                lr = podar(traducir(r.get("arbolLR")), alc - {o["codigo"], k[0]})
                lr_set = set(codigos(lr))
                if lr_set == set(codigos(arbol)) and forma(lr) == forma(arbol):
                    lectura = "única"
                elif lr_set == ac_set and solo_y(lr):
                    arbol, of_set, lectura = lr, lr_set, "izq-der (coincide con la actual)"
                elif of_set == ac_set:
                    lectura = "precedencia-y (coincide con la actual)"
                else:
                    lectura = f"ambigua: «{forma(arbol)}» o «{forma(lr)}»"
                res["ambiguos"].append(f"{etq}: {lectura} — texto «{r['texto'][:160]}»")
            if lectura.startswith("ambigua"):
                res[dest].append({"curso": etq, "oficial": lectura, "actual": " y ".join(sorted(ac_set)) or "—", "faltan": [], "sobran": [], "hayO": True, "texto": r["texto"], "ambiguo": True})
                o[campo]["podado"] = None; o[campo]["decision"] = "mantener-actual"
                continue
            if of_set != ac_set or not solo_y(arbol):
                res[dest].append({"curso": etq, "oficial": forma(arbol), "actual": " y ".join(sorted(ac_set)) or "—",
                                  "faltan": sorted(of_set - ac_set), "sobran": sorted(ac_set - of_set),
                                  "hayO": not solo_y(arbol), "texto": r["texto"]})
            o[campo]["podado"] = arbol
    res["dudosos"] = sorted(res["dudosos"])
    res["equivalencias"] = {k: sorted(v) for k, v in sorted(res["equivalencias"].items())}
    return res

if __name__ == "__main__":
    of, ac = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    r = comparar(of, ac)
    json.dump(r, open(sys.argv[3], "w"), ensure_ascii=False, indent=1)
    json.dump(of, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)  # guarda árboles podados
    print(sys.argv[2].split("/")[-1], {k: len(v) for k, v in r.items() if isinstance(v, (list, dict, set))})
