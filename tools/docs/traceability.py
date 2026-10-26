"""Genera docs/plan/traceability.md desde los requerimientos y el backlog.
Conserva la columna "Pruebas" que ya exista en el archivo. Uso: python3 tools/docs/traceability.py"""
import re, os
R = "docs/requirements/requerimientos-v1.2.md"; B = "docs/plan/backlog.md"; T = "docs/plan/traceability.md"
req = open(R).read(); back = open(B).read()
reqs = {}
for m in re.finditer(r"^\|\s*(?:\*\*)?([A-Z]{2}-\d{2})(?:\*\*)?(?:\s*\*\*[A-Z]+\*\*)?\s*\|\s*([^|]+?)\s*\|", req, re.M):
    reqs.setdefault(m.group(1), m.group(2).strip())
ENTREGA = {**{k: "V2.0" for k in "CU CA MP AV NO HO PL AN TU".split()}, "AD": "V2.0", "PR": "V2.2", "CO": "V2.2", "PA": "V2.2",
           "IA": "V2.1", "OF": "V2.1", "MC": "V2.1", "SC": "Posterior", "NF": "Transversal"}
ENTREGA_AD = {"AD-04": "V2.1", "AD-05": "V2.1", "AD-06": "V2.1", "AD-07": "V2.0", "AD-08": "V2.2"}
def expand(txt):
    out = set(re.findall(r"[A-Z]{2}-\d{2}", txt))
    for a, b in re.findall(r"([A-Z]{2}-\d{2})…([A-Z]{2}-\d{2})", txt):
        p = a[:3]
        for i in range(int(a[3:]), int(b[3:]) + 1): out.add(f"{p}{i:02d}")
    return out
tareas = {}
for bloque in re.split(r"^### ", back, flags=re.M)[1:]:
    tid = bloque.split(" ")[0]
    m = re.search(r"Requisitos: ([^\n·]+)", bloque)
    if m:
        for r in expand(m.group(1)): tareas.setdefault(r, []).append(tid)
for linea in re.findall(r"^- \*\*(.+?)\*\* — (.+)$", back, re.M):
    for r in expand(linea[1]): tareas.setdefault(r, []).append("épica " + linea[0].strip())
# Ya implementado antes del backlog (ver "Hecho antes de este backlog")
for rid, ent in {"CU-01": "s02", "CA-01": "s03 (parcial)", "CA-03": "s03 (parcial)"}.items():
    tareas.setdefault(rid, []).append(ent)
previas = {}
if os.path.exists(T):
    for m in re.finditer(r"^\| ([A-Z]{2}-\d{2}) \|(?:[^|]*\|){3}([^|]*)\|", open(T).read(), re.M):
        previas[m.group(1)] = m.group(2).strip()
L = ["# Trazabilidad requisito → tarea → prueba", "",
     "Generado con `python3 tools/docs/traceability.py` desde los requerimientos y el backlog. "
     "La columna **Pruebas** la completa el implementador al cerrar cada tarea (ruta del archivo y nombre del caso) y se conserva al regenerar.", "",
     "| ID | Requisito | Entrega | Tareas | Pruebas |", "|---|---|---|---|---|"]
sin = []
for rid in sorted(reqs, key=lambda x: (x[:2], int(x[3:]))):
    if rid == "PR-07": continue
    ent = ENTREGA_AD.get(rid, ENTREGA.get(rid[:2], "?"))
    ts = ", ".join(sorted(set(tareas.get(rid, [])))) or "—"
    if ts == "—": sin.append(rid)
    L.append(f"| {rid} | {reqs[rid][:90]} | {ent} | {ts} | {previas.get(rid, '')} |")
L += ["", f"Requisitos sin tarea asignada: {', '.join(sin) if sin else 'ninguno'}.", "PR-07 está retirado y no se implementa."]
open(T, "w").write("\n".join(L) + "\n")
print(len(reqs), "requisitos;", "sin tarea:", sin)
