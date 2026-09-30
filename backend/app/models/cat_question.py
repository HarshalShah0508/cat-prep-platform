from sqlalchemy import Boolean, Column, DateTime, Integer, JSON, String, Text
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import CatQuestionSource, CatQuestionType, CatSection, sa_enum


class CatQuestion(Base):
    __tablename__ = "cat_questions"

    id = Column(Integer, primary_key=True, index=True)
    section = Column(sa_enum(CatSection, "cat_section"), nullable=False, index=True)
    question_type = Column(sa_enum(CatQuestionType, "cat_question_type"), nullable=False)
    topic = Column(String, nullable=False, index=True)
    difficulty = Column(String, nullable=False)
    source = Column(sa_enum(CatQuestionSource, "cat_question_source"), nullable=False)
    source_year = Column(Integer, nullable=True)
    source_slot = Column(String, nullable=True)
    passage_text = Column(Text, nullable=True)
    # Structured chart data for DI sets where the source is a graph rather than a
    # table (e.g. step-line charts) - a list of {title, x_label, y_label, series:
    # [{name, color, points: [[x,y], ...]}]} objects, rendered client-side instead
    # of embedding a copied chart image.
    chart_data = Column(JSON, nullable=True)
    group_id = Column(String, nullable=True, index=True)
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=True)
    correct_answer = Column(String, nullable=True)
    explanation = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
