"""add marked_for_review/visited to cat_mock_test_questions

Revision ID: 0005
Revises: 0004
Create Date: 2026-10-01

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "cat_mock_test_questions",
        sa.Column("marked_for_review", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "cat_mock_test_questions",
        sa.Column("visited", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_column("cat_mock_test_questions", "visited")
    op.drop_column("cat_mock_test_questions", "marked_for_review")
