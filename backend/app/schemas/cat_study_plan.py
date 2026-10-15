from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel


class GeneratePlanRequest(BaseModel):
    source: str
    session_id: Optional[int] = None


class StudyPlanDayOut(BaseModel):
    date: str
    day_number: int
    day_type: str
    section: Optional[str] = None
    topics: List[str] = []
    duration_minutes: int
    note: str


class StudyPlanResponse(BaseModel):
    id: int
    source: str
    source_session_id: Optional[int] = None
    exam_date: date
    generated_at: datetime
    days: List[StudyPlanDayOut]

    class Config:
        from_attributes = True
