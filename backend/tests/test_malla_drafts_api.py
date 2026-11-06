"""Prototype route POST /api/v1/me/malla-drafts (spike/ia-mallas). The AI is faked."""

from typing import Any

import pytest
from httpx import AsyncClient

from app.api.v1 import malla_drafts
from app.core.config import Settings
from tests.test_ai_malla import FakeClient

URL = "/api/v1/me/malla-drafts"
PDF = {"Content-Type": "application/pdf"}


async def test_returns_a_draft_with_comparison(user_a: AsyncClient, ai_drafts: FakeClient) -> None:
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
    [call] = ai_drafts.calls
    assert call["messages"][0]["content"][0]["type"] == "document"


async def test_requires_login(client: AsyncClient, ai_drafts: FakeClient) -> None:
    response = await client.post(URL, content=b"%PDF", headers=PDF)
    assert response.status_code == 401
    assert ai_drafts.calls == []


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


async def test_rejects_bad_inputs(user_a: AsyncClient, ai_drafts: FakeClient) -> None:
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
    assert ai_drafts.calls == []


async def test_ai_failure_gives_a_safe_502(
    user_a: AsyncClient, ai_drafts: FakeClient, monkeypatch: pytest.MonkeyPatch
) -> None:
    def boom(**_kwargs: Any) -> None:
        raise RuntimeError("secret document text")

    monkeypatch.setattr(ai_drafts, "create", boom)
    response = await user_a.post(URL, content=b"%PDF", headers=PDF)
    assert response.status_code == 502
    assert "secret" not in response.text


async def test_history_lists_opens_and_deletes_own_drafts(
    user_a: AsyncClient, user_b: AsyncClient, ai_drafts: FakeClient
) -> None:
    first = (
        await user_a.post(
            URL, params={"filename": "C:\\x/Quimica.pdf"}, content=b"%PDF", headers=PDF
        )
    ).json()
    second = (
        await user_a.post(URL, params={"compare_with": "QuimicaUCH"}, content=b"%PDF", headers=PDF)
    ).json()
    assert first["documento"] == "Quimica.pdf"
    assert second["documento"] == "documento"

    listing = (await user_a.get(URL)).json()
    assert [d["id"] for d in listing] == [second["id"], first["id"]]  # newest first
    assert listing[0]["cobertura_pct"] == 100.0
    assert listing[1]["cobertura_pct"] is None
    assert listing[0]["ramos"] > 0

    opened = await user_a.get(f"{URL}/{first['id']}")
    assert opened.status_code == 200
    assert opened.json() == first

    # The other user sees none of them (the per-id routes are covered by test_isolation).
    assert (await user_b.get(URL)).json() == []

    assert (await user_a.delete(f"{URL}/{first['id']}")).status_code == 204
    assert (await user_a.get(f"{URL}/{first['id']}")).status_code == 404
    assert [d["id"] for d in (await user_a.get(URL)).json()] == [second["id"]]


async def test_history_rejects_ids_that_are_not_uuids(
    user_a: AsyncClient, ai_drafts: FakeClient
) -> None:
    assert (await user_a.get(f"{URL}/..%2F..%2Fsecret")).status_code in (404, 422)
    assert (await user_a.get(f"{URL}/not-a-uuid")).status_code == 422
