from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import CatWeakConceptStatus, sa_enum


class CatWeakConcept(Base):
    __tablename__ = "cat_weak_concepts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    section = Column(String, nullable=False)
    concept = Column(String, nullable=False)
    status = Column(
        sa_enum(CatWeakConceptStatus, "cat_weak_concept_status"),
        nullable=False,
        default=CatWeakConceptStatus.FLAGGED,
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)
