"""Team routes (AD-03). Every route here declares its role guard explicitly."""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import require_role
from app.db.session import get_db
from app.models.user import ROLE_SUPERADMIN, User
from app.schemas.user import AdminUserRead, RoleUpdate
from app.services.roles import ActorNotAllowed, SelfDemotion, UserNotFound, change_role

router = APIRouter(prefix="/admin", tags=["admin"])

Superadmin = Annotated[User, Depends(require_role(ROLE_SUPERADMIN))]
Db = Annotated[AsyncSession, Depends(get_db)]


@router.patch("/users/{user_id}/role", response_model=AdminUserRead)
async def update_user_role(user_id: uuid.UUID, body: RoleUpdate, actor: Superadmin, db: Db) -> User:
    try:
        target, _changed = await change_role(db, target_id=user_id, new_role=body.role, actor=actor)
    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No existe ese usuario."
        ) from None
    except ActorNotAllowed:
        # The actor lost the role between the guard and the lock (concurrent change).
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos para esta acción.",
        ) from None
    except SelfDemotion:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No puedes quitarte tu propio rol de superadministrador.",
        ) from None
    await db.commit()
    return target
