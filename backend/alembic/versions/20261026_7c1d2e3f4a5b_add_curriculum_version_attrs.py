"""add curriculum_versions.attrs

Keeps top-level malla fields the model does not represent as columns (official source,
old-plan equivalences, notes about codes) so the import loses nothing.

Revision ID: 7c1d2e3f4a5b
Revises: 4baf1ae8589b
Create Date: 2026-10-26 10:00:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision: str = "7c1d2e3f4a5b"
down_revision: str | None = "4baf1ae8589b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "curriculum_versions",
        sa.Column(
            "attrs",
            postgresql.JSONB(astext_type=sa.Text()),
            server_default=sa.text("'{}'::jsonb"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("curriculum_versions", "attrs")
