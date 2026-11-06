"""PROTOTYPE (spike/ia-mallas): turn a malla PDF or photo into a draft malla with Claude.

Not part of V2.0 and not wired to any route. It exists to measure how well AI extraction works
against the 13 verified mallas before the V2.1 design (IA-01..IA-05, D-07, D-08).

Rules it keeps from AGENTS.md:
- The result is always a draft ("estado": "borrador"); nothing is imported or saved.
- Nothing is invented: a requirement the model cannot read, or one that points to a course
  that is not in the draft, becomes "unknown" (prereq_status), never "none".
- The document's content is never logged (NF-07).
"""

from __future__ import annotations

import base64
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any, Protocol

from app.services.legacy_import import _collect_entries, _detect

DEFAULT_MODEL = "claude-sonnet-5-5"
MAX_OUTPUT_TOKENS = 16000

MEDIA_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".webp": "image/webp",
    ".gif": "image/gif",
}

TOOL_NAME = "entregar_malla"

SYSTEM_PROMPT = """Eres un extractor de mallas curriculares de universidades chilenas.
Recibes un documento (PDF o foto) con la malla de una carrera y la devuelves llamando a la
herramienta entregar_malla. Reglas estrictas:
- Transcribe solo lo que está en el documento. No completes con conocimiento general.
- Un ramo por cada asignatura visible, en su semestre (1, 2, 3...). Si el documento usa números
  romanos, conviértelos.
- "ref" identifica al ramo dentro de este documento: su código tal como aparece (p. ej.
  "CINF102"); si no tiene código, el número que lo identifica en el documento (p. ej. "22").
- Los prerrequisitos se indican con esas mismas "ref".
- prereq_estado:
  "ninguno" solo si el documento muestra claramente que el ramo no tiene requisitos;
  "conocido" si los lees completos;
  "desconocido" si no se leen, están cortados o no estás seguro. Ante la duda: "desconocido".
- Si un requisito es "Semestre N aprobado" o "N semestres aprobados", usa
  semestres_aprobados_requeridos = N y deja prerrequisitos vacío.
- Si hay alternativas ("A o B"), copia el texto completo en prereq_texto y pon en
  prerrequisitos solo los que se exigen siempre; si no se puede saber, "desconocido".
- Créditos: usa el número del documento (SCT u otro) y dilo en sistema_creditos.
- Anota en advertencias cualquier cosa dudosa: menciones o especialidades, ramos ilegibles,
  totales que no cuadran."""

TOOL_SCHEMA: dict[str, Any] = {
    "name": TOOL_NAME,
    "description": "Entrega la malla extraída del documento, como borrador para revisión.",
    "input_schema": {
        "type": "object",
        "required": ["carrera", "semestres", "advertencias"],
        "properties": {
            "carrera": {"type": "string"},
            "universidad": {"type": ["string", "null"]},
            "codigo_programa": {"type": ["string", "null"]},
            "sistema_creditos": {"type": ["string", "null"]},
            "total_creditos": {"type": ["integer", "null"]},
            "semestres": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["numero", "cursos"],
                    "properties": {
                        "numero": {"type": "integer"},
                        "cursos": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["ref", "nombre", "prereq_estado", "prerrequisitos"],
                                "properties": {
                                    "ref": {"type": "string"},
                                    "codigo": {"type": ["string", "null"]},
                                    "numero_en_documento": {"type": ["integer", "null"]},
                                    "nombre": {"type": "string"},
                                    "creditos": {"type": ["integer", "null"]},
                                    "prereq_estado": {
                                        "enum": ["ninguno", "conocido", "desconocido"]
                                    },
                                    "prerrequisitos": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "semestres_aprobados_requeridos": {"type": ["integer", "null"]},
                                    "prereq_texto": {"type": ["string", "null"]},
                                },
                            },
                        },
                    },
                },
            },
            "advertencias": {"type": "array", "items": {"type": "string"}},
        },
    },
}


class MessagesClient(Protocol):
    """The part of anthropic.Anthropic we use (so tests can pass a fake)."""

    @property
    def messages(self) -> Any: ...


@dataclass
class Extraction:
    raw: dict[str, Any]  # what the model returned through the tool
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    stop_reason: str | None = None


@dataclass
class Draft:
    malla: dict[str, Any]  # legacy malla JSON (same format as frontend/public/mallas)
    warnings: list[str] = field(default_factory=list)
    unknown_courses: int = 0


def media_type_for(filename: str) -> str:
    for ext, mt in MEDIA_TYPES.items():
        if filename.lower().endswith(ext):
            return mt
    raise ValueError("Formato no soportado: usa PDF, PNG, JPG, WEBP o GIF")


def extract(
    content: bytes, media_type: str, *, client: MessagesClient, model: str = DEFAULT_MODEL
) -> Extraction:
    """One call to Claude. The document goes as a document/image block; output is forced
    through the tool so it always matches TOOL_SCHEMA."""
    data = base64.standard_b64encode(content).decode("ascii")
    block_type = "document" if media_type == "application/pdf" else "image"
    response = client.messages.create(
        model=model,
        max_tokens=MAX_OUTPUT_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[TOOL_SCHEMA],
        tool_choice={"type": "tool", "name": TOOL_NAME},
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": block_type,
                        "source": {"type": "base64", "media_type": media_type, "data": data},
                    },
                    {"type": "text", "text": "Extrae la malla de este documento."},
                ],
            }
        ],
    )
    tool_input = next(
        (b.input for b in response.content if getattr(b, "type", None) == "tool_use"), None
    )
    if tool_input is None:
        raise RuntimeError("El modelo no devolvió la malla")
    usage = getattr(response, "usage", None)
    return Extraction(
        raw=dict(tool_input),
        model=model,
        input_tokens=getattr(usage, "input_tokens", 0) or 0,
        output_tokens=getattr(usage, "output_tokens", 0) or 0,
        stop_reason=getattr(response, "stop_reason", None),
    )


def to_draft(raw: dict[str, Any]) -> Draft:
    """Model output -> legacy malla JSON, enforcing the no-invention rules.

    ids: the number in the document when every course has a distinct one (the U. de Chile
    mallas number their courses); otherwise 1..N in reading order.
    """
    warnings = [str(w) for w in raw.get("advertencias") or []]
    semesters = sorted(raw.get("semestres") or [], key=lambda s: int(s["numero"]))
    flat = [(int(s["numero"]), c) for s in semesters for c in s.get("cursos") or []]

    numbers = [c.get("numero_en_documento") for _, c in flat]
    use_numbers = all(isinstance(n, int) for n in numbers) and len(set(numbers)) == len(numbers)
    ids = numbers if use_numbers else list(range(1, len(flat) + 1))

    ref_to_id: dict[str, int] = {}
    for (_, c), cid in zip(flat, ids, strict=True):
        ref = str(c.get("ref") or "").strip()
        if ref in ref_to_id:
            warnings.append(f"ref repetida en el documento: {ref}")
        ref_to_id.setdefault(ref, cid)
        if c.get("codigo"):
            ref_to_id.setdefault(str(c["codigo"]).strip(), cid)
        if isinstance(c.get("numero_en_documento"), int):
            ref_to_id.setdefault(str(c["numero_en_documento"]), cid)

    out_semesters: dict[int, list[dict[str, Any]]] = {}
    unknown = 0
    for (sem, c), cid in zip(flat, ids, strict=True):
        status = c.get("prereq_estado")
        prereq_ids: list[int] = []
        n_sem = c.get("semestres_aprobados_requeridos")
        if status == "conocido" and isinstance(n_sem, int) and n_sem > 0:
            # "Semestre N aprobado": every course up to semester N (as the verified mallas do).
            prereq_ids = [i for (s, _), i in zip(flat, ids, strict=True) if s <= n_sem]
        elif status == "conocido":
            for ref in c.get("prerrequisitos") or []:
                target = ref_to_id.get(str(ref).strip())
                if target is None:
                    status = "desconocido"
                    warnings.append(f"{c.get('ref')}: requisito {ref} no está en la malla")
                    prereq_ids = []
                    break
                prereq_ids.append(target)
            if status == "conocido" and not prereq_ids:
                status = "desconocido"  # "known" with nothing listed is not trustworthy
        course: dict[str, Any] = {
            "id": cid,
            "codigo": (c.get("codigo") or c.get("ref") or f"X{cid:03d}"),
            "nombre": c.get("nombre") or "",
            "sct": c.get("creditos"),
            "prerrequisitos": prereq_ids if status == "conocido" else [],
            "prereq_status": {"ninguno": "none", "conocido": "known"}.get(status or "", "unknown"),
        }
        if c.get("prereq_texto"):
            course["prereq_expr"] = c["prereq_texto"]
        if course["prereq_status"] == "unknown":
            unknown += 1
        out_semesters.setdefault(sem, []).append(course)

    malla: dict[str, Any] = {
        "estado": "borrador",
        "carrera": raw.get("carrera") or "",
        "universidad": raw.get("universidad"),
        "codigo_programa": raw.get("codigo_programa"),
        "sistema_creditos": raw.get("sistema_creditos"),
        "total_creditos": raw.get("total_creditos"),
        "totalSemestres": max(out_semesters) if out_semesters else 0,
        "semestres": [{"numero": n, "cursos": cs} for n, cs in sorted(out_semesters.items())],
    }
    return Draft(malla=malla, warnings=warnings, unknown_courses=unknown)


# Structural problems: the draft cannot be trusted until they are fixed. (The importer's
# text-vs-ids checks are informative only and are left out.)
STRUCTURAL_KINDS = {
    "id_duplicado",
    "id_inexistente",
    "autorreferencia",
    "ciclo",
    "prereq_mismo_periodo_o_posterior",
    "codigo_repetido",
    "creditos_totales_cero",
}


def validate(malla: dict[str, Any]) -> list[str]:
    """Structural checks of the legacy importer, plus a credit sum check."""
    entries = _collect_entries(malla)
    issues = [
        f"{i.kind}: {i.detail}"
        for i in _detect("borrador", malla.get("carrera") or "", malla, entries)
        if i.kind in STRUCTURAL_KINDS
    ]
    total = malla.get("total_creditos")
    credits = [c.get("sct") for s in malla["semestres"] for c in s["cursos"]]
    if isinstance(total, int) and all(isinstance(x, int) for x in credits):
        if sum(credits) != total:
            issues.append(f"creditos: la suma de ramos ({sum(credits)}) no da el total ({total})")
    return issues


# ---------------------------------------------------------------- measurement


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def _courses(malla: dict[str, Any]) -> list[tuple[int, dict[str, Any]]]:
    return [(e.period, e.raw) for e in _collect_entries(malla)]


def compare(draft: dict[str, Any], verified: dict[str, Any]) -> dict[str, Any]:
    """How close the draft is to a verified malla. Courses are matched by code, then by id,
    then by normalized name; prerequisites are compared as sets of matched courses."""
    d_list, v_list = _courses(draft), _courses(verified)
    v_by_code = {c.get("codigo"): (s, c) for s, c in v_list}
    v_by_id = {c.get("id"): (s, c) for s, c in v_list}
    v_by_name = {_norm(c.get("nombre", "")): (s, c) for s, c in v_list}

    def best_index() -> tuple[str, dict[Any, Any]]:
        scores = {
            "codigo": sum(1 for _, c in d_list if c.get("codigo") in v_by_code),
            "id": sum(
                1
                for _, c in d_list
                if c.get("id") in v_by_id
                and _norm(v_by_id[c["id"]][1].get("nombre", "")) == _norm(c.get("nombre", ""))
            ),
            "nombre": sum(1 for _, c in d_list if _norm(c.get("nombre", "")) in v_by_name),
        }
        method = max(scores, key=lambda k: scores[k])
        return method, {"codigo": v_by_code, "id": v_by_id, "nombre": v_by_name}[method]

    method, index = best_index()

    def key(c: dict[str, Any]) -> Any:
        return {"codigo": c.get("codigo"), "id": c.get("id"), "nombre": _norm(c.get("nombre", ""))}[
            method
        ]

    pairs: dict[int, tuple[int, dict[str, Any], int, dict[str, Any]]] = {}
    used: set[int] = set()
    for ds, dc in d_list:
        hit = index.get(key(dc))
        if hit and hit[1]["id"] not in used:
            used.add(hit[1]["id"])
            pairs[dc["id"]] = (ds, dc, hit[0], hit[1])

    d_to_v = {d_id: v["id"] for d_id, (_, _, _, v) in pairs.items()}
    sem_ok = sum(1 for ds, _, vs, _ in pairs.values() if ds == vs)
    sct_ok = sum(1 for _, dc, _, vc in pairs.values() if dc.get("sct") == vc.get("sct"))
    pre_ok = pre_wrong = pre_unknown = 0
    for _, dc, _, vc in pairs.values():
        if dc.get("prereq_status") == "unknown":
            pre_unknown += 1
            continue
        mapped = {d_to_v.get(p) for p in dc.get("prerrequisitos") or []}
        if mapped == set(vc.get("prerrequisitos") or []):
            pre_ok += 1
        else:
            pre_wrong += 1

    matched = len(pairs)
    answered = pre_ok + pre_wrong

    def pct(n: int, d: int) -> float:
        return round(100 * n / d, 1) if d else 0.0

    return {
        "metodo_cruce": method,
        "ramos_verificados": len(v_list),
        "ramos_borrador": len(d_list),
        "ramos_cruzados": matched,
        "cobertura_pct": pct(matched, len(v_list)),
        "ramos_inventados": len(d_list) - matched,
        "semestre_correcto_pct": pct(sem_ok, matched),
        "creditos_correctos_pct": pct(sct_ok, matched),
        "prerrequisitos_correctos_pct": pct(pre_ok, answered),
        "prerrequisitos_incorrectos": pre_wrong,
        "prerrequisitos_desconocidos": pre_unknown,
    }
