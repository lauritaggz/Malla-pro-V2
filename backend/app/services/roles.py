"""Team roles (AD-03): only a superadmin assigns or revokes roles; every change is audited."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import ROLE_SUPERADMIN, ROLES, User
from app.services.audit import record_audit

ACTION_ROLE_CHANGED = "user.role_changed"


class RoleError(Exception):
    """Base class for role changes the service refuses."""


class UserNotFound(RoleError):
    pass


class SelfDemotion(RoleError):
    """A superadmin tried to remove their own superadmin role."""


class AmbiguousUser(RoleError):
    """More than one account has that e-mail."""


async def change_role(
    db: AsyncSession,
    *,
    target_id: uuid.UUID,
    new_role: str,
    actor: User | None,
    actor_label: str | None = None,
) -> tuple[User, bool]:
    """Set `target_id`'s role. Returns (user, changed). Audits only real changes. No commit."""
    if new_role not in ROLES:
        raise ValueError(f"Unknown role {new_role!r}")
    target = await db.get(User, target_id)
    if target is None:
        raise UserNotFound(str(target_id))
    if (
        actor is not None
        and actor.id == target.id
        and target.role == ROLE_SUPERADMIN
        and new_role != ROLE_SUPERADMIN
    ):
        raise SelfDemotion(str(target_id))
    if target.role == new_role:
        return target, False
    old_role = target.role
    target.role = new_role
    record_audit(
        db,
        actor=actor,
        actor_label=actor_label,
        action=ACTION_ROLE_CHANGED,
        entity_type="user",
        entity_id=target.id,
        before={"role": old_role},
        after={"role": new_role},
    )
    await db.flush()
    return target, True


async def find_user_by_email(db: AsyncSession, email: str) -> User:
    users = (
        await db.scalars(select(User).where(func.lower(User.email) == email.strip().lower()))
    ).all()
    if not users:
        raise UserNotFound(email)
    if len(users) > 1:
        raise AmbiguousUser(email)
    return users[0]
