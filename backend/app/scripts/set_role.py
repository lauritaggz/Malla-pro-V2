"""Assign a team role from the command line, e.g. to name the first superadmin.

Usage: uv run python -m app.scripts.set_role <email> <student|curator|superadmin>

The user must have signed in at least once (that creates the account). The change is written
to the audit log with actor "cli" (no user performs it through the API).
"""

import argparse
import asyncio
import sys

from sqlalchemy.exc import SQLAlchemyError

from app.db.session import get_engine, get_sessionmaker
from app.models.user import ROLES
from app.services.roles import AmbiguousUser, UserNotFound, change_role, find_user_by_email

ACTOR_LABEL = "cli"


async def run(email: str, role: str) -> int:
    async with get_sessionmaker()() as db:
        try:
            user = await find_user_by_email(db, email)
            _, changed = await change_role(
                db, target_id=user.id, new_role=role, actor=None, actor_label=ACTOR_LABEL
            )
        except UserNotFound:
            print(
                "No hay una cuenta con ese correo. La persona debe iniciar sesión una vez antes.",
                file=sys.stderr,
            )
            return 1
        except AmbiguousUser:
            print("Hay más de una cuenta con ese correo; no se cambió nada.", file=sys.stderr)
            return 1
        except SQLAlchemyError as exc:
            # Short message without the SQL or its parameters (they contain the e-mail, NF-07).
            print(
                f"No se pudo cambiar el rol: error de base de datos ({type(exc).__name__}). "
                "¿Están aplicadas las migraciones? Con Docker: docker compose restart backend",
                file=sys.stderr,
            )
            return 2
        await db.commit()
    await get_engine().dispose()
    print(f"Rol {'actualizado' if changed else 'sin cambios'}: {role}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Asigna un rol del equipo a una cuenta, buscándola por correo."
    )
    parser.add_argument("email", help="correo de la cuenta (debe haber iniciado sesión una vez)")
    parser.add_argument("role", choices=ROLES, help="rol: student, curator o superadmin")
    args = parser.parse_args()
    sys.exit(asyncio.run(run(args.email, args.role)))


if __name__ == "__main__":
    main()
