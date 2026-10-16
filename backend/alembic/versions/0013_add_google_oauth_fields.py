"""add google_id/auth_provider to users, relax hashed_password to nullable

Revision ID: 0013
Revises: 0012
Create Date: 2026-10-16

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("google_id", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column("auth_provider", sa.String(length=20), nullable=False, server_default="local"),
    )
    op.alter_column("users", "hashed_password", existing_type=sa.String(), nullable=True)
    op.create_unique_constraint("uq_users_google_id", "users", ["google_id"])


def downgrade() -> None:
    op.drop_constraint("uq_users_google_id", "users", type_="unique")
    op.alter_column("users", "hashed_password", existing_type=sa.String(), nullable=False)
    op.drop_column("users", "auth_provider")
    op.drop_column("users", "google_id")
