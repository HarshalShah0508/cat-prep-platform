"""add chart_data to cat_questions

Revision ID: 0004
Revises: 0003
Create Date: 2026-09-30

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cat_questions", sa.Column("chart_data", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("cat_questions", "chart_data")
