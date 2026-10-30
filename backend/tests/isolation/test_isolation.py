"""Isolation between users over the real app (NF-01, T-004)."""

import pytest
from httpx import AsyncClient

from app.main import app
from tests.isolation.framework import (
    PrivateResource,
    all_route_keys,
    assert_isolated,
    find_stale_registrations,
    find_unregistered_private_routes,
    private_route_keys,
)
from tests.isolation.registry import PRIVATE_RESOURCES, SELF_SCOPED_ROUTES


async def test_user_a_and_user_b_are_different_users(
    user_a: AsyncClient, user_b: AsyncClient
) -> None:
    a = (await user_a.get("/api/v1/me")).json()
    b = (await user_b.get("/api/v1/me")).json()
    assert a["email"] == "a@example.com"
    assert b["email"] == "b@example.com"
    assert a["id"] != b["id"]


async def test_unknown_token_is_rejected(client: AsyncClient, fake_firebase: None) -> None:
    response = await client.get("/api/v1/me", headers={"Authorization": "Bearer someone-else"})
    assert response.status_code == 401


def test_route_discovery_sees_the_real_routes() -> None:
    """Guard: if FastAPI changes how routes are stored, discovery must not silently find none."""
    assert ("GET", "/api/v1/me") in private_route_keys(app)
    assert ("GET", "/api/v1/health") in all_route_keys(app)
    assert ("GET", "/api/v1/health") not in private_route_keys(app)


def test_every_private_route_is_registered() -> None:
    missing = find_unregistered_private_routes(app, PRIVATE_RESOURCES, SELF_SCOPED_ROUTES)
    assert not missing, (
        "These routes depend on get_current_user but are not in tests/isolation/registry.py "
        f"(add them to PRIVATE_RESOURCES or SELF_SCOPED_ROUTES): {sorted(missing)}"
    )


def test_registry_has_no_stale_routes() -> None:
    stale = find_stale_registrations(app, PRIVATE_RESOURCES, SELF_SCOPED_ROUTES)
    assert not stale, f"Registered routes that no longer exist: {sorted(stale)}"


@pytest.mark.parametrize("resource", PRIVATE_RESOURCES, ids=lambda r: r.name)
async def test_private_resource_is_isolated(
    resource: PrivateResource, user_a: AsyncClient, user_b: AsyncClient
) -> None:
    await assert_isolated(resource, owner=user_a, other=user_b)
    await assert_isolated(resource, owner=user_b, other=user_a)
