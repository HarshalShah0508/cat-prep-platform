from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.database.database import Base


class ReminderEmailLog(Base):
    __tablename__ = "reminder_email_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reminder_type = Column(String, nullable=False)
    # Session id for event nudges, days-left for exam countdown milestones,
    # null for user-scoped reminders deduped by user_id + reminder_type + time window.
    target_id = Column(Integer, nullable=True)
    sent_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
