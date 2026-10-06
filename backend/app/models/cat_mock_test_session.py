from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import (
    CatMockTestStatus,
    CatQuestionSourcePreference,
    CatTestType,
    sa_enum,
)


class CatMockTestSession(Base):
    __tablename__ = "cat_mock_test_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    test_type = Column(sa_enum(CatTestType, "cat_test_type"), nullable=False)
    sections_included = Column(JSON, nullable=False)
    question_source = Column(
        sa_enum(CatQuestionSourcePreference, "cat_question_source_preference"),
        nullable=False,
        default=CatQuestionSourcePreference.MIXED,
    )
    # Only set for test_type=pyq_paper - which exact paper this session replays.
    pyq_source_year = Column(Integer, nullable=True)
    pyq_source_slot = Column(String, nullable=True)
    # Only set for a user-driven custom topic practice session (QA only for now) -
    # the topics picked and whether to generate harder, multi-step, non-direct
    # questions ("challenging") instead of the default style ("standard").
    topics = Column(JSON, nullable=True)
    question_style = Column(String, nullable=True, default="standard")
    question_count = Column(Integer, nullable=True)
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
