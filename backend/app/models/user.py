from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, false
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, IdTimestampMixin


class User(IdTimestampMixin, Base):
    __tablename__ = "users"

    firebase_uid: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    email: Mapped[str | None] = mapped_column(String(320), index=True)
    display_name: Mapped[str | None] = mapped_column(String(255))
    photo_url: Mapped[str | None] = mapped_column(String(2048))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default=false())
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
