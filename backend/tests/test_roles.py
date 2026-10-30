"""Team roles and audit log (T-002: AD-01, AD-03, NF-11, CO-04)."""

import asyncio
import uuid
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import func, select, text, update
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from alembic import command
from app.core.config import get_settings
from app.core.security import require_role
from app.models.audit import AuditLog
from app.models.user import User
from app.scripts import set_role as set_role_script
from app.services.audit import record_audit
from app.services.roles import (
    ActorNotAllowed,
    AmbiguousUser,
    UserNotFound,
    change_role,
    find_user_by_email,
)
from tests.conftest import BACKEND_DIR, _ensure_database

ROLE_URL = "/api/v1/admin/users/{}/role"


async def _me(client: AsyncClient) -> dict:
    response = await client.get("/api/v1/me")
    assert response.status_code == 200
    return response.json()


async def _set_role(db: AsyncSession, user_id: str, role: str) -> None:
    await db.execute(update(User).where(User.id == uuid.UUID(user_id)).values(role=role))
    await db.commit()


async def _audit_rows(db: AsyncSession) -> list[AuditLog]:
    db.expire_all()
    return list((await db.scalars(select(AuditLog).order_by(AuditLog.created_at))).all())


# ---------------------------------------------------------------- /me


async def test_me_reports_role_and_new_users_are_students(user_a: AsyncClient) -> None:
    body = await _me(user_a)
    assert body["role"] == "student"
    assert "is_admin" not in body


# ---------------------------------------------------------------- role x route matrix


@pytest.mark.parametrize(
    ("actor_role", "expected"),
    [("student", 403), ("curator", 403), ("superadmin", 200)],
)
async def test_only_a_superadmin_changes_roles(
    actor_role: str,
    expected: int,
    user_a: AsyncClient,
    user_b: AsyncClient,
    db_session: AsyncSession,
) -> None:
    actor = await _me(user_a)
    target = await _me(user_b)
    await _set_role(db_session, actor["id"], actor_role)

    response = await user_a.patch(ROLE_URL.format(target["id"]), json={"role": "curator"})

    assert response.status_code == expected
    db_session.expire_all()
    stored = await db_session.get(User, uuid.UUID(target["id"]))
    assert stored.role == ("curator" if expected == 200 else "student")
    assert len(await _audit_rows(db_session)) == (1 if expected == 200 else 0)
    if expected == 403:
        assert response.json()["detail"] == "No tienes permisos para esta acción."


async def test_role_change_requires_login(client: AsyncClient) -> None:
    response = await client.patch(ROLE_URL.format(uuid.uuid4()), json={"role": "curator"})
    assert response.status_code == 401


# ---------------------------------------------------------------- audit


async def test_role_change_is_audited(
    user_a: AsyncClient, user_b: AsyncClient, db_session: AsyncSession
) -> None:
    actor = await _me(user_a)
    target = await _me(user_b)
    await _set_role(db_session, actor["id"], "superadmin")

    response = await user_a.patch(ROLE_URL.format(target["id"]), json={"role": "curator"})

    assert response.status_code == 200
    assert response.json() == {
        "id": target["id"],
        "email": "b@example.com",
        "display_name": "Usuario B",
        "role": "curator",
    }
    [row] = await _audit_rows(db_session)
    assert str(row.actor_id) == actor["id"]
    assert row.actor_label is None
    assert (row.action, row.entity_type, row.entity_id) == (
        "user.role_changed",
        "user",
        target["id"],
    )
    assert (row.before, row.after) == ({"role": "student"}, {"role": "curator"})
    assert row.created_at is not None


async def test_setting_the_same_role_changes_nothing_and_is_not_audited(
    user_a: AsyncClient, user_b: AsyncClient, db_session: AsyncSession
) -> None:
    actor = await _me(user_a)
    target = await _me(user_b)
    await _set_role(db_session, actor["id"], "superadmin")
    response = await user_a.patch(ROLE_URL.format(target["id"]), json={"role": "student"})
    assert response.status_code == 200
    assert await _audit_rows(db_session) == []


async def test_a_superadmin_cannot_remove_their_own_role(
    user_a: AsyncClient, db_session: AsyncSession
) -> None:
    actor = await _me(user_a)
    await _set_role(db_session, actor["id"], "superadmin")

    for role in ("curator", "student"):
        response = await user_a.patch(ROLE_URL.format(actor["id"]), json={"role": role})
        assert response.status_code == 409
        assert response.json()["detail"] == (
            "No puedes quitarte tu propio rol de superadministrador."
        )
    # Re-asserting the own role is harmless.
    ok = await user_a.patch(ROLE_URL.format(actor["id"]), json={"role": "superadmin"})
    assert ok.status_code == 200
    db_session.expire_all()
    assert (await db_session.get(User, uuid.UUID(actor["id"]))).role == "superadmin"
    assert await _audit_rows(db_session) == []


async def test_a_superadmin_can_demote_another_superadmin(
    user_a: AsyncClient, user_b: AsyncClient, user_c: AsyncClient, db_session: AsyncSession
) -> None:
    a, b = await _me(user_a), await _me(user_b)
    await _me(user_c)
    await _set_role(db_session, a["id"], "superadmin")
    await _set_role(db_session, b["id"], "superadmin")
    response = await user_a.patch(ROLE_URL.format(b["id"]), json={"role": "student"})
    assert response.status_code == 200
    # B lost the role in the database, so B's next team request is refused.
    again = await user_b.patch(ROLE_URL.format(a["id"]), json={"role": "student"})
    assert again.status_code == 403


async def test_unknown_user_and_invalid_role(user_a: AsyncClient, db_session: AsyncSession) -> None:
    actor = await _me(user_a)
    await _set_role(db_session, actor["id"], "superadmin")
    missing = await user_a.patch(ROLE_URL.format(uuid.uuid4()), json={"role": "curator"})
    assert missing.status_code == 404
    assert missing.json()["detail"] == "No existe ese usuario."
    bad = await user_a.patch(ROLE_URL.format(actor["id"]), json={"role": "admin"})
    assert bad.status_code == 422
    assert await _audit_rows(db_session) == []


async def test_the_role_cannot_be_set_through_the_login_claims(
    client: AsyncClient, db_session: AsyncSession, monkeypatch: pytest.MonkeyPatch
) -> None:
    """CO-04: a token claiming a role does not grant it; only the database decides."""
    from app.core import security

    claims = {"uid": "uid-x", "email": "x@example.com", "role": "superadmin", "admin": True}
    monkeypatch.setattr(security, "verify_firebase_token", lambda _t: dict(claims))
    me = await client.get("/api/v1/me", headers={"Authorization": "Bearer x"})
    assert me.json()["role"] == "student"
    response = await client.patch(
        ROLE_URL.format(me.json()["id"]),
        json={"role": "superadmin"},
        headers={"Authorization": "Bearer x"},
    )
    assert response.status_code == 403


async def test_change_and_audit_are_saved_together_or_not_at_all(
    user_a: AsyncClient, user_b: AsyncClient, db_session: AsyncSession, test_engine: AsyncEngine
) -> None:
    """If the transaction does not commit, neither the new role nor its audit row exists."""
    actor_id = uuid.UUID((await _me(user_a))["id"])
    target_id = uuid.UUID((await _me(user_b))["id"])
    await _set_role(db_session, str(actor_id), "superadmin")

    maker = async_sessionmaker(test_engine, expire_on_commit=False)
    async with maker() as session:
        actor = await session.get(User, actor_id)
        _, changed = await change_role(
            session, target_id=target_id, new_role="curator", actor=actor
        )
        assert changed
        await session.rollback()  # e.g. the commit failed

    async with maker() as other:
        assert (await other.get(User, target_id)).role == "student"
        assert await other.scalar(select(func.count()).select_from(AuditLog)) == 0


async def test_two_superadmins_demoting_each_other_cannot_both_win(
    user_a: AsyncClient, user_b: AsyncClient, db_session: AsyncSession, test_engine: AsyncEngine
) -> None:
    """Rows are locked and the actor re-checked: the second demotion is refused (403)."""
    a_id = uuid.UUID((await _me(user_a))["id"])
    b_id = uuid.UUID((await _me(user_b))["id"])
    await _set_role(db_session, str(a_id), "superadmin")
    await _set_role(db_session, str(b_id), "superadmin")

    maker = async_sessionmaker(test_engine, expire_on_commit=False)
    async with maker() as s1, maker() as s2:
        actor_a = await s1.get(User, a_id)
        actor_b = await s2.get(User, b_id)
        await change_role(s1, target_id=b_id, new_role="student", actor=actor_a)
        second = asyncio.create_task(
            change_role(s2, target_id=a_id, new_role="student", actor=actor_b)
        )
        await asyncio.sleep(0.3)
        assert not second.done(), "the second change must wait for the first one's locks"
        await s1.commit()
        with pytest.raises(ActorNotAllowed):
            await asyncio.wait_for(second, timeout=10)
        await s2.rollback()

    db_session.expire_all()
    roles = {u.id: u.role for u in (await db_session.scalars(select(User))).all()}
    assert (roles[a_id], roles[b_id]) == ("superadmin", "student")
    assert len(await _audit_rows(db_session)) == 1


async def test_a_demoted_superadmin_gets_403_even_with_a_stale_user(
    user_a: AsyncClient, user_b: AsyncClient, db_session: AsyncSession, test_engine: AsyncEngine
) -> None:
    """The role is read from the locked row, not from the User object loaded at login.

    The actor object comes from a different session (like the one built by get_current_user),
    so reading `actor.role` instead of the locked row would let the stale superadmin through.
    """
    a_id = uuid.UUID((await _me(user_a))["id"])
    b_id = uuid.UUID((await _me(user_b))["id"])
    await _set_role(db_session, str(a_id), "superadmin")
    maker = async_sessionmaker(test_engine, expire_on_commit=False)
    async with maker() as login_session:
        stale_actor = await login_session.get(User, a_id)  # loaded while still superadmin
    await _set_role(db_session, str(a_id), "student")
    assert stale_actor.role == "superadmin"
    async with maker() as session:
        with pytest.raises(ActorNotAllowed):
            await change_role(session, target_id=b_id, new_role="curator", actor=stale_actor)
        await session.rollback()


async def test_rows_are_locked_in_id_order(
    user_a: AsyncClient, user_b: AsyncClient, db_session: AsyncSession, test_engine: AsyncEngine
) -> None:
    """Deadlock guard: change_role locks the lower id first, whoever the actor is.

    Another session holds the higher-id row. change_role must already hold the lower-id row
    while it waits, which a NOWAIT lock on that row proves.
    """
    a_id = uuid.UUID((await _me(user_a))["id"])
    b_id = uuid.UUID((await _me(user_b))["id"])
    low, high = sorted([a_id, b_id])
    # The actor is the higher id, so "actor first" would wait without holding the lower row.
    await _set_role(db_session, str(high), "superadmin")
    maker = async_sessionmaker(test_engine, expire_on_commit=False)
    lock_row = text("SELECT id FROM users WHERE id = :id FOR UPDATE NOWAIT")
    async with maker() as holder, maker() as worker, maker() as probe:
        await holder.execute(lock_row, {"id": high})
        actor = await worker.get(User, high)
        await worker.commit()
        task = asyncio.create_task(
            change_role(worker, target_id=low, new_role="curator", actor=actor)
        )
        try:
            await asyncio.sleep(0.3)
            assert not task.done(), "change_role must wait for the higher-id row"
            with pytest.raises(Exception, match="could not obtain lock"):
                await probe.execute(lock_row, {"id": low})
        finally:
            await probe.rollback()
            await holder.rollback()
            await asyncio.wait_for(task, timeout=10)
            await worker.rollback()


async def test_api_answers_403_when_the_actor_lost_the_role_meanwhile(
    user_a: AsyncClient, user_b: AsyncClient, db_session: AsyncSession, monkeypatch
) -> None:
    """The route passes require_role, then the service finds the actor demoted: 403, not 500."""
    from app.api.v1 import admin

    actor = await _me(user_a)
    target = await _me(user_b)
    await _set_role(db_session, actor["id"], "superadmin")

    async def demoted_meanwhile(*args, **kwargs):
        raise ActorNotAllowed("actor is not a superadmin")

    monkeypatch.setattr(admin, "change_role", demoted_meanwhile)
    response = await user_a.patch(ROLE_URL.format(target["id"]), json={"role": "curator"})
    assert response.status_code == 403
    assert response.json()["detail"] == "No tienes permisos para esta acción."


def test_require_role_rejects_unknown_role_names() -> None:
    with pytest.raises(ValueError, match="unknown or missing roles"):
        require_role("admin")
    with pytest.raises(ValueError):
        require_role()


async def test_role_errors_never_carry_the_email(db_session: AsyncSession) -> None:
    """NF-07: exception messages may end up in logs (T-003)."""
    with pytest.raises(UserNotFound) as missing:
        await find_user_by_email(db_session, "secreta@example.com")
    db_session.add_all(
        [
            User(firebase_uid="d1", email="dup@example.com"),
            User(firebase_uid="d2", email="dup@example.com"),
        ]
    )
    await db_session.commit()
    with pytest.raises(AmbiguousUser) as dup:
        await find_user_by_email(db_session, "dup@example.com")
    assert "@" not in str(missing.value) + str(dup.value)


def test_record_audit_needs_an_actor_or_a_label() -> None:
    with pytest.raises(ValueError, match="actor_label"):
        record_audit(
            None,  # type: ignore[arg-type]  (fails before touching the session)
            actor=None,
            action="x",
            entity_type="user",
            entity_id="1",
        )


# ---------------------------------------------------------------- set_role script


@pytest.fixture
def script_uses_test_db(monkeypatch: pytest.MonkeyPatch, test_engine: AsyncEngine) -> None:
    class _NoDispose:
        async def dispose(self) -> None:
            return None

    monkeypatch.setattr(
        set_role_script,
        "get_sessionmaker",
        lambda: async_sessionmaker(test_engine, expire_on_commit=False),
    )
    monkeypatch.setattr(set_role_script, "get_engine", lambda: _NoDispose())


async def test_set_role_script_names_the_first_superadmin(
    user_a: AsyncClient,
    db_session: AsyncSession,
    script_uses_test_db: None,
    capsys: pytest.CaptureFixture[str],
) -> None:
    me = await _me(user_a)
    assert await set_role_script.run("A@Example.com", "superadmin") == 0
    db_session.expire_all()
    assert (await db_session.get(User, uuid.UUID(me["id"]))).role == "superadmin"
    [row] = await _audit_rows(db_session)
    assert (row.actor_id, row.actor_label) == (None, "cli")
    assert (row.before, row.after) == ({"role": "student"}, {"role": "superadmin"})
    out = capsys.readouterr()
    assert "a@example.com" not in (out.out + out.err).lower()  # NF-07: no e-mail in output
    # Now that user can use the team route.
    target = await user_a.patch(ROLE_URL.format(me["id"]), json={"role": "superadmin"})
    assert target.status_code == 200


async def test_set_role_script_refuses_unknown_or_ambiguous_emails(
    db_session: AsyncSession, script_uses_test_db: None
) -> None:
    assert await set_role_script.run("nadie@example.com", "superadmin") == 1
    db_session.add_all(
        [
            User(firebase_uid="dup-1", email="dup@example.com"),
            User(firebase_uid="dup-2", email="DUP@example.com"),
        ]
    )
    await db_session.commit()
    assert await set_role_script.run("dup@example.com", "superadmin") == 1
    count = await db_session.scalar(
        select(func.count()).select_from(User).where(User.role == "superadmin")
    )
    assert count == 0
    assert await _audit_rows(db_session) == []


async def test_set_role_script_hides_database_errors(
    script_uses_test_db: None,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """E.g. migrations not applied: a short message, no traceback, SQL or e-mail (NF-07)."""
    from sqlalchemy.exc import ProgrammingError

    async def broken(*_args: object, **_kwargs: object) -> None:
        raise ProgrammingError(
            "SELECT users.role FROM users WHERE lower(users.email) = $1",
            ("secreta@example.com",),
            Exception("column users.role does not exist"),
        )

    monkeypatch.setattr(set_role_script, "find_user_by_email", broken)
    assert await set_role_script.run("secreta@example.com", "superadmin") == 2
    out = capsys.readouterr()
    text_out = out.out + out.err
    assert "docker compose restart backend" in text_out
    assert "@" not in text_out and "SELECT" not in text_out


def test_app_engine_hides_sql_parameters() -> None:
    from app.db.session import get_engine

    assert get_engine().sync_engine.hide_parameters is True


# ---------------------------------------------------------------- migration


PREVIOUS = "7c1d2e3f4a5b"
THIS = "3e8a9b1c2d4f"


def _alembic(url: str, action: str, revision: str) -> None:
    cfg = Config(str(BACKEND_DIR / "alembic.ini"))
    cfg.set_main_option("script_location", str(BACKEND_DIR / "alembic"))
    cfg.set_main_option("sqlalchemy.url", url.replace("%", "%%"))
    getattr(command, action)(cfg, revision)


@pytest_asyncio.fixture
async def migration_db() -> AsyncIterator[tuple[str, AsyncEngine]]:
    """A throwaway database, so moving revisions never touches the shared test database."""
    url = make_url(get_settings().test_database_url)
    url = url.set(database=f"{url.database}_migration")
    url_str = url.render_as_string(hide_password=False)
    await _ensure_database(url_str)
    engine = create_async_engine(url_str, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA public CASCADE"))
        await conn.execute(text("CREATE SCHEMA public"))
    yield url_str, engine
    await engine.dispose()


async def test_migration_maps_admins_to_superadmin_and_back(
    migration_db: tuple[str, AsyncEngine],
) -> None:
    url, engine = migration_db
    await asyncio.to_thread(_alembic, url, "upgrade", PREVIOUS)
    async with engine.begin() as conn:
        await conn.execute(
            text(
                "INSERT INTO users (id, firebase_uid, is_admin) VALUES "
                "(gen_random_uuid(), 'admin', true), (gen_random_uuid(), 'plain', false)"
            )
        )

    await asyncio.to_thread(_alembic, url, "upgrade", THIS)
    async with engine.begin() as conn:
        roles = dict((await conn.execute(text("SELECT firebase_uid, role FROM users"))).all())
        assert roles == {"admin": "superadmin", "plain": "student"}
        cols = {
            r[0]
            for r in await conn.execute(
                text(
                    "SELECT column_name FROM information_schema.columns WHERE table_name = 'users'"
                )
            )
        }
        assert "is_admin" not in cols
        await conn.execute(
            text(
                "INSERT INTO users (id, firebase_uid, role) "
                "VALUES (gen_random_uuid(), 'cur', 'curator')"
            )
        )
        with pytest.raises(Exception, match="ck_users_role"):
            async with conn.begin_nested():
                await conn.execute(
                    text(
                        "INSERT INTO users (id, firebase_uid, role) "
                        "VALUES (gen_random_uuid(), 'bad', 'admin')"
                    )
                )

    # With audit history, the downgrade refuses to run (nothing is lost by accident).
    async with engine.begin() as conn:
        await conn.execute(
            text(
                "INSERT INTO audit_log (id, actor_label, action, entity_type, entity_id) "
                "VALUES (gen_random_uuid(), 'cli', 'user.role_changed', 'user', 'x')"
            )
        )
    with pytest.raises(RuntimeError, match="audit_log has 1 rows"):
        await asyncio.to_thread(_alembic, url, "downgrade", PREVIOUS)
    async with engine.begin() as conn:
        assert (await conn.execute(text("SELECT count(*) FROM audit_log"))).scalar_one() == 1
        await conn.execute(text("DELETE FROM audit_log"))

    await asyncio.to_thread(_alembic, url, "downgrade", PREVIOUS)
    async with engine.begin() as conn:
        admins = dict((await conn.execute(text("SELECT firebase_uid, is_admin FROM users"))).all())
        # Curators become plain users on downgrade (accepted in the T-002 plan).
        assert admins == {"admin": True, "plain": False, "cur": False}
        tables = {
            r[0]
            for r in await conn.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )
        }
        assert "audit_log" not in tables

    await asyncio.to_thread(_alembic, url, "upgrade", "head")
