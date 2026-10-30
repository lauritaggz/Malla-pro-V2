"""Tools to prove that one user can never reach another user's data (NF-01, T-004).

Every route that depends on `get_current_user` must be one of:
- registered in `registry.PRIVATE_RESOURCES` (a resource owned by a user, checked with
  `assert_isolated`);
- listed in `registry.SELF_SCOPED_ROUTES` (it only ever acts on the caller, like `/me`);
- listed in `registry.TEAM_ROUTES` with the roles it allows (guarded by `require_role`, T-002).

`find_unregistered_private_routes` makes a test fail as soon as a new private route is added
without one of the two.

Limits (no such routes exist today; extend this module before adding one):
- only `get_current_user` counts as "authenticated"; another auth dependency would be missed;
- only HTTP routes (`APIRoute` and FastAPI's included routers) are inspected, not `app.mount`
  sub-apps or websocket routes.
"""

from __future__ import annotations

import re
from collections.abc import Awaitable, Callable, Iterable, Iterator
from dataclasses import dataclass, field
from typing import Any

from fastapi import FastAPI
from fastapi.dependencies.models import Dependant
from fastapi.routing import APIRoute
from httpx import AsyncClient

from app.core.security import get_current_user

RouteKey = tuple[str, str]  # (HTTP method, path template as declared, e.g. "/api/v1/me/x/{id}")


PATH_PARAM = re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}")


@dataclass(frozen=True)
class Op:
    """A request another user must not be able to make on the owner's resource.

    `path` is the route exactly as FastAPI declares it (e.g. "/api/v1/me/profiles/{profile_id}"),
    so it can be matched against the registry. Every path parameter is filled with the resource
    id unless `params` gives another value. In `json`, the literal "{id}" is replaced by the
    resource id, which covers the id in the body.

    Limit: `params` holds fixed values and `create` returns a single id, so nested routes that
    need the id of a parent created during the test (e.g. a profile's attempts, T-021) cannot be
    expressed yet. Trying fails visibly (owner control or render error), never silently; extend
    `create` to return several ids when the first nested route arrives.
    """

    method: str
    path: str
    json: dict[str, Any] | None = None
    params: dict[str, str] = field(default_factory=dict)

    def render(self, resource_id: str) -> tuple[str, dict[str, Any] | None]:
        path = PATH_PARAM.sub(lambda m: self.params.get(m.group(1), resource_id), self.path)
        if "{" in path or "}" in path:
            raise ValueError(f"Unfilled path parameter in {self.path!r} -> {path!r}")
        body = _fill(self.json, resource_id) if self.json is not None else None
        return path, body

    @property
    def route_key(self) -> RouteKey:
        return (self.method.upper(), self.path)


@dataclass(frozen=True)
class PrivateResource:
    """A kind of data owned by one user (attempts, grades, schedules…)."""

    name: str
    # Creates one resource as `owner` and returns its id.
    create: Callable[[AsyncClient], Awaitable[str]]
    # Route the owner uses to read it back (must return 200 and the same body afterwards).
    read: Op
    # Everything another user will try: read, modify and delete, with the id in URL and body.
    attempts: tuple[Op, ...]
    # Routes used by `create` that are not already in `read`/`attempts`.
    create_routes: tuple[RouteKey, ...] = field(default_factory=tuple)

    def route_keys(self) -> set[RouteKey]:
        keys = {self.read.route_key, *(op.route_key for op in self.attempts)}
        return keys | {(m.upper(), p) for m, p in self.create_routes}


def _fill(value: Any, resource_id: str) -> Any:
    if isinstance(value, str):
        return value.replace("{id}", resource_id)
    if isinstance(value, dict):
        return {k: _fill(v, resource_id) for k, v in value.items()}
    if isinstance(value, list):
        return [_fill(v, resource_id) for v in value]
    return value


async def assert_isolated(
    resource: PrivateResource, owner: AsyncClient, other: AsyncClient
) -> None:
    """Owner creates a resource; every attempt by `other` gets 404 and changes nothing.

    404 and not 403: another user's resource is indistinguishable from one that does not exist
    (docs/architecture/api.md).

    Control: each attempt, made by the owner on a fresh resource of its own, must succeed (2xx).
    Otherwise a 404 would prove nothing (wrong path, wrong body, route that never works).
    """
    for op in resource.attempts:
        control_id = await resource.create(owner)
        path, body = op.render(control_id)
        response = await owner.request(op.method, path, json=body)
        assert 200 <= response.status_code < 300, (
            f"{resource.name}: control failed, the owner's own {op.method} {op.path} returned "
            f"{response.status_code}; fix the Op so the isolation check means something"
        )

    resource_id = await resource.create(owner)
    read_path, _ = resource.read.render(resource_id)
    before = await owner.request(resource.read.method, read_path)
    assert before.status_code == 200, (
        f"{resource.name}: the owner cannot read its own resource ({before.status_code})"
    )

    for op in resource.attempts:
        path, body = op.render(resource_id)
        response = await other.request(op.method, path, json=body)
        assert response.status_code == 404, (
            f"{resource.name}: {op.method} {op.path} by another user returned "
            f"{response.status_code}, expected 404"
        )

    after = await owner.request(resource.read.method, read_path)
    assert after.status_code == 200, f"{resource.name}: the resource disappeared"
    assert after.json() == before.json(), f"{resource.name}: another user changed the resource"


def _depends_on_current_user(dependant: Dependant) -> bool:
    for dep in dependant.dependencies:
        if dep.call is get_current_user or _depends_on_current_user(dep):
            return True
    return False


def _effective_routes(app: FastAPI) -> Iterator[tuple[str, set[str], Dependant | None]]:
    """(path, methods, dependant) of every HTTP route, prefixes and router dependencies applied.

    FastAPI >= 0.14x resolves `include_router` lazily (an internal `_IncludedRouter` route that
    exposes `effective_route_contexts()`); older versions copy APIRoutes into `app.routes`. Both
    are handled. `test_isolation.py` checks that `/api/v1/me` is found, so if FastAPI changes this
    again the test fails instead of silently finding no private routes.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            yield route.path, set(route.methods), route.dependant
            continue
        contexts = getattr(route, "effective_route_contexts", None)
        if callable(contexts):
            for ctx in contexts():
                methods = getattr(ctx, "methods", None)
                if methods:
                    yield ctx.path, set(methods), getattr(ctx, "dependant", None)


def private_route_keys(app: FastAPI) -> set[RouteKey]:
    """(method, path) of every route that needs an authenticated user."""
    return {
        (method, path)
        for path, methods, dependant in _effective_routes(app)
        if dependant is not None and _depends_on_current_user(dependant)
        for method in methods
    }


def all_route_keys(app: FastAPI) -> set[RouteKey]:
    return {(method, path) for path, methods, _ in _effective_routes(app) for method in methods}


def find_unregistered_private_routes(
    app: FastAPI,
    resources: Iterable[PrivateResource],
    self_scoped: Iterable[RouteKey],
    team_routes: Iterable[RouteKey] = (),
) -> set[RouteKey]:
    covered = {key for r in resources for key in r.route_keys()}
    covered |= set(self_scoped) | set(team_routes)
    return private_route_keys(app) - covered


def find_stale_registrations(
    app: FastAPI,
    resources: Iterable[PrivateResource],
    self_scoped: Iterable[RouteKey],
    team_routes: Iterable[RouteKey] = (),
) -> set[RouteKey]:
    """Registered routes that no longer exist (renamed or deleted)."""
    registered = {key for r in resources for key in r.route_keys()}
    registered |= set(self_scoped) | set(team_routes)
    return registered - all_route_keys(app)


def _role_guards(dependant: Dependant) -> list[frozenset[str]]:
    found: list[frozenset[str]] = []
    for dep in dependant.dependencies:
        roles = getattr(dep.call, "required_roles", None)
        if roles is not None:
            found.append(frozenset(roles))
        found += _role_guards(dep)
    return found


def route_role_guards(app: FastAPI) -> dict[RouteKey, frozenset[str] | None]:
    """Roles each route requires through `require_role` (intersection if several), else None."""
    out: dict[RouteKey, frozenset[str] | None] = {}
    for path, methods, dependant in _effective_routes(app):
        guards = _role_guards(dependant) if dependant is not None else []
        allowed = frozenset.intersection(*guards) if guards else None
        for method in methods:
            out[(method, path)] = allowed
    return out
