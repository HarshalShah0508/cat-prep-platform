"""add resume_id/user_rating/user_feedback_text to cat_pi_sessions,
delivery_signals/delivery_feedback to pi_session_answers

Revision ID: 0008
Revises: 0007
Create Date: 2026-10-12

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0008"
down_revision = "0007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cat_pi_sessions", sa.Column("resume_id", sa.Integer(), nullable=True))
    op.add_column("cat_pi_sessions", sa.Column("user_rating", sa.Integer(), nullable=True))
    op.add_column("cat_pi_sessions", sa.Column("user_feedback_text", sa.Text(), nullable=True))
    op.create_foreign_key(
        "fk_cat_pi_sessions_resume_id",
        "cat_pi_sessions",
        "cat_pi_resumes",
        ["resume_id"],
        ["id"],
    )

    op.add_column("pi_session_answers", sa.Column("delivery_signals", sa.JSON(), nullable=True))
    op.add_column("pi_session_answers", sa.Column("delivery_feedback", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("pi_session_answers", "delivery_feedback")
    op.drop_column("pi_session_answers", "delivery_signals")

    op.drop_constraint("fk_cat_pi_sessions_resume_id", "cat_pi_sessions", type_="foreignkey")
    op.drop_column("cat_pi_sessions", "user_feedback_text")
    op.drop_column("cat_pi_sessions", "user_rating")
    op.drop_column("cat_pi_sessions", "resume_id")
