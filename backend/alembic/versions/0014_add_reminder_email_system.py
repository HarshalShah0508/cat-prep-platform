"""add users.last_login_at/email_opt_out, reminder_email_log table

Revision ID: 0014
Revises: 0013
Create Date: 2026-10-22

"""
from alembic import op
import sqlalchemy as sa

revision = "0014"
down_revision = "0013"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "users",
        sa.Column("email_opt_out", sa.Boolean(), nullable=False, server_default=sa.false()),
    )

    op.create_table(
        "reminder_email_log",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("reminder_type", sa.String(), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=True),
        sa.Column("sent_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reminder_email_log_id"), "reminder_email_log", ["id"])
    op.create_index(op.f("ix_reminder_email_log_user_id"), "reminder_email_log", ["user_id"])
    op.create_index(
        "ix_reminder_email_log_user_id_sent_at", "reminder_email_log", ["user_id", "sent_at"]
    )
    op.create_index(
        "ix_reminder_email_log_type_target", "reminder_email_log", ["reminder_type", "target_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_reminder_email_log_type_target", table_name="reminder_email_log")
    op.drop_index("ix_reminder_email_log_user_id_sent_at", table_name="reminder_email_log")
    op.drop_index(op.f("ix_reminder_email_log_user_id"), table_name="reminder_email_log")
    op.drop_index(op.f("ix_reminder_email_log_id"), table_name="reminder_email_log")
    op.drop_table("reminder_email_log")
    op.drop_column("users", "email_opt_out")
    op.drop_column("users", "last_login_at")
