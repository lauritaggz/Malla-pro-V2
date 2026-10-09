from collections.abc import AsyncIterator

from httpx import ASGITransport, AsyncClient

from app.db.session import get_db
from app.main import app


class BrokenSession:
    async def execute(self, *args, **kwargs):
        raise ConnectionRefusedError("database is down")


async def test_health_ok(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


async def test_health_database_down() -> None:
    async def broken_get_db() -> AsyncIterator[BrokenSession]:
        yield BrokenSession()

    app.dependency_overrides[get_db] = broken_get_db
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
            response = await c.get("/api/v1/health")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 503
    assert response.json() == {"status": "degraded", "database": "error"}
