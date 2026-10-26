"""Aplica a cada malla actual (formato del MVP) las diferencias verificadas contra el documento oficial.

Uso: python3 corregir.py <clave> <actual.json> <oficial.json> <diff.json> <salida.json> <cambios.json>

Reglas:
- Prerrequisitos/correquisitos: se reemplazan por el requisito oficial (podado a los cursos del plan),
  salvo expresiones ambiguas sin lectura que coincida (se mantiene lo actual y se informa).
- Texto de requisitos (prereq_expr / correq_expr): pasa a ser el texto oficial.
- SCT: se toma el oficial en documentos con texto; en documentos escaneados solo los verificados a mano.
- Códigos y nombres: solo los corregidos a mano (overrides.json).
- Equivalencias: los códigos de planes antiguos citados como alternativa se guardan aparte.
"""
import json, sys, copy
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from comparar import aplanar
from oficial import codigos

clave, actual_p, of_p, diff_p, out_p, cambios_p = sys.argv[1:7]
OV = json.load(open(__file__.rsplit("/", 1)[0] + "/overrides.json")).get(clave, {})
SCT_VERIFICADOS = {  # documentos escaneados: SCT confirmados mirando el PDF
    "CInf": {"CINF101": 16, "CINF102": 10, "CINF103": 19, "CINF104": 15, "CINF105": 13, "CINF107": 14, "CINF108": 15,
             "CINF110": 14, "CINF111": 14, "CINF112": 14, "CINF400": 28, "CINF200": 6},
    "Geo": {"GEOL401": 16},
}.get(clave, {})

actual = json.load(open(actual_p)); of = json.load(open(of_p)); diff = json.load(open(diff_p))
nuevo = copy.deepcopy(actual)
planos = aplanar(nuevo)
# referencias a los objetos reales dentro de `nuevo`
reales = {}
def recorrer(sems, men):
    for s in sems:
        for c in s["cursos"]: reales[(c["codigo"], men)] = c
if "semestres_comunes" in nuevo:
    recorrer(nuevo["semestres_comunes"], None)
    for k, m in nuevo["menciones"].items(): recorrer(m["semestres"], k)
else:
    recorrer(nuevo["semestres"], None)

def id_de(codigo, mencion):
    c = reales.get((codigo, mencion)) or reales.get((codigo, None))
    return c["id"] if c else None

cambios = []
for o in of["cursos"]:
    k = (o.get("enlace") or o["codigo"], o["mencion"])
    a = reales.get(k)
    if not a: continue
    etq = a["codigo"] + (f" ({o['mencion']})" if o["mencion"] else "")
    for campo, ids_k, txt_k, nombre in (("req", "prerrequisitos", "prereq_expr", "prerrequisitos"), ("coreq", "correquisitos", "correq_expr", "correquisitos")):
        r = o[campo]
        if r.get("decision") == "mantener-actual":
            cambios.append({"curso": etq, "campo": nombre, "tipo": "mantenido (texto oficial ambiguo)", "texto": r["texto"]}); continue
        arbol = r.get("podado")
        cods = list(dict.fromkeys(codigos(arbol)))
        ids = [i for i in (id_de(c, o["mencion"]) for c in cods) if i is not None]
        antes = sorted(a.get(ids_k) or [])
        if sorted(ids) != antes:
            nombres = lambda xs: [next((p["codigo"] for p in planos if p["id"] == i), str(i)) for i in xs]
            cambios.append({"curso": etq, "campo": nombre, "tipo": "corregido", "antes": nombres(antes), "despues": nombres(ids), "texto": r["texto"]})
        if ids or ids_k == "prerrequisitos": a[ids_k] = ids
        elif ids_k in a: a[ids_k] = []
        if r["texto"]: a[txt_k] = r["texto"]
        elif txt_k in a and campo == "req": a[txt_k] = ""
    # SCT
    sct_of = o["sct"] if not of.get("ocr") else SCT_VERIFICADOS.get(o["codigo"])
    if sct_of is not None and sct_of != a["sct"]:
        cambios.append({"curso": etq, "campo": "sct", "tipo": "corregido", "antes": a["sct"], "despues": sct_of}); a["sct"] = sct_of
    # código y nombre (solo correcciones manuales)
    if OV.get("sin_enlace") and o["codigo"] != a["codigo"] and o.get("calidadCodigo") in ("nuevo", "manual", "ok", "corregido"):
        cambios.append({"curso": etq, "campo": "codigo", "tipo": "corregido", "antes": a["codigo"], "despues": o["codigo"]})
        a["_nuevo_codigo"] = o["codigo"]
    if o["codigo"] in OV.get("nombres", {}):
        n = OV["nombres"][o["codigo"]]
        if n != a["nombre"]:
            cambios.append({"curso": etq, "campo": "nombre", "tipo": "corregido", "antes": a["nombre"], "despues": n}); a["nombre"] = n

# renombrar códigos al final (los ids no cambian)
mapa = {}
for c in reales.values():
    if "_nuevo_codigo" in c:
        mapa[c["codigo"]] = c["_nuevo_codigo"]; c["codigo"] = c.pop("_nuevo_codigo")

# equivalencias (en códigos del plan corregido)
eq = {}
for destino, origenes in diff["equivalencias"].items():
    d = mapa.get(destino, destino)
    if any(c["codigo"] == d for c in reales.values()):
        eq[d] = [o.split(" + ") for o in origenes]
nuevo["equivalencias"] = eq
# total de créditos: si había un total declarado y la malla se corrigió, se recalcula desde los cursos
suma = sum(c["sct"] for c in reales.values()) if "semestres" in nuevo else None
# los SCT de cada curso ya están contrastados con el documento, así que el total es su suma
if suma is not None and nuevo.get("total_creditos") != suma:
    cambios.append({"curso": "(total)", "campo": "total_creditos", "tipo": "corregido" if nuevo.get("total_creditos") else "completado",
                    "antes": nuevo.get("total_creditos"), "despues": suma})
    nuevo["total_creditos"] = suma
nuevo["fuente_oficial"] = {"programa": of["programa"], "catalogo": of.get("catalogo"), "catalogoTexto": of.get("catalogoTexto"),
                           "lectura": "OCR revisado" if of.get("ocr") else "texto del documento"}
if "(" not in nuevo["carrera"]: nuevo["carrera"] += " (UNAB)"
if "semestres" in nuevo and not nuevo.get("totalSemestres"):
    nuevo["totalSemestres"] = max(s["numero"] for s in nuevo["semestres"])
# orden de claves como en el original
orden = ["carrera", "codigo_programa", "fuente_oficial", "total_creditos", "totalSemestres", "menciones_disponibles", "total_creditos_por_mencion", "semestres", "semestres_comunes", "menciones", "equivalencias"]
nuevo = {k: nuevo[k] for k in orden if k in nuevo} | {k: v for k, v in nuevo.items() if k not in orden}
json.dump(nuevo, open(out_p, "w"), ensure_ascii=False, indent=2)
json.dump({"clave": clave, "cambios": cambios, "renombres": mapa, "equivalencias": sum(len(v) for v in eq.values())}, open(cambios_p, "w"), ensure_ascii=False, indent=1)
print(clave, len([c for c in cambios if c["tipo"] == "corregido"]), "correcciones,", len(mapa), "códigos renombrados,", len(eq), "cursos con equivalencias")
