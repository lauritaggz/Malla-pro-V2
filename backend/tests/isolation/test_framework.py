"""Tests of the isolation tools themselves, on a throwaway app (T-004).

The real app has no user-owned resources yet, so these prove that `assert_isolated` catches
every kind of leak (read, update, delete, id in the body) and that the route registry check
notices unregistered private routes, including ones protected only through a nested dependency
or a router-level dependency.
"""

import uuid
from collections.abc import AsyncIterator
from typing import Annotated, Any

import pytest
import pytest_asyncio
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from httpx import ASGITransport, AsyncClient
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user
from app.db.session import get_db
from app.models.user import User
from tests.isolation.framework import (
    Op,
    PrivateResource,
    assert_isolated,
    find_stale_registrations,
    find_unregistered_private_routes,
)

CurrentUser = Annotated[User, Depends(get_current_user)]
LEAKS = ("read", "update", "delete", "body")


class NoteIn(BaseModel):
    text: str


class ShareIn(BaseModel):
    note_id: str


def make_notes_app(leaks: set[str]) -> FastAPI:
    """A tiny private resource. Each name in `leaks` drops the owner check on that operation."""
    notes: dict[str, dict[str, Any]] = {}
    app = FastAPI()

    def find(note_id: str, user: User, leak: str) -> dict[str, Any]:
        note = notes.get(note_id)
        if note is None or (leak not in leaks and note["owner"] != user.id):
            raise HTTPException(status_code=404, detail="No existe")
        return note

    @app.post("/notes")
    async def create(body: NoteIn, user: CurrentUser) -> dict[str, str]:
        note_id = str(uuid.uuid4())
        notes[note_id] = {"owner": user.id, "text": body.text, "shared": False}
        return {"id": note_id}

    @app.get("/notes/{note_id}")
    async def read(note_id: str, user: CurrentUser) -> dict[str, Any]:
        note = find(note_id, user, "read")
        return {"text": note["text"], "shared": note["shared"]}

    @app.patch("/notes/{note_id}")
    async def update(note_id: str, body: NoteIn, user: CurrentUser) -> dict[str, str]:
        find(note_id, user, "update")["text"] = body.text
        return {"ok": "yes"}

    @app.delete("/notes/{note_id}")
    async def delete(note_id: str, user: CurrentUser) -> dict[str, str]:
        find(note_id, user, "delete")
        del notes[note_id]
        return {"ok": "yes"}

    @app.post("/notes/share")
    async def share(body: ShareIn, user: CurrentUser) -> dict[str, str]:
        find(body.note_id, user, "body")["shared"] = True
        return {"ok": "yes"}

    return app


async def _create_note(owner: AsyncClient) -> str:
    response = await owner.post("/notes", json={"text": "privada"})
    assert response.status_code == 200
    return response.json()["id"]


NOTES = PrivateResource(
    name="toy note",
    create=_create_note,
    read=Op("GET", "/notes/{id}"),
    attempts=(
        Op("GET", "/notes/{id}"),
        Op("PATCH", "/notes/{id}", json={"text": "cambiada por otro"}),
        Op("POST", "/notes/share", json={"note_id": "{id}"}),
        Op("DELETE", "/notes/{id}"),
    ),
    create_routes=(("POST", "/notes"),),
)


@pytest_asyncio.fixture
async def toy_clients(db_session: AsyncSession, fake_firebase: None) -> AsyncIterator[Any]:
    """Factory: (owner, other) clients for a notes app with the given leaks."""
    opened: list[AsyncClient] = []

    async def override_get_db() -> AsyncIterator[AsyncSession]:
        yield db_session

    def build(leaks: set[str]) -> tuple[AsyncClient, AsyncClient]:
        app = make_notes_app(leaks)
        app.dependency_overrides[get_db] = override_get_db
        pair = tuple(
            AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://toy",
                headers={"Authorization": f"Bearer {token}"},
            )
            for token in ("token-user-a", "token-user-b")
        )
        opened.extend(pair)
        return pair  # type: ignore[return-value]

    yield build
    for c in opened:
        await c.aclose()


async def test_isolated_resource_passes(toy_clients: Any) -> None:
    owner, other = toy_clients(set())
    await assert_isolated(NOTES, owner, other)


@pytest.mark.parametrize("leak", LEAKS)
async def test_each_kind_of_leak_is_caught(toy_clients: Any, leak: str) -> None:
    owner, other = toy_clients({leak})
    with pytest.raises(AssertionError, match="by another user returned 200"):
        await assert_isolated(NOTES, owner, other)


# ---------------------------------------------------------------- route registry


def _registry_app() -> FastAPI:
    app = FastAPI()

    def owned_by_caller(user: CurrentUser) -> User:  # nested dependency on the current user
        return user

    @app.get("/public")
    async def public() -> dict[str, str]:
        return {}

    @app.get("/me")
    async def me(user: CurrentUser) -> dict[str, str]:
        return {}

    @app.get("/things/{thing_id}")
    async def thing(thing_id: str, user: Annotated[User, Depends(owned_by_caller)]) -> dict:
        return {}

    guarded = APIRouter(dependencies=[Depends(get_current_user)])

    @guarded.delete("/guarded/{thing_id}")
    async def guarded_delete(thing_id: str) -> dict[str, str]:
        return {}

    app.include_router(guarded)
    return app


def test_registry_flags_unregistered_private_routes() -> None:
    app = _registry_app()
    missing = find_unregistered_private_routes(app, [], {("GET", "/me")})
    # The public route is ignored; nested and router-level dependencies are detected.
    assert missing == {("GET", "/things/{thing_id}"), ("DELETE", "/guarded/{thing_id}")}


def test_registry_accepts_registered_routes() -> None:
    app = _registry_app()
    resource = PrivateResource(
        name="thing",
        create=_create_note,
        read=Op("GET", "/things/{thing_id}"),
        attempts=(Op("DELETE", "/guarded/{thing_id}"),),
    )
    assert find_unregistered_private_routes(app, [resource], {("GET", "/me")}) == set()


def test_registry_flags_stale_entries() -> None:
    app = _registry_app()
    stale = find_stale_registrations(app, [NOTES], {("GET", "/me"), ("GET", "/gone")})
    assert ("GET", "/gone") in stale
    assert ("POST", "/notes/share") in stale  # NOTES routes do not exist in this app
