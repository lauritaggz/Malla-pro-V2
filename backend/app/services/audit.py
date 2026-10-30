"""Audit log (NF-11): every team action is recorded in the same transaction as the change."""

import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog
from app.models.user import User


def record_audit(
    db: AsyncSession,
    *,
    actor: User | None,
    action: str,
    entity_type: str,
    entity_id: uuid.UUID | str,
    before: dict[str, Any] | None = None,
    after: dict[str, Any] | None = None,
    actor_label: str | None = None,
) -> AuditLog:
    """Add an audit row to the session. The caller commits, together with the change itself.

    Never put grades, document contents, tokens or full e-mails in before/after (NF-07).
    """
    if actor is None and not actor_label:
        raise ValueError("An audit entry without an actor needs an actor_label")
    entry = AuditLog(
        actor_id=actor.id if actor else None,
        actor_label=actor_label,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        before=before,
        after=after,
    )
    db.add(entry)
    return entry
