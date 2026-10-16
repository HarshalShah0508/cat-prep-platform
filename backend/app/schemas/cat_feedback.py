from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class MockTestFeedbackRequest(BaseModel):
    difficulty: Literal["too_easy", "about_right", "too_hard"]
    usefulness_rating: int = Field(ge=1, le=5)
    issues_text: Optional[str] = None
    nps_rating: int = Field(ge=1, le=5)


class MockTestFeedbackOut(BaseModel):
    id: int
    difficulty: str
    usefulness_rating: int
    issues_text: Optional[str] = None
    nps_rating: int
    created_at: datetime

    class Config:
        from_attributes = True


class PiFeedbackSurveyRequest(BaseModel):
    realism_rating: int = Field(ge=1, le=5)
    relevance_rating: int = Field(ge=1, le=5)
    issues_text: Optional[str] = None
    nps_rating: int = Field(ge=1, le=5)


class PiFeedbackSurveyOut(BaseModel):
    id: int
    realism_rating: int
    relevance_rating: int
    issues_text: Optional[str] = None
    nps_rating: int
    created_at: datetime

    class Config:
        from_attributes = True
