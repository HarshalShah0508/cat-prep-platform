"""pyq passages: group_id/passage_text on cat_questions, defer answer key

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-30

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("cat_questions", sa.Column("passage_text", sa.Text(), nullable=True))
    op.add_column("cat_questions", sa.Column("group_id", sa.String(), nullable=True))
    op.create_index("ix_cat_questions_group_id", "cat_questions", ["group_id"])

    # PYQ questions are now loaded before their answer key is transcribed, so the
    # answer key columns can no longer be NOT NULL at ingestion time.
    op.alter_column("cat_questions", "correct_answer", existing_type=sa.String(), nullable=True)
    op.alter_column("cat_questions", "explanation", existing_type=sa.Text(), nullable=True)


def downgrade() -> None:
    op.alter_column("cat_questions", "explanation", existing_type=sa.Text(), nullable=False)
    op.alter_column("cat_questions", "correct_answer", existing_type=sa.String(), nullable=False)
    op.drop_index("ix_cat_questions_group_id", table_name="cat_questions")
    op.drop_column("cat_questions", "group_id")
    op.drop_column("cat_questions", "passage_text")
