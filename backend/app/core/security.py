import asyncio
from datetime import UTC, datetime
from typing import Annotated, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.firebase import get_firebase_app
from app.db.session import get_db
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)

CLOCK_SKEW_SECONDS = 10


class InvalidTokenError(Exception):
    """The Firebase ID token is malformed, expired, revoked or otherwise not valid."""


def verify_firebase_token(token: str) -> dict[str, Any]:
    """Verify a Firebase ID token. Replaceable in tests (monkeypatch) to avoid calling Google."""
    try:
        return auth.verify_id_token(
            token, app=get_firebase_app(), clock_skew_seconds=CLOCK_SKEW_SECONDS
        )
    except (ValueError, auth.InvalidIdTokenError, auth.RevokedIdTokenError) as exc:
        raise InvalidTokenError(str(exc)) from exc


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> User:
    if credentials is None or not credentials.credentials:
        raise _unauthorized("Falta el encabezado Authorization con el token de sesión.")

    try:
        claims = await asyncio.to_thread(verify_firebase_token, credentials.credentials)
    except InvalidTokenError:
        raise _unauthorized("Token inválido o expirado. Vuelve a iniciar sesión.") from None

    firebase_uid = claims.get("uid") or claims.get("sub")
    if not firebase_uid:
        raise _unauthorized("Token inválido o expirado. Vuelve a iniciar sesión.")

    now = datetime.now(UTC)
    profile = {
        "email": claims.get("email"),
        "display_name": claims.get("name"),
        "photo_url": claims.get("picture"),
        "last_login_at": now,
    }
    stmt = (
        pg_insert(User)
        .values(firebase_uid=firebase_uid, **profile)
        .on_conflict_do_update(
            index_elements=[User.firebase_uid], set_={**profile, "updated_at": now}
        )
        .returning(User)
    )
    user = (await db.execute(stmt)).scalar_one()
    await db.commit()
    return user
