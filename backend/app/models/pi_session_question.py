from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import backref, relationship
from sqlalchemy.sql import func

from app.database.database import Base


class PISessionQuestion(Base):
    __tablename__ = "pi_session_questions"

    id = Column(Integer, primary_key=True, index=True)
    pi_session_id = Column(Integer, ForeignKey("cat_pi_sessions.id"), nullable=False, index=True)
    question_text = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)
    follow_up_depth = Column(Integer, nullable=False, default=0)
    parent_question_id = Column(Integer, ForeignKey("pi_session_questions.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pi_session = relationship("CatPISession", back_populates="questions")
    answer = relationship(
        "PISessionAnswer",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan",
    )
    children = relationship(
        "PISessionQuestion",
        backref=backref("parent", remote_side=[id]),
    )
