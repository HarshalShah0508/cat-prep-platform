from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import CatMockTestStatus, CatTestType, sa_enum


class CatMockTestSession(Base):
    __tablename__ = "cat_mock_test_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    test_type = Column(sa_enum(CatTestType, "cat_test_type"), nullable=False)
    sections_included = Column(JSON, nullable=False)
    status = Column(
        sa_enum(CatMockTestStatus, "cat_mock_test_status"),
        nullable=False,
        default=CatMockTestStatus.GENERATING,
    )
    section_started_at = Column(JSON, nullable=True)
    section_submitted_at = Column(JSON, nullable=True)
    raw_score = Column(Float, nullable=True)
    percentile_estimate = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    questions = relationship(
        "CatMockTestQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="CatMockTestQuestion.order_index",
    )
