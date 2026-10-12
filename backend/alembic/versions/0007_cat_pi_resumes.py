"""add cat_pi_resumes table

Revision ID: 0007
Revises: 3831c60f269c
Create Date: 2026-10-12

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0007"
down_revision = "3831c60f269c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cat_pi_resumes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("original_filename", sa.String(), nullable=False),
        sa.Column("extracted_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cat_pi_resumes_id"), "cat_pi_resumes", ["id"], unique=False)
    op.create_index(op.f("ix_cat_pi_resumes_user_id"), "cat_pi_resumes", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cat_pi_resumes_user_id"), table_name="cat_pi_resumes")
    op.drop_index(op.f("ix_cat_pi_resumes_id"), table_name="cat_pi_resumes")
    op.drop_table("cat_pi_resumes")
