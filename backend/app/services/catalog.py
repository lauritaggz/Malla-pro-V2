import uuid

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
from app.schemas.catalog import (
    CourseRead,
    CurriculumRead,
    PeriodRead,
    ProgramRead,
    TrackRead,
    UniversityRead,
    VersionRead,
)


def _current_published():
    return (CurriculumVersion.is_current.is_(True)) & (CurriculumVersion.status == "published")


async def list_universities(db: AsyncSession) -> list[UniversityRead]:
    rows = (await db.scalars(select(University).order_by(University.name))).all()
    return [UniversityRead.model_validate(r) for r in rows]


async def list_programs(db: AsyncSession, university_slug: str) -> list[ProgramRead] | None:
    """None if the university does not exist. Only programs with a published current version."""
    uni = await db.scalar(select(University).where(University.slug == university_slug))
    if uni is None:
        return None
    rows = (
        await db.scalars(
            select(Program)
            .join(CurriculumVersion, CurriculumVersion.program_id == Program.id)
            .where(Program.university_id == uni.id, _current_published())
            .order_by(Program.sort_order, Program.name)
        )
    ).all()
    return [ProgramRead.model_validate(r) for r in rows]


async def get_current_curriculum(db: AsyncSession, program_id: uuid.UUID) -> CurriculumRead | None:
    row = (
        await db.execute(
            select(Program, University, CurriculumVersion)
            .join(University, University.id == Program.university_id)
            .join(CurriculumVersion, CurriculumVersion.program_id == Program.id)
            .where(Program.id == program_id, _current_published())
        )
    ).first()
    if row is None:
        return None
    program, university, version = row

    tracks = (
        await db.scalars(
            select(Track).where(Track.version_id == version.id).order_by(Track.sort_order)
        )
    ).all()
    track_code = {t.id: t.code for t in tracks}
    courses = (
        await db.scalars(
            select(Course)
            .where(Course.version_id == version.id)
            .order_by(Course.period_number, Course.sort_order)
        )
    ).all()
    aliases_rows = (
        await db.execute(
            select(Course.code, CourseAlias.alias_code)
            .join(Course, Course.id == CourseAlias.course_id)
            .where(CourseAlias.version_id == version.id)
            .order_by(Course.sort_order, CourseAlias.alias_code)
        )
    ).all()

    aliases: dict[str, list[str]] = {}
    for code, alias in aliases_rows:
        bucket = aliases.setdefault(code, [])
        if alias not in bucket:
            bucket.append(alias)

    # Group course ids by (track, period), preserving the source order inside each period.
    periods: dict[tuple[str | None, int], list[uuid.UUID]] = {}
    for c in sorted(courses, key=lambda c: c.sort_order):
        periods.setdefault((track_code.get(c.track_id), c.period_number), []).append(c.id)
    ordered_tracks = [None] + [t.code for t in tracks]
    period_reads = [
        PeriodRead(number=number, track_code=tc, course_ids=ids)
        for tc in ordered_tracks
        for (ptc, number), ids in sorted(periods.items(), key=lambda kv: kv[0][1])
        if ptc == tc
    ]

    return CurriculumRead(
        program=ProgramRead.model_validate(program),
        university=UniversityRead.model_validate(university),
        version=VersionRead.model_validate(version),
        tracks=[
            TrackRead(code=t.code, slug=t.slug, name=t.name, total_credits=t.total_credits)
            for t in tracks
        ],
        periods=period_reads,
        courses=[
            CourseRead(
                id=c.id,
                legacy_id=c.legacy_id,
                code=c.code,
                name=c.name,
                credits=c.credits,
                period_number=c.period_number,
                sort_order=c.sort_order,
                track_code=track_code.get(c.track_id),
                prereq_status=c.prereq_status,
                prereq_expr=c.prereq_expr,
                prereq_raw=c.prereq_raw,
                coreq_expr=c.coreq_expr,
                coreq_raw=c.coreq_raw,
                attrs=c.attrs or {},
            )
            for c in courses
        ],
        aliases=aliases,
    )
