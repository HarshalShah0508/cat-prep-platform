"""separate PYQ paper practice from mock tests

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-30

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

cat_test_type = postgresql.ENUM(
    "full_mock", "sectional", "topic_drill", "pyq_paper", name="cat_test_type", create_type=False
)
cat_question_source_preference = postgresql.ENUM(
    "mixed", "pyq_only", "ai_only", name="cat_question_source_preference", create_type=False
)


def upgrade() -> None:
    bind = op.get_bind()

    # Add the new enum value to the existing cat_test_type type.
    op.execute("ALTER TYPE cat_test_type ADD VALUE IF NOT EXISTS 'pyq_paper'")

    cat_question_source_preference.create(bind, checkfirst=True)

    op.add_column(
        "cat_mock_test_sessions",
        sa.Column(
            "question_source",
            cat_question_source_preference,
            nullable=False,
            server_default="mixed",
        ),
    )
    op.add_column("cat_mock_test_sessions", sa.Column("pyq_source_year", sa.Integer(), nullable=True))
    op.add_column("cat_mock_test_sessions", sa.Column("pyq_source_slot", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("cat_mock_test_sessions", "pyq_source_slot")
    op.drop_column("cat_mock_test_sessions", "pyq_source_year")
    op.drop_column("cat_mock_test_sessions", "question_source")

    bind = op.get_bind()
    cat_question_source_preference.drop(bind, checkfirst=True)
    # Postgres can't drop a single enum value; leaving 'pyq_paper' in cat_test_type on downgrade.
