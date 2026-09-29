"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-29

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


cat_section = postgresql.ENUM("VARC", "DILR", "QA", name="cat_section", create_type=False)
cat_question_type = postgresql.ENUM("MCQ", "TITA", name="cat_question_type", create_type=False)
cat_question_source = postgresql.ENUM("pyq", "ai_generated", name="cat_question_source", create_type=False)
cat_test_type = postgresql.ENUM(
    "full_mock", "sectional", "topic_drill", name="cat_test_type", create_type=False
)
cat_mock_test_status = postgresql.ENUM(
    "generating", "ready", "in_progress", "submitted", name="cat_mock_test_status", create_type=False
)
cat_weak_concept_status = postgresql.ENUM(
    "flagged", "drilling", "resolved", name="cat_weak_concept_status", create_type=False
)
cat_pi_status = postgresql.ENUM("in_progress", "finished", name="cat_pi_status", create_type=False)


def upgrade() -> None:
    bind = op.get_bind()

    cat_section.create(bind, checkfirst=True)
    cat_question_type.create(bind, checkfirst=True)
    cat_question_source.create(bind, checkfirst=True)
    cat_test_type.create(bind, checkfirst=True)
    cat_mock_test_status.create(bind, checkfirst=True)
    cat_weak_concept_status.create(bind, checkfirst=True)
    cat_pi_status.create(bind, checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("cat_academic_background", sa.String(), nullable=True),
        sa.Column("cat_target_iims", postgresql.ARRAY(sa.String()), nullable=True),
        sa.Column("cat_target_percentile", sa.Float(), nullable=True),
        sa.Column("cat_weak_concepts_flagged_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("cat_weak_concepts_resolved_total", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "cat_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("section", cat_section, nullable=False),
        sa.Column("question_type", cat_question_type, nullable=False),
        sa.Column("topic", sa.String(), nullable=False),
        sa.Column("difficulty", sa.String(), nullable=False),
        sa.Column("source", cat_question_source, nullable=False),
        sa.Column("source_year", sa.Integer(), nullable=True),
        sa.Column("source_slot", sa.String(), nullable=True),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=True),
        sa.Column("correct_answer", sa.String(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_cat_questions_id", "cat_questions", ["id"])
    op.create_index("ix_cat_questions_section", "cat_questions", ["section"])
    op.create_index("ix_cat_questions_topic", "cat_questions", ["topic"])

    op.create_table(
        "cat_mock_test_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("test_type", cat_test_type, nullable=False),
        sa.Column("sections_included", sa.JSON(), nullable=False),
        sa.Column("status", cat_mock_test_status, nullable=False, server_default="'generating'"),
        sa.Column("section_started_at", sa.JSON(), nullable=True),
        sa.Column("section_submitted_at", sa.JSON(), nullable=True),
        sa.Column("raw_score", sa.Float(), nullable=True),
        sa.Column("percentile_estimate", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_cat_mock_test_sessions_id", "cat_mock_test_sessions", ["id"])
    op.create_index("ix_cat_mock_test_sessions_user_id", "cat_mock_test_sessions", ["user_id"])

    op.create_table(
        "cat_mock_test_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "session_id", sa.Integer(), sa.ForeignKey("cat_mock_test_sessions.id"), nullable=False
        ),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("cat_questions.id"), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("question_snapshot", sa.JSON(), nullable=True),
        sa.Column("selected_answer", sa.String(), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=True),
        sa.Column("marks_awarded", sa.Float(), nullable=True),
        sa.Column("time_spent_seconds", sa.Integer(), nullable=True),
        sa.Column("was_skipped", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_cat_mock_test_questions_id", "cat_mock_test_questions", ["id"])
    op.create_index(
        "ix_cat_mock_test_questions_session_id", "cat_mock_test_questions", ["session_id"]
    )

    op.create_table(
        "cat_weak_concepts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("section", sa.String(), nullable=False),
        sa.Column("concept", sa.String(), nullable=False),
        sa.Column("status", cat_weak_concept_status, nullable=False, server_default="'flagged'"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_cat_weak_concepts_id", "cat_weak_concepts", ["id"])
    op.create_index("ix_cat_weak_concepts_user_id", "cat_weak_concepts", ["user_id"])

    op.create_table(
        "cat_pi_sessions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("target_iims", sa.JSON(), nullable=True),
        sa.Column("target_percentile", sa.Float(), nullable=True),
        sa.Column("status", cat_pi_status, nullable=False, server_default="'in_progress'"),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("overall_score", sa.Float(), nullable=True),
        sa.Column("feedback_text", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_cat_pi_sessions_id", "cat_pi_sessions", ["id"])
    op.create_index("ix_cat_pi_sessions_user_id", "cat_pi_sessions", ["user_id"])

    op.create_table(
        "pi_session_questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("pi_session_id", sa.Integer(), sa.ForeignKey("cat_pi_sessions.id"), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("follow_up_depth", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "parent_question_id",
            sa.Integer(),
            sa.ForeignKey("pi_session_questions.id"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_pi_session_questions_id", "pi_session_questions", ["id"])
    op.create_index(
        "ix_pi_session_questions_pi_session_id", "pi_session_questions", ["pi_session_id"]
    )

    op.create_table(
        "pi_session_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "pi_session_question_id",
            sa.Integer(),
            sa.ForeignKey("pi_session_questions.id"),
            nullable=False,
        ),
        sa.Column("answer_text", sa.Text(), nullable=False),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("feedback", sa.Text(), nullable=True),
        sa.Column("strengths", sa.JSON(), nullable=True),
        sa.Column("improvements", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_pi_session_answers_id", "pi_session_answers", ["id"])
    op.create_index(
        "ix_pi_session_answers_pi_session_question_id",
        "pi_session_answers",
        ["pi_session_question_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_table("pi_session_answers")
    op.drop_table("pi_session_questions")
    op.drop_table("cat_pi_sessions")
    op.drop_table("cat_weak_concepts")
    op.drop_table("cat_mock_test_questions")
    op.drop_table("cat_mock_test_sessions")
    op.drop_table("cat_questions")
    op.drop_table("users")

    bind = op.get_bind()
    cat_pi_status.drop(bind, checkfirst=True)
    cat_weak_concept_status.drop(bind, checkfirst=True)
    cat_mock_test_status.drop(bind, checkfirst=True)
    cat_test_type.drop(bind, checkfirst=True)
    cat_question_source.drop(bind, checkfirst=True)
    cat_question_type.drop(bind, checkfirst=True)
    cat_section.drop(bind, checkfirst=True)
