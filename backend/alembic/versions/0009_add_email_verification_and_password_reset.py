"""add email verification and password reset OTP columns to users

Revision ID: 0009
Revises: 0008
Create Date: 2026-10-15

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0009"
down_revision = "0008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_verified", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("users", sa.Column("email_verification_otp_hash", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column("email_verification_otp_expires_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column("users", sa.Column("password_reset_otp_hash", sa.String(), nullable=True))
    op.add_column(
        "users",
        sa.Column("password_reset_otp_expires_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "password_reset_otp_expires_at")
    op.drop_column("users", "password_reset_otp_hash")
    op.drop_column("users", "email_verification_otp_expires_at")
    op.drop_column("users", "email_verification_otp_hash")
    op.drop_column("users", "is_verified")
