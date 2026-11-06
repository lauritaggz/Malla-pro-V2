"""Prototype AI extraction (spike/ia-mallas): conversion, no-invention rules and measurement.
The model is faked: these tests never call the API."""

import copy
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from app.services.ai_malla import (
    TOOL_NAME,
    compare,
    extract,
    media_type_for,
    to_draft,
    validate,
)

MALLAS = Path(__file__).resolve().parents[2] / "frontend" / "public" / "mallas"


def verified(stem: str) -> dict[str, Any]:
    return json.loads((MALLAS / f"{stem}.json").read_text(encoding="utf-8"))


def as_model_output(malla: dict[str, Any], *, by_number: bool) -> dict[str, Any]:
    """What a perfect model would return for a verified malla (refs = codes or numbers)."""
    code_of = {c["id"]: c["codigo"] for s in malla["semestres"] for c in s["cursos"]}
    sems = []
    for s in malla["semestres"]:
        cursos = []
        for c in s["cursos"]:
            ref = str(c["id"]) if by_number else c["codigo"]
            pre = [str(p) if by_number else code_of[p] for p in c["prerrequisitos"]]
            cursos.append(
                {
                    "ref": ref,
                    "codigo": None if by_number else c["codigo"],
                    "numero_en_documento": c["id"] if by_number else None,
                    "nombre": c["nombre"],
                    "creditos": c["sct"],
                    "prereq_estado": "conocido" if pre else "ninguno",
                    "prerrequisitos": pre,
                }
            )
        sems.append({"numero": s["numero"], "cursos": cursos})
    return {
        "carrera": malla["carrera"],
        "universidad": malla.get("universidad"),
        "total_creditos": malla.get("total_creditos"),
        "semestres": sems,
        "advertencias": [],
    }


class FakeClient:
    def __init__(self, output: dict[str, Any]) -> None:
        self.calls: list[dict[str, Any]] = []
        self._output = output
        self.messages = self

    def create(self, **kwargs: Any) -> Any:
        self.calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type="tool_use", name=TOOL_NAME, input=self._output)],
            usage=SimpleNamespace(input_tokens=1234, output_tokens=5678),
            stop_reason="tool_use",
        )


def test_extract_sends_the_document_and_forces_the_tool() -> None:
    client = FakeClient({"carrera": "X", "semestres": [], "advertencias": []})
    result = extract(b"%PDF-1.4 ...", "application/pdf", client=client, model="m")
    [call] = client.calls
    assert call["tool_choice"] == {"type": "tool", "name": TOOL_NAME}
    block = call["messages"][0]["content"][0]
    assert block["type"] == "document"
    assert block["source"]["media_type"] == "application/pdf"
    assert (result.input_tokens, result.output_tokens) == (1234, 5678)

    extract(b"\x89PNG", "image/png", client=client, model="m")
    assert client.calls[1]["messages"][0]["content"][0]["type"] == "image"


def test_media_types() -> None:
    assert media_type_for("Malla.PDF") == "application/pdf"
    assert media_type_for("foto.jpeg") == "image/jpeg"
    with pytest.raises(ValueError):
        media_type_for("malla.docx")


@pytest.mark.parametrize(("stem", "by_number"), [("QuimicaUCH", True), ("CInf", False)])
def test_a_perfect_extraction_scores_100(stem: str, by_number: bool) -> None:
    truth = verified(stem)
    draft = to_draft(as_model_output(truth, by_number=by_number))
    assert draft.malla["estado"] == "borrador"
    assert validate(draft.malla) == []
    m = compare(draft.malla, truth)
    assert m["cobertura_pct"] == 100.0
    assert m["ramos_inventados"] == 0
    assert m["semestre_correcto_pct"] == 100.0
    assert m["creditos_correctos_pct"] == 100.0
    assert m["prerrequisitos_correctos_pct"] == 100.0


def test_unreadable_or_dangling_requirements_become_unknown_never_none() -> None:
    out = {
        "carrera": "Prueba",
        "semestres": [
            {
                "numero": 1,
                "cursos": [
                    {"ref": "A1", "nombre": "A", "prereq_estado": "ninguno", "prerrequisitos": []}
                ],
            },
            {
                "numero": 2,
                "cursos": [
                    # points to a course that is not in the document
                    {
                        "ref": "B1",
                        "nombre": "B",
                        "prereq_estado": "conocido",
                        "prerrequisitos": ["ZZ99"],
                    },
                    # "known" but nothing listed: not trustworthy
                    {"ref": "B2", "nombre": "C", "prereq_estado": "conocido", "prerrequisitos": []},
                    {
                        "ref": "B3",
                        "nombre": "D",
                        "prereq_estado": "desconocido",
                        "prerrequisitos": ["A1"],
                    },
                ],
            },
        ],
        "advertencias": [],
    }
    draft = to_draft(out)
    status = {
        c["codigo"]: (c["prereq_status"], c["prerrequisitos"])
        for s in draft.malla["semestres"]
        for c in s["cursos"]
    }
    assert status == {
        "A1": ("none", []),
        "B1": ("unknown", []),
        "B2": ("unknown", []),
        "B3": ("unknown", []),
    }
    assert draft.unknown_courses == 3
    assert any("ZZ99" in w for w in draft.warnings)


def test_semesters_approved_means_every_earlier_course() -> None:
    out = {
        "carrera": "P",
        "semestres": [
            {
                "numero": 1,
                "cursos": [
                    {
                        "ref": "1",
                        "numero_en_documento": 1,
                        "nombre": "a",
                        "prereq_estado": "ninguno",
                        "prerrequisitos": [],
                    },
                    {
                        "ref": "2",
                        "numero_en_documento": 2,
                        "nombre": "b",
                        "prereq_estado": "ninguno",
                        "prerrequisitos": [],
                    },
                ],
            },
            {
                "numero": 2,
                "cursos": [
                    {
                        "ref": "3",
                        "numero_en_documento": 3,
                        "nombre": "práctica",
                        "prereq_estado": "conocido",
                        "prerrequisitos": [],
                        "semestres_aprobados_requeridos": 1,
                    },
                ],
            },
        ],
        "advertencias": [],
    }
    practica = to_draft(out).malla["semestres"][1]["cursos"][0]
    assert practica["prerrequisitos"] == [1, 2]
    assert practica["prereq_status"] == "known"


def test_comparison_counts_errors() -> None:
    truth = verified("QuimicaUCH")
    out = as_model_output(truth, by_number=True)
    bad = copy.deepcopy(out)
    first = bad["semestres"][0]["cursos"][0]
    first["creditos"] = (first["creditos"] or 0) + 1  # one credit wrong
    with_pre = next(c for s in bad["semestres"] for c in s["cursos"] if c["prerrequisitos"])
    with_pre["prereq_estado"] = "desconocido"  # one unknown
    bad["semestres"][0]["cursos"].append(  # one invented course
        {
            "ref": "999",
            "numero_en_documento": 999,
            "nombre": "Ramo inventado",
            "prereq_estado": "ninguno",
            "prerrequisitos": [],
        }
    )
    m = compare(to_draft(bad).malla, truth)
    assert m["ramos_inventados"] == 1
    assert m["prerrequisitos_desconocidos"] == 1
    assert m["creditos_correctos_pct"] < 100.0
    assert m["cobertura_pct"] == 100.0


def test_validate_flags_credit_total_mismatch() -> None:
    truth = verified("QuimicaUCH")
    out = as_model_output(truth, by_number=True)
    out["total_creditos"] = (out["total_creditos"] or 0) + 10
    assert any(i.startswith("creditos:") for i in validate(to_draft(out).malla))
