from sqlalchemy import ARRAY, Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String, nullable=False)

    cat_academic_background = Column(String, nullable=True)
    cat_target_iims = Column(ARRAY(String), nullable=True)
    cat_target_percentile = Column(Float, nullable=True)
    cat_weak_concepts_flagged_total = Column(Integer, nullable=False, default=0)
    cat_weak_concepts_resolved_total = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
