"""drop target_iims/target_percentile, add years_experience_band/current_company/
target_percentile_min/target_percentile_max to users

Revision ID: 0010
Revises: 0009
Create Date: 2026-10-15

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("cat_years_experience_band", sa.String(), nullable=True))
    op.add_column("users", sa.Column("cat_current_company", sa.String(), nullable=True))
    op.add_column("users", sa.Column("cat_target_percentile_min", sa.Float(), nullable=True))
    op.add_column("users", sa.Column("cat_target_percentile_max", sa.Float(), nullable=True))
    op.drop_column("users", "cat_target_iims")
    op.drop_column("users", "cat_target_percentile")


def downgrade() -> None:
    op.add_column("users", sa.Column("cat_target_percentile", sa.Float(), nullable=True))
    op.add_column(
        "users",
        sa.Column("cat_target_iims", postgresql.ARRAY(sa.String()), nullable=True),
    )
    op.drop_column("users", "cat_target_percentile_max")
    op.drop_column("users", "cat_target_percentile_min")
    op.drop_column("users", "cat_current_company")
    op.drop_column("users", "cat_years_experience_band")
