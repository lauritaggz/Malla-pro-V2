"""user roles and audit log (T-002)

users.is_admin is replaced by users.role (student / curator / superadmin): admins become
superadmin. Downgrade maps superadmin back to is_admin = true; curators become plain users
(the old model had no curator), which Laura accepted on 2026-10-30. Downgrade refuses to run
while audit_log has rows, so the audit history is never lost by accident.

Revision ID: 3e8a9b1c2d4f
Revises: 7c1d2e3f4a5b
Create Date: 2026-10-30 15:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "3e8a9b1c2d4f"
down_revision: str | None = "7c1d2e3f4a5b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("role", sa.String(length=16), server_default="student", nullable=False),
    )
    op.create_check_constraint(
        "ck_users_role", "users", "role IN ('student', 'curator', 'superadmin')"
    )
    op.execute("UPDATE users SET role = 'superadmin' WHERE is_admin")
    op.drop_column("users", "is_admin")

    op.create_table(
        "audit_log",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("actor_id", sa.Uuid(), nullable=True),
        sa.Column("actor_label", sa.String(length=64), nullable=True),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("entity_type", sa.String(length=64), nullable=False),
        sa.Column("entity_id", sa.String(length=64), nullable=False),
        sa.Column("before", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("after", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["actor_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_audit_log_actor_id", "audit_log", ["actor_id"])
    op.create_index("ix_audit_log_entity", "audit_log", ["entity_type", "entity_id"])
    op.create_index("ix_audit_log_created_at", "audit_log", ["created_at"])


def downgrade() -> None:
    # Never drop the team's audit history silently (NF-11). Export it first, then empty the
    # table on purpose if the downgrade is really needed.
    bind = op.get_bind()
    # Lock first, so no row can be added between the count and the drop.
    bind.execute(sa.text("LOCK TABLE audit_log IN ACCESS EXCLUSIVE MODE"))
    rows = bind.execute(sa.text("SELECT count(*) FROM audit_log")).scalar_one()
    if rows:
        raise RuntimeError(
            f"audit_log has {rows} rows: export them and empty the table before downgrading"
        )
    op.drop_index("ix_audit_log_created_at", table_name="audit_log")
    op.drop_index("ix_audit_log_entity", table_name="audit_log")
    op.drop_index("ix_audit_log_actor_id", table_name="audit_log")
    op.drop_table("audit_log")

    op.add_column(
        "users",
        sa.Column("is_admin", sa.Boolean(), server_default=sa.text("false"), nullable=False),
    )
    op.execute("UPDATE users SET is_admin = (role = 'superadmin')")
    op.drop_constraint("ck_users_role", "users", type_="check")
    op.drop_column("users", "role")
