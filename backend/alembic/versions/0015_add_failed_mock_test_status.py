"""add 'failed' value to cat_mock_test_status enum

Revision ID: 0015
Revises: 0014
Create Date: 2026-11-14

"""
from alembic import op

revision = "0015"
down_revision = "0014"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE cat_mock_test_status ADD VALUE IF NOT EXISTS 'failed'")


def downgrade() -> None:
    # Postgres has no DROP VALUE for enums; leaving 'failed' in the type on
    # downgrade is harmless as long as no row uses it.
    pass
