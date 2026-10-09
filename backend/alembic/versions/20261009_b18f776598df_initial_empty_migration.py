"""initial empty migration

Revision ID: b18f776598df
Revises:
Create Date: 2026-10-09 17:50:16.030157
"""

from collections.abc import Sequence

revision: str = "b18f776598df"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
