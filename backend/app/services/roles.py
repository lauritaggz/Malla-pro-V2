"""Team roles (AD-03): only a superadmin assigns or revokes roles; every change is audited."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import ROLE_SUPERADMIN, ROLES, User
from app.services.audit import record_audit

ACTION_ROLE_CHANGED = "user.role_changed"


class RoleError(Exception):
    """Base class for role changes the service refuses. Messages never carry e-mails (NF-07)."""


class UserNotFound(RoleError):
    pass


class SelfDemotion(RoleError):
    """A superadmin tried to remove their own superadmin role."""


class ActorNotAllowed(RoleError):
    """The actor is no longer a superadmin (e.g. demoted by someone else a moment ago)."""


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
    """Set `target_id`'s role. Returns (user, changed). Audits only real changes. No commit.

    The actor and target rows are locked (SELECT ... FOR UPDATE, in id order to avoid
    deadlocks) and the actor's role is checked again under the lock. So two superadmins demoting
    each other at the same time cannot both succeed: the second one sees that it is no longer a
    superadmin. The caller commits; until then neither the change nor its audit row exists.
    """
    if new_role not in ROLES:
        raise ValueError(f"Unknown role {new_role!r}")
    ids = sorted({target_id, *([actor.id] if actor is not None else [])})
    locked = {
        u.id: u
        for u in (
            await db.scalars(
                select(User)
                .where(User.id.in_(ids))
                .order_by(User.id)
                .with_for_update()
                .execution_options(populate_existing=True)
            )
        ).all()
    }
    target = locked.get(target_id)
    if target is None:
        raise UserNotFound("target user does not exist")
    if actor is not None:
        current_actor = locked.get(actor.id)
        if current_actor is None or current_actor.role != ROLE_SUPERADMIN:
            raise ActorNotAllowed("actor is not a superadmin")
        if current_actor.id == target.id and new_role != ROLE_SUPERADMIN:
            raise SelfDemotion("a superadmin cannot remove their own role")
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
        raise UserNotFound("no account with that e-mail")
    if len(users) > 1:
        raise AmbiguousUser("several accounts with that e-mail")
    return users[0]
