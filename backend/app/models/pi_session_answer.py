from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class PISessionAnswer(Base):
    __tablename__ = "pi_session_answers"

    id = Column(Integer, primary_key=True, index=True)
    pi_session_question_id = Column(
        Integer, ForeignKey("pi_session_questions.id"), nullable=False, unique=True, index=True
    )
    answer_text = Column(Text, nullable=False)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    strengths = Column(JSON, nullable=True)
    improvements = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    question = relationship("PISessionQuestion", back_populates="answer")
