from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import CatPIStatus, sa_enum


class CatPISession(Base):
    __tablename__ = "cat_pi_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    target_iims = Column(JSON, nullable=True)
    target_percentile = Column(Float, nullable=True)
    status = Column(
        sa_enum(CatPIStatus, "cat_pi_status"),
        nullable=False,
        default=CatPIStatus.IN_PROGRESS,
    )
    finished_at = Column(DateTime(timezone=True), nullable=True)
    overall_score = Column(Float, nullable=True)
    feedback_text = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship(
        "PISessionQuestion",
        back_populates="pi_session",
        cascade="all, delete-orphan",
        order_by="PISessionQuestion.order_index",
    )
