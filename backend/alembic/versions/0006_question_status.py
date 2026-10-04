"""add explicit status to cat_mock_test_questions

Revision ID: 0006
Revises: 0005
Create Date: 2026-10-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "cat_mock_test_questions",
        sa.Column("status", sa.String(), nullable=False, server_default="not_visited"),
    )


def downgrade() -> None:
    op.drop_column("cat_mock_test_questions", "status")
