import pytest
from httpx import ASGITransport, AsyncClient

from app.core.config import Settings
from app.main import create_app


async def _preflight(origin: str, environment: str, monkeypatch: pytest.MonkeyPatch):
    settings = Settings(
        environment=environment,
        CORS_ORIGINS="https://mallapro.cl",
    )
    monkeypatch.setattr("app.main.get_settings", lambda: settings)
    app = create_app()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        return await client.options(
            "/api/v1/universities",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "authorization",
            },
        )


@pytest.mark.parametrize(
    "origin",
    ["http://localhost:5177", "http://127.0.0.1:5174", "http://localhost:3000"],
)
async def test_development_allows_any_local_port(
    origin: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    response = await _preflight(origin, "development", monkeypatch)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin


async def test_development_still_allows_configured_origins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    response = await _preflight("https://mallapro.cl", "development", monkeypatch)
    assert response.headers["access-control-allow-origin"] == "https://mallapro.cl"


@pytest.mark.parametrize("origin", ["http://localhost:5177", "http://127.0.0.1:5174"])
async def test_production_rejects_local_origins(
    origin: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    response = await _preflight(origin, "production", monkeypatch)
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


async def test_production_allows_configured_origins(monkeypatch: pytest.MonkeyPatch) -> None:
    response = await _preflight("https://mallapro.cl", "production", monkeypatch)
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://mallapro.cl"


async def test_development_rejects_non_local_origin(monkeypatch: pytest.MonkeyPatch) -> None:
    response = await _preflight("http://evil.example:5174", "development", monkeypatch)
    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
