import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.schemas.prereq import PrereqNode


class UniversityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str
    short_name: str | None
    country: str


class ProgramRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    slug: str
    name: str
    official_name: str | None
    official_code: str | None
    career_key: str
    legacy_url: str | None


class VersionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    label: str
    period_regime: str
    credit_system: str
    total_periods: int
    total_credits: int | None
    status: str
    is_current: bool
    source_type: str
    source_url: str | None
    source_note: str | None
    reviewed_at: datetime | None


class TrackRead(BaseModel):
    code: str
    slug: str
    name: str
    total_credits: int | None


class CourseRead(BaseModel):
    id: uuid.UUID
    legacy_id: int | None
    code: str | None
    name: str
    credits: int | None
    period_number: int
    sort_order: int
    track_code: str | None
    prereq_status: str
    prereq_expr: PrereqNode | None
    prereq_raw: str | None
    coreq_expr: PrereqNode | None
    coreq_raw: str | None
    attrs: dict[str, Any]


class PeriodRead(BaseModel):
    number: int
    track_code: str | None
    course_ids: list[uuid.UUID]


class CurriculumRead(BaseModel):
    program: ProgramRead
    university: UniversityRead
    version: VersionRead
    tracks: list[TrackRead]
    periods: list[PeriodRead]
    courses: list[CourseRead]
    aliases: dict[str, list[str]]
