"""add cat_study_plans table

Revision ID: 0011
Revises: 0010
Create Date: 2026-10-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cat_study_plans",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("source_session_id", sa.Integer(), nullable=True),
        sa.Column("exam_date", sa.Date(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("days", sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["source_session_id"], ["cat_mock_test_sessions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cat_study_plans_id"), "cat_study_plans", ["id"], unique=False)
    op.create_index(op.f("ix_cat_study_plans_user_id"), "cat_study_plans", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cat_study_plans_user_id"), table_name="cat_study_plans")
    op.drop_index(op.f("ix_cat_study_plans_id"), table_name="cat_study_plans")
    op.drop_table("cat_study_plans")
