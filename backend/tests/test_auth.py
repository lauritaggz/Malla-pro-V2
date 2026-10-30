import pytest
from httpx import AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import security
from app.models.user import User

ME = "/api/v1/me"


def _fake_verify(claims_by_token: dict[str, dict]):
    def verify(token: str) -> dict:
        if token not in claims_by_token:
            raise security.InvalidTokenError("bad token")
        return claims_by_token[token]

    return verify


async def _count_users(db: AsyncSession) -> int:
    return await db.scalar(select(func.count()).select_from(User))


async def test_me_without_header_returns_401(client: AsyncClient) -> None:
    response = await client.get(ME)
    assert response.status_code == 401
    assert "Authorization" in response.json()["detail"]


async def test_me_with_invalid_token_returns_401(
    client: AsyncClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(security, "verify_firebase_token", _fake_verify({}))
    response = await client.get(ME, headers={"Authorization": "Bearer nope"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Token inválido o expirado. Vuelve a iniciar sesión."


async def test_valid_token_creates_user(
    client: AsyncClient, db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    claims = {
        "uid": "uid-1",
        "email": "ana@example.com",
        "name": "Ana Pérez",
        "picture": "https://example.com/a.png",
    }
    monkeypatch.setattr(security, "verify_firebase_token", _fake_verify({"t1": claims}))

    response = await client.get(ME, headers={"Authorization": "Bearer t1"})

    assert response.status_code == 200
    body = response.json()
    assert body["email"] == "ana@example.com"
    assert body["display_name"] == "Ana Pérez"
    assert body["photo_url"] == "https://example.com/a.png"
    assert body["role"] == "student"
    assert set(body) == {"id", "email", "display_name", "photo_url", "role", "created_at"}
    assert await _count_users(db_session) == 1


async def test_second_login_updates_without_duplicating(
    client: AsyncClient, db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = {"uid": "uid-1", "email": "ana@example.com", "name": "Ana"}
    second = {"uid": "uid-1", "email": "ana@example.com", "name": "Ana María"}
    monkeypatch.setattr(security, "verify_firebase_token", _fake_verify({"a": first, "b": second}))

    r1 = await client.get(ME, headers={"Authorization": "Bearer a"})
    r2 = await client.get(ME, headers={"Authorization": "Bearer b"})

    assert r1.status_code == r2.status_code == 200
    assert r1.json()["id"] == r2.json()["id"]
    assert r2.json()["display_name"] == "Ana María"
    assert await _count_users(db_session) == 1


async def test_cors_preflight_allows_authorization_header(client: AsyncClient) -> None:
    response = await client.options(
        ME,
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization",
        },
    )
    assert response.status_code == 200
    assert "authorization" in response.headers["access-control-allow-headers"].lower()
