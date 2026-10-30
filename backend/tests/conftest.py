import asyncio
from collections.abc import AsyncIterator
from pathlib import Path

import pytest
import pytest_asyncio
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from alembic import command
from app.core import security
from app.core.config import get_settings
from app.db.session import get_db
from app.main import app

BACKEND_DIR = Path(__file__).resolve().parents[1]


async def _ensure_database(url: str) -> None:
    parsed = make_url(url)
    admin = create_async_engine(
        parsed.set(database="postgres"), isolation_level="AUTOCOMMIT", poolclass=NullPool
    )
    try:
        async with admin.connect() as conn:
            exists = await conn.scalar(
                text("SELECT 1 FROM pg_database WHERE datname = :n"), {"n": parsed.database}
            )
            if not exists:
                await conn.execute(text(f'CREATE DATABASE "{parsed.database}"'))
    finally:
        await admin.dispose()


def _upgrade_head(url: str) -> None:
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
    command.upgrade(cfg, "head")


@pytest_asyncio.fixture(scope="session")
async def test_engine() -> AsyncIterator[AsyncEngine]:
    url = get_settings().test_database_url
    await _ensure_database(url)
    # env.py calls asyncio.run(); run it in a worker thread, outside the test loop.
    await asyncio.to_thread(_upgrade_head, url)
    engine = create_async_engine(url, poolclass=NullPool)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    async with test_engine.begin() as conn:
        rows = await conn.execute(
            text(
                "SELECT quote_ident(tablename) FROM pg_tables "
                "WHERE schemaname = 'public' AND tablename <> 'alembic_version'"
            )
        )
        tables = [r[0] for r in rows]
        if tables:
            await conn.execute(text(f"TRUNCATE {', '.join(tables)} RESTART IDENTITY CASCADE"))
    async with async_sessionmaker(test_engine, expire_on_commit=False)() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncIterator[AsyncClient]:
    async def override_get_db() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------- two authenticated users (T-004)

TEST_CLAIMS: dict[str, dict[str, str]] = {
    "token-user-a": {"uid": "uid-user-a", "email": "a@example.com", "name": "Usuaria A"},
    "token-user-b": {"uid": "uid-user-b", "email": "b@example.com", "name": "Usuario B"},
    "token-user-c": {"uid": "uid-user-c", "email": "c@example.com", "name": "Usuarie C"},
}


def fake_verify_firebase_token(token: str) -> dict[str, str]:
    """Stands in for Firebase in tests: only the two known tokens are valid; no call to Google."""
    if token not in TEST_CLAIMS:
        raise security.InvalidTokenError("unknown test token")
    return dict(TEST_CLAIMS[token])


@pytest_asyncio.fixture
async def fake_firebase(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(security, "verify_firebase_token", fake_verify_firebase_token)


async def _authed_client(token: str) -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        headers={"Authorization": f"Bearer {token}"},
    )


@pytest_asyncio.fixture
async def user_a(client: AsyncClient, fake_firebase: None) -> AsyncIterator[AsyncClient]:
    """HTTP client authenticated as user A (shares the test database with `client`)."""
    async with await _authed_client("token-user-a") as c:
        yield c


@pytest_asyncio.fixture
async def user_b(client: AsyncClient, fake_firebase: None) -> AsyncIterator[AsyncClient]:
    """HTTP client authenticated as user B."""
    async with await _authed_client("token-user-b") as c:
        yield c


@pytest_asyncio.fixture
async def user_c(client: AsyncClient, fake_firebase: None) -> AsyncIterator[AsyncClient]:
    """A third authenticated user, for role tests that need actor, target and bystander."""
    async with await _authed_client("token-user-c") as c:
        yield c
