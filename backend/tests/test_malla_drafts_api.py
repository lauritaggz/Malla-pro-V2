"""Prototype route POST /api/v1/me/malla-drafts (spike/ia-mallas). The AI is faked."""

from typing import Any

import pytest
from httpx import AsyncClient

from app.api.v1 import malla_drafts
from app.core.config import Settings
from app.main import app
from tests.test_ai_malla import FakeClient, as_model_output, verified

URL = "/api/v1/me/malla-drafts"
PDF = {"Content-Type": "application/pdf"}


@pytest.fixture
def enabled(monkeypatch: pytest.MonkeyPatch) -> FakeClient:
    settings = Settings(ENVIRONMENT="development", ANTHROPIC_API_KEY="test-key", AI_MODEL="m")
    monkeypatch.setattr(malla_drafts, "get_settings", lambda: settings)
    fake = FakeClient(as_model_output(verified("QuimicaUCH"), by_number=True))
    app.dependency_overrides[malla_drafts.get_ai_client] = lambda: fake
    yield fake
    app.dependency_overrides.pop(malla_drafts.get_ai_client, None)


async def test_returns_a_draft_with_comparison(user_a: AsyncClient, enabled: FakeClient) -> None:
    response = await user_a.post(
        URL, params={"compare_with": "QuimicaUCH"}, content=b"%PDF-1.4 x", headers=PDF
    )
    assert response.status_code == 200
    body: dict[str, Any] = response.json()
    assert body["malla"]["estado"] == "borrador"
    assert body["problemas"] == []
    assert body["comparacion"]["cobertura_pct"] == 100.0
    assert body["tokens"] == {"entrada": 1234, "salida": 5678}
    assert body["cortado"] is False
    [call] = enabled.calls
    assert call["messages"][0]["content"][0]["type"] == "document"


async def test_requires_login(client: AsyncClient, enabled: FakeClient) -> None:
    response = await client.post(URL, content=b"%PDF", headers=PDF)
    assert response.status_code == 401
    assert enabled.calls == []


@pytest.mark.parametrize(
    "settings",
    [
        {"ENVIRONMENT": "production", "ANTHROPIC_API_KEY": "k"},
        {"ENVIRONMENT": "development", "ANTHROPIC_API_KEY": None},
    ],
    ids=["production", "no-key"],
)
async def test_disabled_outside_development_or_without_key(
    user_a: AsyncClient, monkeypatch: pytest.MonkeyPatch, settings: dict[str, Any]
) -> None:
    monkeypatch.setattr(malla_drafts, "get_settings", lambda: Settings(**settings))
    response = await user_a.post(URL, content=b"%PDF", headers=PDF)
    assert response.status_code == 503
    assert "no está habilitada" in response.json()["detail"]


async def test_rejects_bad_inputs(user_a: AsyncClient, enabled: FakeClient) -> None:
    word = await user_a.post(URL, content=b"PK..", headers={"Content-Type": "application/msword"})
    assert word.status_code == 415
    empty = await user_a.post(URL, content=b"", headers=PDF)
    assert empty.status_code == 400
    big = await user_a.post(URL, content=b"0" * (10 * 1024 * 1024 + 1), headers=PDF)
    assert big.status_code == 413
    traversal = await user_a.post(
        URL, params={"compare_with": "../../etc/passwd"}, content=b"%PDF", headers=PDF
    )
    assert traversal.status_code == 404
    assert enabled.calls == []


async def test_ai_failure_gives_a_safe_502(
    user_a: AsyncClient, enabled: FakeClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def boom(**_kwargs: Any) -> None:
        raise RuntimeError("secret document text")

    monkeypatch.setattr(enabled, "create", boom)
    response = await user_a.post(URL, content=b"%PDF", headers=PDF)
    assert response.status_code == 502
    assert "secret" not in response.text
