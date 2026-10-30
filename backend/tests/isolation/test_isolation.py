"""Isolation between users over the real app (NF-01, T-004)."""

import uuid

import pytest
from httpx import AsyncClient

from app.main import app
from tests.isolation.framework import (
    PATH_PARAM,
    PrivateResource,
    all_route_keys,
    assert_isolated,
    find_stale_registrations,
    find_unregistered_private_routes,
    private_route_keys,
    route_role_guards,
)
from tests.isolation.registry import PRIVATE_RESOURCES, SELF_SCOPED_ROUTES, TEAM_ROUTES


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
    missing = find_unregistered_private_routes(
        app, PRIVATE_RESOURCES, SELF_SCOPED_ROUTES, TEAM_ROUTES
    )
    assert not missing, (
        "These routes depend on get_current_user but are not in tests/isolation/registry.py "
        f"(add them to PRIVATE_RESOURCES, SELF_SCOPED_ROUTES or TEAM_ROUTES): {sorted(missing)}"
    )


def test_registry_has_no_stale_routes() -> None:
    stale = find_stale_registrations(app, PRIVATE_RESOURCES, SELF_SCOPED_ROUTES, TEAM_ROUTES)
    assert not stale, f"Registered routes that no longer exist: {sorted(stale)}"


@pytest.mark.parametrize("resource", PRIVATE_RESOURCES, ids=lambda r: r.name)
async def test_private_resource_is_isolated(
    resource: PrivateResource, user_a: AsyncClient, user_b: AsyncClient
) -> None:
    await assert_isolated(resource, owner=user_a, other=user_b)
    await assert_isolated(resource, owner=user_b, other=user_a)


def test_team_routes_declare_exactly_their_roles() -> None:
    """Each registered team route uses require_role with the roles in the registry, and every
    route guarded by require_role is registered as a team route."""
    guards = route_role_guards(app)
    for key, roles in TEAM_ROUTES.items():
        assert guards.get(key) == roles, f"{key}: require_role{sorted(guards.get(key) or [])}"
    guarded = {key for key, roles in guards.items() if roles is not None}
    assert guarded == set(TEAM_ROUTES), sorted(guarded ^ set(TEAM_ROUTES))


@pytest.mark.parametrize("route", sorted(TEAM_ROUTES), ids=lambda r: f"{r[0]} {r[1]}")
async def test_a_student_gets_403_on_every_team_route(
    route: tuple[str, str], user_a: AsyncClient
) -> None:
    method, path = route
    filled = PATH_PARAM.sub(lambda _m: str(uuid.uuid4()), path)
    response = await user_a.request(method, filled, json={})
    assert response.status_code == 403
    assert response.json()["detail"] == "No tienes permisos para esta acción."
