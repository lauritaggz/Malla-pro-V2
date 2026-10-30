from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdTimestampMixin

ROLE_STUDENT = "student"
ROLE_CURATOR = "curator"
ROLE_SUPERADMIN = "superadmin"
ROLES = (ROLE_STUDENT, ROLE_CURATOR, ROLE_SUPERADMIN)


class User(IdTimestampMixin, Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(f"role IN ({', '.join(repr(r) for r in ROLES)})", name="ck_users_role"),
    )

    firebase_uid: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(320), index=True)
    display_name: Mapped[str | None] = mapped_column(String(255))
    photo_url: Mapped[str | None] = mapped_column(String(2048))
    # Team role (AD-03). Checked only in the backend (require_role); never sent by the client.
    role: Mapped[str] = mapped_column(String(16), default=ROLE_STUDENT, server_default=ROLE_STUDENT)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
