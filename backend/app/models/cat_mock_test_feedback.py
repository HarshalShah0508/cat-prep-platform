from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.database.database import Base


class CatMockTestFeedback(Base):
    __tablename__ = "cat_mock_test_feedback"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("cat_mock_test_sessions.id"), nullable=False, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    difficulty = Column(String, nullable=False)
    usefulness_rating = Column(Integer, nullable=False)
    issues_text = Column(Text, nullable=True)
    nps_rating = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
