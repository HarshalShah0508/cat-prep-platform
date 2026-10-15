from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.sql import func

from app.database.database import Base


class CatStudyPlan(Base):
    __tablename__ = "cat_study_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    source = Column(String, nullable=False)
    source_session_id = Column(Integer, ForeignKey("cat_mock_test_sessions.id"), nullable=True)
    exam_date = Column(Date, nullable=False)
    generated_at = Column(DateTime(timezone=True), server_default=func.now())
    days = Column(JSON, nullable=False)
