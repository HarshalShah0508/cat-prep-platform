from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=True)
    username = Column(String, nullable=False)

    google_id = Column(String, unique=True, nullable=True)
    auth_provider = Column(String(20), nullable=False, default="local")

    is_verified = Column(Boolean, nullable=False, default=False)
    email_verification_otp_hash = Column(String, nullable=True)
    email_verification_otp_expires_at = Column(DateTime(timezone=True), nullable=True)
    password_reset_otp_hash = Column(String, nullable=True)
    password_reset_otp_expires_at = Column(DateTime(timezone=True), nullable=True)

    cat_academic_background = Column(String, nullable=True)
    cat_years_experience_band = Column(String, nullable=True)
    cat_current_company = Column(String, nullable=True)
    cat_target_percentile_min = Column(Float, nullable=True)
    cat_target_percentile_max = Column(Float, nullable=True)
    cat_weak_concepts_flagged_total = Column(Integer, nullable=False, default=0)
    cat_weak_concepts_resolved_total = Column(Integer, nullable=False, default=0)

    last_login_at = Column(DateTime(timezone=True), nullable=True)
    email_opt_out = Column(Boolean, nullable=False, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
