"""Import the legacy frontend/public/mallas/*.json files into the catalog tables.

Semantics reproduced from the frontend: only `prerrequisitos` (a list of course ids, AND) is
enforced. `prereq_expr` text is kept verbatim in prereq_raw; nothing is "fixed" silently, every
oddity found is returned as an Inconsistency.
"""

import json
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, NamedTuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.catalog import (
    Course,
    CourseAlias,
    CurriculumVersion,
    Program,
    Track,
    University,
)
from app.services.career_key import career_key_from_url
from app.services.prerequisites import and_tree

UNIVERSITIES: dict[str, dict[str, str]] = {
    "unab": {"slug": "unab", "name": "Universidad Andrés Bello", "short_name": "UNAB"},
    "uch": {"slug": "uch", "name": "Universidad de Chile", "short_name": "UCH"},
}


class LegacyProgram(NamedTuple):
    stem: str  # file name without .json inside frontend/public/mallas/
    slug: str  # program slug, unique within its university
    name: str  # listing name, as in the static mallasLoader listing
    university: str  # key of UNIVERSITIES


# Order and names match the static mallasLoader listing exactly so the UI looks the same.
# The U. de Chile files live at /mallas/<Name>UCH.json because that is where the public
# version (v1) serves them: their career_key ("unab-...uch") is what users' saved progress
# is keyed on, so it must stay as is even though the prefix says "unab" (ADR-0007).
LEGACY_PROGRAMS: list[LegacyProgram] = [
    LegacyProgram(
        "Industrial", "ingenieria-civil-industrial", "Ingeniería Civil Industrial", "unab"
    ),
    LegacyProgram(
        "Comp",
        "ingenieria-computacion-informatica",
        "Ingeniería en Computación e Informática",
        "unab",
    ),
    LegacyProgram("Geo", "geologia", "Geología", "unab"),
    LegacyProgram("MM", "ingenieria-marina-mercante", "Ingeniería en Marina Mercante", "unab"),
    LegacyProgram("CInf", "ingenieria-civil-informatica", "Ingeniería Civil Informática", "unab"),
    LegacyProgram("Minas", "ingenieria-civil-minas", "Ingeniería Civil en Minas", "unab"),
    LegacyProgram("Med", "medicina", "Medicina", "unab"),
    LegacyProgram("TM", "tecnologia-medica", "Tecnología Médica", "unab"),
    LegacyProgram("Psicologia", "psicologia", "Psicología", "unab"),
    LegacyProgram("BioquimicaUCH", "bioquimica", "Bioquímica", "uch"),
    LegacyProgram(
        "IngenieriaAlimentosUCH", "ingenieria-alimentos", "Ingeniería en Alimentos", "uch"
    ),
    LegacyProgram("QuimicaUCH", "quimica", "Química", "uch"),
    LegacyProgram("QuimicaFarmaciaUCH", "quimica-farmacia", "Química y Farmacia", "uch"),
]

VERSION_LABEL = "legacy"
KNOWN_TOP_KEYS = {
    "carrera",
    "codigo_programa",
    "total_creditos",
    "total_creditos_por_mencion",
    "totalSemestres",
    "semestres",
    "semestres_comunes",
    "menciones",
    "menciones_disponibles",
    "courseCodeAliases",
    "course_code_aliases",
    # Kept verbatim in curriculum_versions.attrs (VERSION_ATTR_KEYS):
    "universidad",
    "fuente_oficial",
    "nota_codigos",
    "equivalencias",
}
# Top-level keys copied as they are into curriculum_versions.attrs. Any other unknown
# top-level key is copied too, and reported as campo_no_modelado.
VERSION_ATTR_KEYS = ("universidad", "fuente_oficial", "nota_codigos", "equivalencias")
# Course keys with no column that are expected: kept in courses.attrs without a report line.
COURSE_ATTR_KEYS = {"area", "linea"}
KNOWN_COURSE_KEYS = {
    "id",
    "codigo",
    "nombre",
    "sct",
    "prerrequisitos",
    "prereq_expr",
    "correquisitos",
    "correq_expr",
}
CODE_RE = re.compile(r"[A-Z]{2,6}\d{2,4}[A-Z]?")
ALT_RE = re.compile(r"\bo\b|equivalente", re.IGNORECASE)

KIND_TITLES = {
    "id_duplicado": "Id de curso repetido (se ignora la segunda aparición)",
    "id_inexistente": "Prerrequisito apunta a un id que no existe",
    "autorreferencia": "Curso es prerrequisito de sí mismo",
    "ciclo": "Ciclo de prerrequisitos",
    "prereq_fuera_del_alcance": "Prerrequisito de otra mención",
    "prereq_mismo_periodo_o_posterior": "Prerrequisito en el mismo período o uno posterior",
    "texto_distinto_de_ids": "El texto prereq_expr no coincide con los ids de prerrequisitos",
    "ids_sin_texto": "Tiene ids de prerrequisitos pero prereq_expr vacío o ausente",
    "texto_sin_ids": "Tiene texto en prereq_expr pero ningún id de prerrequisito",
    "correq_texto_distinto_de_ids": "El texto correq_expr no coincide con los ids de correquisitos",
    "alternativas_ignoradas": (
        'prereq_expr menciona alternativas ("o"/equivalentes); solo se aplican los ids'
    ),
    "codigo_repetido": "Mismo código con ids distintos (una copia por mención)",
    "campo_no_modelado": "Campo del JSON que el modelo no representa (se conserva en attrs)",
    "equivalencia_sin_curso": "Equivalencia declarada para un código que no está en la malla",
    "creditos_totales_cero": "total_creditos = 0 (se interpreta como desconocido)",
}


@dataclass
class Inconsistency:
    malla: str
    kind: str
    detail: str
    course_code: str | None = None
    course_name: str | None = None
    legacy_id: int | None = None
    period: int | None = None
    track: str | None = None


@dataclass
class MallaResult:
    stem: str
    program_name: str
    career_key: str
    courses: int = 0
    tracks: int = 0
    aliases: int = 0
    created_courses: int = 0
    created_program: bool = False


@dataclass
class ImportReport:
    results: list[MallaResult] = field(default_factory=list)
    inconsistencies: list[Inconsistency] = field(default_factory=list)


@dataclass
class _Entry:
    track_code: str | None
    period: int
    order: int
    raw: dict[str, Any]


def _collect_entries(data: dict[str, Any]) -> list[_Entry]:
    entries: list[_Entry] = []
    order = 0
    sections: list[tuple[str | None, list[dict[str, Any]]]] = [
        (None, data.get("semestres") or []),
        (None, data.get("semestres_comunes") or []),
    ]
    for code, mention in (data.get("menciones") or {}).items():
        sections.append((code, mention.get("semestres") or []))
    for track_code, semesters in sections:
        for sem in semesters:
            for raw in sem.get("cursos") or []:
                entries.append(_Entry(track_code, int(sem["numero"]), order, raw))
                order += 1
    return entries


def _codes(text: str | None) -> set[str]:
    return set(CODE_RE.findall(text or ""))


def _detect(
    stem: str, name: str, data: dict[str, Any], entries: list[_Entry]
) -> list[Inconsistency]:
    found: list[Inconsistency] = []

    def add(kind: str, detail: str, e: _Entry | None = None, **kw: Any) -> None:
        found.append(
            Inconsistency(
                malla=name,
                kind=kind,
                detail=detail,
                course_code=e.raw.get("codigo") if e else None,
                course_name=e.raw.get("nombre") if e else None,
                legacy_id=e.raw.get("id") if e else None,
                period=e.period if e else None,
                track=e.track_code if e else None,
                **kw,
            )
        )

    for key in sorted(set(data) - KNOWN_TOP_KEYS):
        add("campo_no_modelado", f"clave de primer nivel `{key}`")
    if data.get("total_creditos") == 0:
        add("creditos_totales_cero", "total_creditos = 0")

    by_id: dict[int, _Entry] = {}
    for e in entries:
        cid = e.raw["id"]
        if cid in by_id:
            add("id_duplicado", f"id {cid} aparece más de una vez", e)
            continue
        by_id[cid] = e

    malla_codes = {e.raw.get("codigo") for e in by_id.values()}
    code_to_ids: dict[str, set[int]] = defaultdict(set)
    for e in by_id.values():
        code_to_ids[e.raw.get("codigo")].add(e.raw["id"])

    for e in by_id.values():
        raw = e.raw
        for key in sorted(set(raw) - KNOWN_COURSE_KEYS - COURSE_ATTR_KEYS):
            add("campo_no_modelado", f"campo de curso `{key}` = {raw[key]!r}", e)

        pre = raw.get("prerrequisitos") or []
        expr = raw.get("prereq_expr")
        id_codes: set[str] = set()
        for p in pre:
            target = by_id.get(p)
            if target is None:
                add("id_inexistente", f"prerrequisito id {p}", e)
                continue
            id_codes.add(target.raw.get("codigo"))
            if p == raw["id"]:
                add("autorreferencia", f"id {p}", e)
            elif target.track_code not in (None, e.track_code):
                add(
                    "prereq_fuera_del_alcance",
                    f"{target.raw.get('codigo')} (id {p}) es de la mención {target.track_code}",
                    e,
                )
            elif target.period >= e.period:
                add(
                    "prereq_mismo_periodo_o_posterior",
                    f"{target.raw.get('codigo')} {target.raw.get('nombre')} (id {p}) "
                    f"está en el período {target.period}",
                    e,
                )

        text = expr if isinstance(expr, str) else ""
        if pre and not text.strip():
            add("ids_sin_texto", "ids: " + ", ".join(sorted(c for c in id_codes if c)), e)
        elif text.strip() and not pre:
            add("texto_sin_ids", f"texto: {text!r}", e)
        elif text.strip():
            t = _codes(text)
            extra = sorted((t & malla_codes) - id_codes)
            missing = sorted(id_codes - t)
            if extra or missing:
                add(
                    "texto_distinto_de_ids",
                    f"texto: {text!r}; ids: {sorted(id_codes)}"
                    + (f"; en el texto y no en ids: {extra}" if extra else "")
                    + (f"; en ids y no en el texto: {missing}" if missing else ""),
                    e,
                )
            elif ALT_RE.search(text):
                add("alternativas_ignoradas", f"texto: {text!r}; ids: {sorted(id_codes)}", e)

        coreq = raw.get("correquisitos") or []
        ctext = raw.get("correq_expr") if isinstance(raw.get("correq_expr"), str) else ""
        if coreq and ctext.strip():
            co_codes = {by_id[c].raw.get("codigo") for c in coreq if c in by_id}
            if _codes(ctext) != co_codes:
                add(
                    "correq_texto_distinto_de_ids",
                    f"texto: {ctext!r}; ids: {sorted(co_codes)}",
                    e,
                )

    for code in sorted((data.get("equivalencias") or {}).keys() - malla_codes):
        add("equivalencia_sin_curso", f"`{code}` tiene equivalencias pero no está en la malla")

    for code, ids in sorted(code_to_ids.items(), key=lambda kv: str(kv[0])):
        if len(ids) > 1:
            where = ", ".join(f"{i} ({by_id[i].track_code or 'común'})" for i in sorted(ids))
            found.append(
                Inconsistency(
                    malla=name,
                    kind="codigo_repetido",
                    detail=f"ids: {where}",
                    course_code=code,
                    course_name=by_id[min(ids)].raw.get("nombre"),
                )
            )

    # Cycles over the AND graph (per track scope, ids are unique per malla).
    graph = {
        cid: [p for p in (e.raw.get("prerrequisitos") or []) if p in by_id and p != cid]
        for cid, e in by_id.items()
    }
    state: dict[int, int] = {}

    def dfs(node: int, stack: list[int]) -> None:
        state[node] = 1
        for nxt in graph[node]:
            if state.get(nxt) == 1:
                cycle = stack[stack.index(nxt) :] + [node, nxt] if nxt in stack else [node, nxt]
                e = by_id[node]
                add("ciclo", " -> ".join(str(c) for c in cycle), e)
            elif nxt not in state:
                dfs(nxt, stack + [node])
        state[node] = 2

    for cid in graph:
        if cid not in state:
            dfs(cid, [])
    return found


async def _get_or_create_university(session: AsyncSession, key: str) -> University:
    info = UNIVERSITIES[key]
    uni = await session.scalar(select(University).where(University.slug == info["slug"]))
    if uni is None:
        uni = University(country="CL", **info)
        session.add(uni)
    else:
        uni.name = info["name"]
        uni.short_name = info["short_name"]
    await session.flush()
    return uni


def _version_attrs(data: dict[str, Any]) -> dict[str, Any]:
    """Top-level fields with no column, verbatim, so nothing in the file is lost."""
    keys = [k for k in VERSION_ATTR_KEYS if k in data]
    keys += sorted(set(data) - KNOWN_TOP_KEYS)
    return {k: data[k] for k in keys}


def _source_note(stem: str, data: dict[str, Any]) -> str:
    note = f"Imported from frontend/public/mallas/{stem}.json"
    source = data.get("fuente_oficial")
    if isinstance(source, dict) and source:
        parts = [
            f"program {source['programa']}" if source.get("programa") else None,
            f"catalog {source['catalogo']}" if source.get("catalogo") else None,
            f"({source['catalogoTexto']})" if source.get("catalogoTexto") else None,
            f"reading: {source['lectura']}" if source.get("lectura") else None,
        ]
        note += ". Checked against the official curriculum: " + " ".join(p for p in parts if p)
    return note


async def _import_one(
    session: AsyncSession,
    uni: University,
    sort_index: int,
    entry: LegacyProgram,
    data: dict[str, Any],
) -> tuple[MallaResult, list[Inconsistency]]:
    stem, slug, list_name = entry.stem, entry.slug, entry.name
    declared = data.get("universidad")
    if declared is not None and declared != uni.name:
        raise ValueError(
            f"{stem}.json declares universidad={declared!r} but is registered under {uni.name!r}"
        )
    legacy_url = f"/mallas/{stem}.json"
    career_key = career_key_from_url(legacy_url)
    entries = _collect_entries(data)
    inconsistencies = _detect(stem, list_name, data, entries)

    program = await session.scalar(
        select(Program).where(Program.university_id == uni.id, Program.slug == slug)
    )
    result = MallaResult(stem=stem, program_name=list_name, career_key=career_key)
    if program is None:
        program = Program(university_id=uni.id, slug=slug, name=list_name, career_key=career_key)
        session.add(program)
        result.created_program = True
    program.name = list_name
    program.official_name = data.get("carrera")
    program.official_code = data.get("codigo_programa")
    program.career_key = career_key
    program.legacy_url = legacy_url
    program.sort_order = sort_index
    await session.flush()

    version = await session.scalar(
        select(CurriculumVersion).where(
            CurriculumVersion.program_id == program.id, CurriculumVersion.label == VERSION_LABEL
        )
    )
    if version is None:
        version = CurriculumVersion(program_id=program.id, label=VERSION_LABEL)
        session.add(version)
    total_periods = data.get("totalSemestres") or len(data.get("semestres") or [])
    total_credits = data.get("total_creditos") or None
    version.period_regime = "semestral"
    version.credit_system = "SCT"
    version.total_periods = int(total_periods)
    version.total_credits = int(total_credits) if total_credits else None
    version.status = "published"
    version.is_current = True
    version.source_type = "legacy_json"
    version.source_url = legacy_url
    version.source_note = _source_note(stem, data)
    version.attrs = _version_attrs(data)
    await session.flush()

    # Tracks (menciones)
    tracks: dict[str, Track] = {}
    existing_tracks = {
        t.code: t
        for t in (await session.scalars(select(Track).where(Track.version_id == version.id))).all()
    }
    credits_by_track = data.get("total_creditos_por_mencion") or {}
    names = {m["codigo"]: m.get("nombre") for m in data.get("menciones_disponibles") or []}
    order = [m["codigo"] for m in data.get("menciones_disponibles") or []]
    order += [c for c in (data.get("menciones") or {}) if c not in order]
    for idx, code in enumerate(order):
        mention = (data.get("menciones") or {}).get(code, {})
        track = existing_tracks.get(code)
        if track is None:
            track = Track(version_id=version.id, code=code, slug=code.lower())
            session.add(track)
        track.name = names.get(code) or mention.get("nombre") or code
        track.total_credits = credits_by_track.get(code)
        track.sort_order = idx
        tracks[code] = track
    await session.flush()

    # Courses (first pass: rows without prerequisites, so every uuid exists)
    existing = {
        c.legacy_id: c
        for c in (
            await session.scalars(select(Course).where(Course.version_id == version.id))
        ).all()
    }
    courses: dict[int, Course] = {}
    for e in entries:
        raw = e.raw
        legacy_id = raw["id"]
        if legacy_id in courses:
            continue
        course = existing.get(legacy_id)
        if course is None:
            course = Course(version_id=version.id, legacy_id=legacy_id, prereq_status="none")
            session.add(course)
            result.created_courses += 1
        course.track_id = tracks[e.track_code].id if e.track_code else None
        course.period_number = e.period
        course.sort_order = e.order
        course.code = raw.get("codigo")
        course.name = raw.get("nombre")
        course.credits = raw.get("sct")
        course.prereq_raw = raw.get("prereq_expr") if "prereq_expr" in raw else None
        course.coreq_raw = raw.get("correq_expr") if "correq_expr" in raw else None
        course.attrs = {k: v for k, v in raw.items() if k not in KNOWN_COURSE_KEYS}
        courses[legacy_id] = course
    await session.flush()

    # Second pass: prerequisite trees, in the original id order.
    for legacy_id, course in courses.items():
        raw = next(e.raw for e in entries if e.raw["id"] == legacy_id)
        pre_ids = [courses[p].id for p in (raw.get("prerrequisitos") or []) if p in courses]
        co_ids = [courses[p].id for p in (raw.get("correquisitos") or []) if p in courses]
        course.prereq_expr = and_tree(pre_ids)
        course.prereq_status = "known" if pre_ids else "none"
        course.coreq_expr = and_tree(co_ids)
    await session.flush()

    # Aliases: {mallaCode: [pdfCode, ...]}
    alias_map = data.get("courseCodeAliases") or data.get("course_code_aliases") or {}
    by_code: dict[str, list[Course]] = defaultdict(list)
    for course in courses.values():
        by_code[course.code].append(course)
    existing_aliases = {
        (a.alias_code, a.course_id)
        for a in (
            await session.scalars(select(CourseAlias).where(CourseAlias.version_id == version.id))
        ).all()
    }
    for malla_code, alias_codes in alias_map.items():
        for target in by_code.get(malla_code, []):
            for alias in alias_codes or []:
                if (alias, target.id) not in existing_aliases:
                    session.add(
                        CourseAlias(version_id=version.id, alias_code=alias, course_id=target.id)
                    )
                    existing_aliases.add((alias, target.id))
                    result.aliases += 1

    result.courses = len(courses)
    result.tracks = len(tracks)
    return result, inconsistencies


async def import_legacy_folder(session: AsyncSession, folder: Path) -> ImportReport:
    report = ImportReport()
    universities: dict[str, University] = {}
    sort_index: dict[str, int] = defaultdict(int)
    for entry in LEGACY_PROGRAMS:
        path = folder / f"{entry.stem}.json"
        if not path.exists():
            raise FileNotFoundError(f"Missing legacy malla file: {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        if entry.university not in universities:
            universities[entry.university] = await _get_or_create_university(
                session, entry.university
            )
        index = sort_index[entry.university]
        sort_index[entry.university] += 1
        result, issues = await _import_one(
            session, universities[entry.university], index, entry, data
        )
        report.results.append(result)
        report.inconsistencies.extend(issues)
    await session.commit()
    return report


def render_report_markdown(report: ImportReport) -> str:
    """Deterministic Markdown (no timestamps) so re-runs produce an identical file."""
    lines = [
        "# Inconsistencias en las mallas legadas",
        "",
        "Generado por `uv run python -m app.scripts.import_legacy_mallas`. Los datos se importaron",
        "tal cual (es el comportamiento actual de la app); este archivo es para revisarlos",
        "contra las mallas oficiales. No se corrigió nada.",
        "",
        "## Resumen",
        "",
        "| Malla | " + " | ".join(KIND_TITLES) + " |",
        "|---|" + "---|" * len(KIND_TITLES),
    ]
    names = [r.program_name for r in report.results]
    for name in names:
        counts = defaultdict(int)
        for i in report.inconsistencies:
            if i.malla == name:
                counts[i.kind] += 1
        lines.append(f"| {name} | " + " | ".join(str(counts[k]) for k in KIND_TITLES) + " |")
    lines += [
        "",
        "Leyenda de columnas: " + "; ".join(f"`{k}` = {v}" for k, v in KIND_TITLES.items()),
        "",
    ]

    for name in names:
        items = [i for i in report.inconsistencies if i.malla == name]
        lines += [f"## {name}", ""]
        if not items:
            lines += ["Sin inconsistencias.", ""]
            continue
        for kind, title in KIND_TITLES.items():
            group = sorted(
                (i for i in items if i.kind == kind),
                key=lambda i: (i.track or "", i.period or 0, i.legacy_id or 0),
            )
            if not group:
                continue
            lines += [f"### {title} ({len(group)})", ""]
            for i in group:
                who = " ".join(
                    p for p in (i.course_code, f"— {i.course_name}" if i.course_name else None) if p
                )
                where = []
                if i.legacy_id is not None:
                    where.append(f"id {i.legacy_id}")
                if i.period is not None:
                    where.append(f"período {i.period}")
                if i.track:
                    where.append(f"mención {i.track}")
                prefix = f"- **{who}**" if who else "-"
                suffix = f" ({', '.join(where)})" if where else ""
                lines.append(f"{prefix}{suffix}: {i.detail}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def new_uuid() -> uuid.UUID:  # pragma: no cover - helper kept for scripts
    return uuid.uuid4()
