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
# Leaks where the other user gets 200.
OPEN_LEAKS = ("read", "update", "delete", "body")


class NoteIn(BaseModel):
    text: str


class ShareIn(BaseModel):
    note_id: str


def make_notes_app(leaks: set[str] = frozenset()) -> FastAPI:  # type: ignore[assignment]
    """A tiny private resource. `leaks` breaks it on purpose:

    - "read" / "update" / "delete" / "body": that operation skips the owner check (200).
    - "forbidden": another user gets 403 instead of 404 (reveals that the note exists).
    - "silent_update" / "silent_delete": another user's PATCH / DELETE changes the note but
      answers 404, as if nothing happened.
    """
    notes: dict[str, dict[str, Any]] = {}
    app = FastAPI()

    def find(note_id: str, user: User, op: str) -> dict[str, Any]:
        note = notes.get(note_id)
        if note is None:
            raise HTTPException(status_code=404, detail="No existe")
        if note["owner"] != user.id and op not in leaks:
            if "forbidden" in leaks:
                raise HTTPException(status_code=403, detail="No es tuya")
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
        if "silent_update" in leaks and note_id in notes:
            notes[note_id]["text"] = body.text
        find(note_id, user, "update")["text"] = body.text
        return {"ok": "yes"}

    @app.delete("/notes/{note_id}")
    async def delete(note_id: str, user: CurrentUser) -> dict[str, str]:
        if "silent_delete" in leaks and note_id in notes and notes[note_id]["owner"] != user.id:
            del notes[note_id]
            raise HTTPException(status_code=404, detail="No existe")
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


# Path parameter named note_id (not "id"): the Op uses the declared route, as the registry needs.
NOTES = PrivateResource(
    name="toy note",
    create=_create_note,
    read=Op("GET", "/notes/{note_id}"),
    attempts=(
        Op("GET", "/notes/{note_id}"),
        Op("PATCH", "/notes/{note_id}", json={"text": "cambiada por otro"}),
        Op("POST", "/notes/share", json={"note_id": "{id}"}),
        Op("DELETE", "/notes/{note_id}"),
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


@pytest.mark.parametrize("leak", OPEN_LEAKS)
async def test_each_kind_of_leak_is_caught(toy_clients: Any, leak: str) -> None:
    owner, other = toy_clients({leak})
    with pytest.raises(AssertionError, match="by another user returned 200"):
        await assert_isolated(NOTES, owner, other)


async def test_403_instead_of_404_is_caught(toy_clients: Any) -> None:
    owner, other = toy_clients({"forbidden"})
    with pytest.raises(AssertionError, match="by another user returned 403, expected 404"):
        await assert_isolated(NOTES, owner, other)


async def test_silent_change_is_caught(toy_clients: Any) -> None:
    owner, other = toy_clients({"silent_update"})
    with pytest.raises(AssertionError, match="another user changed the resource"):
        await assert_isolated(NOTES, owner, other)


async def test_silent_delete_is_caught(toy_clients: Any) -> None:
    owner, other = toy_clients({"silent_delete"})
    with pytest.raises(AssertionError, match="the resource disappeared"):
        await assert_isolated(NOTES, owner, other)


async def test_an_attempt_that_never_works_is_rejected(toy_clients: Any) -> None:
    """A 404 from a route that fails for everyone proves nothing: the owner control catches it."""
    owner, other = toy_clients(set())
    broken = PrivateResource(
        name="toy note with a wrong body",
        create=_create_note,
        read=NOTES.read,
        attempts=(Op("PATCH", "/notes/{note_id}", json={"wrong": "field"}),),
    )
    with pytest.raises(AssertionError, match="control failed"):
        await assert_isolated(broken, owner, other)


@pytest.mark.parametrize(
    "broken",
    [
        Op("GET", "/notes/{note_id}", params={"note_id": "does-not-exist"}),  # wrong id
        Op("GET", "/note/{note_id}"),  # typo in the route
    ],
    ids=["param-to-missing-id", "route-typo"],
)
async def test_an_attempt_that_404s_for_the_owner_too_is_rejected(
    toy_clients: Any, broken: Op
) -> None:
    """The case behind A1: with a real leak, a probe that 404s for everyone must not pass.

    The broken probe comes after a valid one, so the control has to check every attempt.
    """
    owner, other = toy_clients({"read"})
    resource = PrivateResource(
        name="toy note with a probe that never reaches the note",
        create=_create_note,
        read=NOTES.read,
        attempts=(Op("PATCH", "/notes/{note_id}", json={"text": "x"}), broken),
    )
    with pytest.raises(AssertionError, match="control failed.*returned 404"):
        await assert_isolated(resource, owner, other)


def test_op_fills_every_path_parameter() -> None:
    op = Op("GET", "/profiles/{profile_id}/attempts/{attempt_id}", params={"profile_id": "p1"})
    assert op.render("a9") == ("/profiles/p1/attempts/a9", None)
    assert Op("POST", "/x", json={"ids": ["{id}"], "n": 1}).render("r1") == (
        "/x",
        {"ids": ["r1"], "n": 1},
    )
    with pytest.raises(ValueError, match="Unfilled path parameter"):
        Op("GET", "/notes/{note-id}").render("r1")


def test_toy_resource_registers_against_its_own_app() -> None:
    """The Op paths are the declared routes, so the registry recognises them."""
    app = make_notes_app()
    assert find_unregistered_private_routes(app, [NOTES], set()) == set()
    assert find_stale_registrations(app, [NOTES], set()) == set()


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
    assert ("GET", "/me") not in stale
