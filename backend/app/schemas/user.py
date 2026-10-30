import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str | None
    display_name: str | None
    photo_url: str | None
    role: str
    created_at: datetime


Role = Literal["student", "curator", "superadmin"]


class RoleUpdate(BaseModel):
    role: Role


class AdminUserRead(BaseModel):
    """What the team sees of a user: no grades, progress or login details."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str | None
    display_name: str | None
    role: str
