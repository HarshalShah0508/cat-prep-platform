from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class CatMockTestQuestion(Base):
    __tablename__ = "cat_mock_test_questions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("cat_mock_test_sessions.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("cat_questions.id"), nullable=True)
    order_index = Column(Integer, nullable=False)
    question_snapshot = Column(JSON, nullable=True)
    selected_answer = Column(String, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    marks_awarded = Column(Float, nullable=True)
    time_spent_seconds = Column(Integer, nullable=True)
    was_skipped = Column(Boolean, nullable=False, default=False)

    session = relationship("CatMockTestSession", back_populates="questions")
    question = relationship("CatQuestion")
