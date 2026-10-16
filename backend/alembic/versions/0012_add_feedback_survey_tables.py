"""add cat_mock_test_feedback and cat_pi_feedback survey tables

Revision ID: 0012
Revises: 0011
Create Date: 2026-10-16

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cat_mock_test_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("usefulness_rating", sa.Integer(), nullable=False),
        sa.Column("issues_text", sa.Text(), nullable=True),
        sa.Column("nps_rating", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["session_id"], ["cat_mock_test_sessions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cat_mock_test_feedback_id"), "cat_mock_test_feedback", ["id"], unique=False)
    op.create_index(
        op.f("ix_cat_mock_test_feedback_session_id"),
        "cat_mock_test_feedback",
        ["session_id"],
        unique=True,
    )

    op.create_table(
        "cat_pi_feedback",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("realism_rating", sa.Integer(), nullable=False),
        sa.Column("relevance_rating", sa.Integer(), nullable=False),
        sa.Column("issues_text", sa.Text(), nullable=True),
        sa.Column("nps_rating", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["session_id"], ["cat_pi_sessions.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cat_pi_feedback_id"), "cat_pi_feedback", ["id"], unique=False)
    op.create_index(op.f("ix_cat_pi_feedback_session_id"), "cat_pi_feedback", ["session_id"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_cat_pi_feedback_session_id"), table_name="cat_pi_feedback")
    op.drop_index(op.f("ix_cat_pi_feedback_id"), table_name="cat_pi_feedback")
    op.drop_table("cat_pi_feedback")

    op.drop_index(op.f("ix_cat_mock_test_feedback_session_id"), table_name="cat_mock_test_feedback")
    op.drop_index(op.f("ix_cat_mock_test_feedback_id"), table_name="cat_mock_test_feedback")
    op.drop_table("cat_mock_test_feedback")
