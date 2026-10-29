import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    false,
    text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, IdTimestampMixin

PERIOD_REGIMES = ("semestral", "trimestral", "anual")
VERSION_STATUSES = ("draft", "published", "archived")
SOURCE_TYPES = ("legacy_json", "official_pdf", "ai_import", "manual")
PREREQ_STATUSES = ("none", "known", "unknown")


def _in(column: str, values: tuple[str, ...]) -> str:
    return f"{column} IN ({', '.join(repr(v) for v in values)})"


class University(IdTimestampMixin, Base):
    __tablename__ = "universities"

    slug: Mapped[str] = mapped_column(String(64), unique=True)
    name: Mapped[str] = mapped_column(String(255))
    short_name: Mapped[str | None] = mapped_column(String(32))
    country: Mapped[str] = mapped_column(String(2), default="CL", server_default="CL")

    programs: Mapped[list["Program"]] = relationship(back_populates="university")


class Program(IdTimestampMixin, Base):
    """A career (carrera). career_key is the stable id the frontend keys user progress on."""

    __tablename__ = "programs"
    __table_args__ = (
        UniqueConstraint("university_id", "slug", name="uq_programs_university_slug"),
    )

    university_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("universities.id"), index=True)
    slug: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(255))
    # Title as it appears in the curriculum file ("carrera"); the UI keys some storage on it.
    official_name: Mapped[str | None] = mapped_column(String(255))
    official_code: Mapped[str | None] = mapped_column(String(64))
    career_key: Mapped[str] = mapped_column(String(160), unique=True)
    legacy_url: Mapped[str | None] = mapped_column(String(255), unique=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    university: Mapped[University] = relationship(back_populates="programs")
    versions: Mapped[list["CurriculumVersion"]] = relationship(back_populates="program")


class CurriculumVersion(IdTimestampMixin, Base):
    __tablename__ = "curriculum_versions"
    __table_args__ = (
        UniqueConstraint("program_id", "label", name="uq_versions_program_label"),
        Index(
            "uq_versions_one_current_per_program",
            "program_id",
            unique=True,
            postgresql_where=text("is_current"),
        ),
        CheckConstraint(_in("period_regime", PERIOD_REGIMES), name="ck_versions_period_regime"),
        CheckConstraint(_in("status", VERSION_STATUSES), name="ck_versions_status"),
        CheckConstraint(_in("source_type", SOURCE_TYPES), name="ck_versions_source_type"),
    )

    program_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("programs.id"), index=True)
    label: Mapped[str] = mapped_column(String(64))
    period_regime: Mapped[str] = mapped_column(String(16))
    credit_system: Mapped[str] = mapped_column(String(32))
    total_periods: Mapped[int] = mapped_column(Integer)
    total_credits: Mapped[int | None] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(16), default="draft", server_default="draft")
    is_current: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false())
    source_type: Mapped[str] = mapped_column(String(16))
    source_url: Mapped[str | None] = mapped_column(String(2048))
    source_note: Mapped[str | None] = mapped_column(Text)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    # Source fields with no column of their own (official source, equivalences, notes).
    attrs: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default=text("'{}'::jsonb")
    )

    program: Mapped[Program] = relationship(back_populates="versions")
    tracks: Mapped[list["Track"]] = relationship(back_populates="version")
    courses: Mapped[list["Course"]] = relationship(back_populates="version")


class Track(IdTimestampMixin, Base):
    """A mención/specialization. Common courses have no track."""

    __tablename__ = "tracks"
    __table_args__ = (
        UniqueConstraint("version_id", "slug", name="uq_tracks_version_slug"),
        UniqueConstraint("version_id", "code", name="uq_tracks_version_code"),
    )

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("curriculum_versions.id", ondelete="CASCADE"), index=True
    )
    slug: Mapped[str] = mapped_column(String(64))
    code: Mapped[str] = mapped_column(String(64))
    name: Mapped[str] = mapped_column(String(255))
    total_credits: Mapped[int | None] = mapped_column(Integer)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    version: Mapped[CurriculumVersion] = relationship(back_populates="tracks")


class Course(IdTimestampMixin, Base):
    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint("version_id", "legacy_id", name="uq_courses_version_legacy_id"),
        CheckConstraint(_in("prereq_status", PREREQ_STATUSES), name="ck_courses_prereq_status"),
        Index("ix_courses_version_period", "version_id", "period_number", "sort_order"),
    )

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("curriculum_versions.id", ondelete="CASCADE")
    )
    track_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("tracks.id", ondelete="CASCADE"), index=True
    )
    period_number: Mapped[int] = mapped_column(Integer)
    sort_order: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    # Not unique: the same code can appear once per track, with distinct legacy ids.
    code: Mapped[str | None] = mapped_column(String(32), index=True)
    name: Mapped[str] = mapped_column(String(255))
    credits: Mapped[int | None] = mapped_column(Integer)
    legacy_id: Mapped[int | None] = mapped_column(Integer)
    prereq_status: Mapped[str] = mapped_column(String(16))
    prereq_expr: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    # Original text. None = absent in the source; "" = present but empty.
    prereq_raw: Mapped[str | None] = mapped_column(Text)
    coreq_expr: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    coreq_raw: Mapped[str | None] = mapped_column(Text)
    attrs: Mapped[dict[str, Any]] = mapped_column(
        JSONB, default=dict, server_default=text("'{}'::jsonb")
    )

    version: Mapped[CurriculumVersion] = relationship(back_populates="courses")
    track: Mapped[Track | None] = relationship()


class CourseAlias(IdTimestampMixin, Base):
    __tablename__ = "course_aliases"
    __table_args__ = (
        UniqueConstraint("version_id", "alias_code", "course_id", name="uq_course_aliases"),
    )

    version_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("curriculum_versions.id", ondelete="CASCADE"), index=True
    )
    alias_code: Mapped[str] = mapped_column(String(32))
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
