import json
import uuid
from pathlib import Path

import pytest
from httpx import AsyncClient
from pydantic import ValidationError
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import Course, CourseAlias, CurriculumVersion, Program, Track, University
from app.schemas.prereq import validate_prereq_tree
from app.services.career_key import career_key_from_url
from app.services.legacy_import import LEGACY_PROGRAMS, import_legacy_folder
from app.services.prerequisites import UnsupportedPrereqTree, and_tree, flatten_and_tree

MALLAS_DIR = Path(__file__).resolve().parents[2] / "frontend" / "public" / "mallas"

# getCareerId({url: "/mallas/<stem>.json"}) as produced by the frontend today (v1 included:
# the U. de Chile mallas are already public there at /mallas/<Name>UCH.json).
EXPECTED_CAREER_KEYS = {
    "Industrial": "unab-industrial",
    "Comp": "unab-comp",
    "Geo": "unab-geo",
    "MM": "unab-mm",
    "CInf": "unab-cinf",
    "Minas": "unab-minas",
    "Med": "unab-med",
    "TM": "unab-tm",
    "Psicologia": "unab-psicologia",
    "BioquimicaUCH": "unab-bioquimicauch",
    "IngenieriaAlimentosUCH": "unab-ingenieriaalimentosuch",
    "QuimicaUCH": "unab-quimicauch",
    "QuimicaFarmaciaUCH": "unab-quimicafarmaciauch",
}
UNAB_STEMS = ["Industrial", "Comp", "Geo", "MM", "CInf", "Minas", "Med", "TM", "Psicologia"]
UCH_STEMS = ["BioquimicaUCH", "IngenieriaAlimentosUCH", "QuimicaUCH", "QuimicaFarmaciaUCH"]


def load_json(stem: str) -> dict:
    return json.loads((MALLAS_DIR / f"{stem}.json").read_text(encoding="utf-8"))


def json_courses(data: dict) -> list[dict]:
    sections = list(data.get("semestres") or []) + list(data.get("semestres_comunes") or [])
    for mention in (data.get("menciones") or {}).values():
        sections += mention["semestres"]
    return [c for s in sections for c in s["cursos"]]


@pytest.fixture
async def imported(db_session: AsyncSession):
    return await import_legacy_folder(db_session, MALLAS_DIR)


async def _counts(db: AsyncSession) -> dict[str, int]:
    return {
        "programs": await db.scalar(select(func.count()).select_from(Program)),
        "versions": await db.scalar(select(func.count()).select_from(CurriculumVersion)),
        "tracks": await db.scalar(select(func.count()).select_from(Track)),
        "courses": await db.scalar(select(func.count()).select_from(Course)),
    }


# ---------------------------------------------------------------- import


async def test_course_counts_match_json(imported, db_session: AsyncSession) -> None:
    assert len(imported.results) == len(LEGACY_PROGRAMS) == 13
    for stem, slug, _name, _uni in LEGACY_PROGRAMS:
        expected = len({c["id"] for c in json_courses(load_json(stem))})
        program = await db_session.scalar(select(Program).where(Program.slug == slug))
        count = await db_session.scalar(
            select(func.count())
            .select_from(Course)
            .join(CurriculumVersion, CurriculumVersion.id == Course.version_id)
            .where(CurriculumVersion.program_id == program.id)
        )
        assert count == expected, stem


async def test_import_is_idempotent(db_session: AsyncSession) -> None:
    await import_legacy_folder(db_session, MALLAS_DIR)
    first = await _counts(db_session)
    second_report = await import_legacy_folder(db_session, MALLAS_DIR)
    assert await _counts(db_session) == first
    assert first == {"programs": 13, "versions": 13, "tracks": 7, "courses": 837}
    assert all(r.created_courses == 0 and not r.created_program for r in second_report.results)


async def test_versions_are_legacy_published_current(imported, db_session: AsyncSession) -> None:
    versions = (await db_session.scalars(select(CurriculumVersion))).all()
    assert len(versions) == 13
    for v in versions:
        assert (v.label, v.status, v.is_current, v.source_type) == (
            "legacy",
            "published",
            True,
            "legacy_json",
        )


async def test_prerequisites_reproduce_frontend_semantics(
    imported, db_session: AsyncSession
) -> None:
    for stem, slug, _, _ in LEGACY_PROGRAMS:
        raw_by_id = {c["id"]: c for c in json_courses(load_json(stem))}
        rows = (
            await db_session.scalars(
                select(Course)
                .join(CurriculumVersion, CurriculumVersion.id == Course.version_id)
                .join(Program, Program.id == CurriculumVersion.program_id)
                .where(Program.slug == slug)
            )
        ).all()
        legacy_by_uuid = {c.id: c.legacy_id for c in rows}
        for course in rows:
            raw = raw_by_id[course.legacy_id]
            ids = [legacy_by_uuid[u] for u in flatten_and_tree(course.prereq_expr)]
            assert ids == raw["prerrequisitos"], (stem, course.legacy_id)
            assert course.prereq_status == ("known" if raw["prerrequisitos"] else "none")
            assert course.prereq_raw == raw.get("prereq_expr")
            co = [legacy_by_uuid[u] for u in flatten_and_tree(course.coreq_expr)]
            assert co == (raw.get("correquisitos") or [])


async def test_one_current_version_per_program(imported, db_session: AsyncSession) -> None:
    program = await db_session.scalar(select(Program).limit(1))
    db_session.add(
        CurriculumVersion(
            program_id=program.id,
            label="second",
            period_regime="semestral",
            credit_system="SCT",
            total_periods=10,
            status="published",
            is_current=True,
            source_type="manual",
        )
    )
    with pytest.raises(IntegrityError):
        await db_session.flush()
    await db_session.rollback()


def test_career_key_matches_get_career_id_for_all_legacy_mallas() -> None:
    assert {p.stem: career_key_from_url(f"/mallas/{p.stem}.json") for p in LEGACY_PROGRAMS} == (
        EXPECTED_CAREER_KEYS
    )
    # Other universities keep the folder segment, like getCareerId.
    assert career_key_from_url("/mallas/uch/Medicina.json") == "uch-medicina"


# ---------------------------------------------------------------- prerequisite tree


def test_and_tree_conversion() -> None:
    a, b, c = uuid.uuid4(), uuid.uuid4(), uuid.uuid4()
    assert and_tree([]) is None
    assert and_tree([a]) == {"course": str(a)}
    tree = and_tree([a, b, c])
    assert tree == {"op": "and", "items": [{"course": str(x)} for x in (a, b, c)]}
    assert flatten_and_tree(tree) == [a, b, c]
    assert flatten_and_tree(None) == []


def test_flatten_rejects_or_and_min_credits() -> None:
    a = str(uuid.uuid4())
    with pytest.raises(UnsupportedPrereqTree):
        flatten_and_tree({"op": "or", "items": [{"course": a}, {"course": a}]})
    with pytest.raises(UnsupportedPrereqTree):
        flatten_and_tree({"min_credits": 120})


def test_tree_validation_accepts_the_three_node_types() -> None:
    a, b = str(uuid.uuid4()), str(uuid.uuid4())
    tree = {
        "op": "and",
        "items": [
            {"course": a},
            {"op": "or", "items": [{"course": b}, {"min_credits": 120}]},
        ],
    }
    assert validate_prereq_tree(tree) == tree


@pytest.mark.parametrize(
    "bad",
    [
        {"op": "xor", "items": [{"course": str(uuid.uuid4())}]},
        {"op": "and", "items": []},
        {"min_credits": 0},
        {"course": "not-a-uuid"},
        {"course": str(uuid.uuid4()), "op": "and"},
        {"unknown": 1},
        {"op": "and", "items": [{"nope": True}]},
    ],
)
def test_tree_validation_rejects_other_shapes(bad: dict) -> None:
    with pytest.raises(ValidationError):
        validate_prereq_tree(bad)


# ---------------------------------------------------------------- API


async def test_universities_endpoint(client: AsyncClient, imported) -> None:
    response = await client.get("/api/v1/universities")
    assert response.status_code == 200
    assert response.headers["cache-control"] == "public, max-age=300"
    body = response.json()
    assert [(u["slug"], u["short_name"], u["country"]) for u in body] == [
        ("unab", "UNAB", "CL"),
        ("uch", "UCH", "CL"),
    ]


async def test_programs_endpoint_keeps_legacy_order(client: AsyncClient, imported) -> None:
    response = await client.get("/api/v1/universities/unab/programs")
    assert response.status_code == 200
    programs = response.json()
    assert [p["legacy_url"] for p in programs] == [f"/mallas/{s}.json" for s in UNAB_STEMS]
    assert {p["career_key"] for p in programs} == {EXPECTED_CAREER_KEYS[s] for s in UNAB_STEMS}
    assert (await client.get("/api/v1/universities/nope/programs")).status_code == 404


async def _program_id(client: AsyncClient, legacy_url: str) -> str:
    programs = (await client.get("/api/v1/universities/unab/programs")).json()
    return next(p["id"] for p in programs if p["legacy_url"] == legacy_url)


async def test_curriculum_endpoint_medicina(client: AsyncClient, imported) -> None:
    program_id = await _program_id(client, "/mallas/Med.json")
    response = await client.get(f"/api/v1/programs/{program_id}/curriculum")
    assert response.status_code == 200
    assert response.headers["cache-control"] == "public, max-age=300"
    body = response.json()
    assert body["program"]["career_key"] == "unab-med"
    assert body["version"]["label"] == "legacy"
    assert len(body["courses"]) == 54
    assert body["tracks"] == []
    legacy_ids = sorted(c["legacy_id"] for c in body["courses"])
    assert legacy_ids == list(range(1, 55))
    biol = next(c for c in body["courses"] if c["code"] == "BIOL148")
    assert biol["prereq_status"] == "known"
    assert biol["prereq_raw"] == "BIOL132 o ( BIO130 y BIO131 )"
    assert biol["prereq_expr"] is not None
    assert next(c for c in body["courses"] if c["code"] == "BIOL132")["prereq_status"] == "none"


async def test_curriculum_endpoint_tecnologia_medica_has_tracks(
    client: AsyncClient, imported
) -> None:
    program_id = await _program_id(client, "/mallas/TM.json")
    body = (await client.get(f"/api/v1/programs/{program_id}/curriculum")).json()
    assert len(body["courses"]) == 165
    assert [t["code"] for t in body["tracks"]] == [
        "BACIMET",
        "IFIME",
        "MORFO",
        "OFTA",
        "OTORRINO",
    ]
    assert {c["track_code"] for c in body["courses"]} == {
        None,
        *[t["code"] for t in body["tracks"]],
    }
    common = [p for p in body["periods"] if p["track_code"] is None]
    assert [p["number"] for p in common] == [1, 2, 3]


async def test_curriculum_unknown_program_returns_404(client: AsyncClient, imported) -> None:
    response = await client.get(f"/api/v1/programs/{uuid.uuid4()}/curriculum")
    assert response.status_code == 404
    assert (await client.get("/api/v1/programs/not-a-uuid/curriculum")).status_code == 422


# ---------------------------------------------------------------- T-010: verified mallas, UCH


async def _version_for(db: AsyncSession, stem: str) -> CurriculumVersion:
    return await db.scalar(
        select(CurriculumVersion)
        .join(Program, Program.id == CurriculumVersion.program_id)
        .where(Program.legacy_url == f"/mallas/{stem}.json")
    )


async def test_uch_programs_belong_to_their_own_university(
    imported, db_session: AsyncSession
) -> None:
    uch = await db_session.scalar(select(University).where(University.slug == "uch"))
    assert (uch.name, uch.short_name) == ("Universidad de Chile", "UCH")
    for stem in UCH_STEMS:
        program = await db_session.scalar(
            select(Program).where(Program.legacy_url == f"/mallas/{stem}.json")
        )
        assert program.university_id == uch.id, stem
        assert program.career_key == EXPECTED_CAREER_KEYS[stem]
        assert load_json(stem)["universidad"] == "Universidad de Chile"
    unab = await db_session.scalar(select(University).where(University.slug == "unab"))
    unab_programs = (
        await db_session.scalars(select(Program).where(Program.university_id == unab.id))
    ).all()
    assert {p.legacy_url for p in unab_programs} == {f"/mallas/{s}.json" for s in UNAB_STEMS}


async def test_programs_endpoint_lists_uch_in_order(client: AsyncClient, imported) -> None:
    programs = (await client.get("/api/v1/universities/uch/programs")).json()
    assert [(p["name"], p["legacy_url"], p["career_key"]) for p in programs] == [
        ("Bioquímica", "/mallas/BioquimicaUCH.json", "unab-bioquimicauch"),
        (
            "Ingeniería en Alimentos",
            "/mallas/IngenieriaAlimentosUCH.json",
            "unab-ingenieriaalimentosuch",
        ),
        ("Química", "/mallas/QuimicaUCH.json", "unab-quimicauch"),
        ("Química y Farmacia", "/mallas/QuimicaFarmaciaUCH.json", "unab-quimicafarmaciauch"),
    ]


async def test_new_top_level_fields_are_kept_verbatim(imported, db_session: AsyncSession) -> None:
    """universidad, fuente_oficial, nota_codigos and equivalencias: nothing is lost."""
    for stem in UNAB_STEMS + UCH_STEMS:
        data = load_json(stem)
        version = await _version_for(db_session, stem)
        for key in ("universidad", "fuente_oficial", "nota_codigos", "equivalencias"):
            if key in data:
                assert version.attrs[key] == data[key], (stem, key)
            else:
                assert key not in version.attrs, (stem, key)

    cinf = await _version_for(db_session, "CInf")
    assert cinf.source_type == "legacy_json"
    assert cinf.source_note == (
        "Imported from frontend/public/mallas/CInf.json. Checked against the official "
        "curriculum: program UNAB12210 catalog 202010 (PRIMER SEMESTRE 2020) reading: OCR revisado"
    )
    quimica = await _version_for(db_session, "QuimicaUCH")
    assert quimica.source_note == (
        "Imported from frontend/public/mallas/QuimicaUCH.json. "
        "Not checked against an official document"
    )
    assert "fuente_oficial" not in quimica.attrs
    bq = await _version_for(db_session, "BioquimicaUCH")
    assert bq.source_note == (
        "Imported from frontend/public/mallas/BioquimicaUCH.json. Checked against the official "
        "curriculum: document 'MALLA BQ - corregido (1).pdf' reading: revisión visual ramo por "
        "ramo on 2026-10-29"
    )
    assert "códigos internos" in quimica.attrs["nota_codigos"]


async def test_equivalencias_do_not_create_aliases(imported, db_session: AsyncSession) -> None:
    """Old-plan equivalences are not code aliases: they stay in attrs, so the schedule import
    (which matches by courseCodeAliases) behaves the same with and without the API."""
    assert await db_session.scalar(select(func.count()).select_from(CourseAlias)) == 0


async def test_area_and_linea_are_kept_in_course_attrs(imported, db_session: AsyncSession) -> None:
    for stem in ["Industrial", *UCH_STEMS]:
        raw_by_id = {c["id"]: c for c in json_courses(load_json(stem))}
        version = await _version_for(db_session, stem)
        rows = (
            await db_session.scalars(select(Course).where(Course.version_id == version.id))
        ).all()
        for course in rows:
            raw = raw_by_id[course.legacy_id]
            for key in ("area", "linea"):
                assert course.attrs.get(key) == raw.get(key), (stem, course.legacy_id, key)


async def test_new_fields_are_not_reported_as_unmodeled(imported) -> None:
    assert [i for i in imported.inconsistencies if i.kind == "campo_no_modelado"] == []
    assert [i for i in imported.inconsistencies if i.kind == "equivalencia_sin_curso"] == []


async def test_declared_university_must_match_registry(
    db_session: AsyncSession, tmp_path: Path
) -> None:
    for stem in [p.stem for p in LEGACY_PROGRAMS]:
        data = load_json(stem)
        if stem == "QuimicaUCH":
            data["universidad"] = "Universidad Andrés Bello"
        (tmp_path / f"{stem}.json").write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="QuimicaUCH"):
        await import_legacy_folder(db_session, tmp_path)
    await db_session.rollback()


async def test_cinf_keeps_ids_with_new_codes(imported, db_session: AsyncSession) -> None:
    """ICF/INSW -> CINF renames keep each legacy id, so progress saved by id survives."""
    renamed = {17: "CINF100", 22: "CINF102", 23: "CINF101", 39: "CINF200", 48: "CINF300"}
    version = await _version_for(db_session, "CInf")
    rows = (await db_session.scalars(select(Course).where(Course.version_id == version.id))).all()
    by_id = {c.legacy_id: c.code for c in rows}
    assert sorted(by_id) == list(range(1, 49))
    for legacy_id, code in renamed.items():
        assert by_id[legacy_id] == code


async def test_unknown_top_level_key_is_kept_and_reported(
    db_session: AsyncSession, tmp_path: Path
) -> None:
    """Any top-level key with no column lands in version.attrs and in the report."""
    for stem in [p.stem for p in LEGACY_PROGRAMS]:
        data = load_json(stem)
        if stem == "Geo":
            data["campo_inventado"] = {"x": [1, 2]}
        (tmp_path / f"{stem}.json").write_text(json.dumps(data), encoding="utf-8")
    report = await import_legacy_folder(db_session, tmp_path)
    version = await _version_for(db_session, "Geo")
    assert version.attrs["campo_inventado"] == {"x": [1, 2]}
    assert version.attrs["fuente_oficial"] == load_json("Geo")["fuente_oficial"]
    unmodeled = [i for i in report.inconsistencies if i.kind == "campo_no_modelado"]
    assert [(i.malla, i.detail) for i in unmodeled] == [
        ("Geología", "clave de primer nivel `campo_inventado`")
    ]


async def test_every_malla_states_whether_it_was_verified(
    imported, db_session: AsyncSession
) -> None:
    """CA-01: the catalog tells verified mallas from the ones never checked (only QuimicaUCH)."""
    unverified = []
    for p in LEGACY_PROGRAMS:
        version = await _version_for(db_session, p.stem)
        if "fuente_oficial" in version.attrs:
            assert "Checked against the official curriculum" in version.source_note
        else:
            assert version.source_note.endswith("Not checked against an official document")
            unverified.append(p.stem)
    assert unverified == ["QuimicaUCH"]
