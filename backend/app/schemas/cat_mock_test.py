from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class MockTestStartRequest(BaseModel):
    test_type: str
    sections: List[str]
    question_source: str = "mixed"


class MockTestStartResponse(BaseModel):
    session_id: int
    status: str


class MockTestStatusResponse(BaseModel):
    status: str


class MockTestQuestionOut(BaseModel):
    id: int
    order_index: int
    section: Optional[str] = None
    question_type: Optional[str] = None
    topic: Optional[str] = None
    difficulty: Optional[str] = None
    group_id: Optional[str] = None
    passage_text: Optional[str] = None
    chart_data: Optional[list] = None
    question_text: str
    options: Optional[List[str]] = None
    selected_answer: Optional[str] = None
    was_skipped: bool = False


class MockTestSectionOut(BaseModel):
    section: str
    time_limit_seconds: int
    questions: List[MockTestQuestionOut]


class MockTestDetailResponse(BaseModel):
    id: int
    test_type: str
    status: str
    question_source: Optional[str] = None
    pyq_source_year: Optional[int] = None
    pyq_source_slot: Optional[str] = None
    sections: List[MockTestSectionOut]
    section_started_at: Optional[Dict[str, str]] = None
    section_submitted_at: Optional[Dict[str, str]] = None


class SectionStartResponse(BaseModel):
    section: str
    started_at: datetime
    deadline: datetime


class AnswerSubmission(BaseModel):
    question_id: int
    selected_answer: Optional[str] = None
    time_spent_seconds: Optional[int] = None
    was_skipped: bool = False


class SectionAnswersRequest(BaseModel):
    answers: List[AnswerSubmission]


class SectionAnswersResponse(BaseModel):
    section: str
    submitted_at: datetime


class SubmitResponse(BaseModel):
    session_id: int
    status: str
    raw_score: Optional[float] = None
    percentile_estimate: Optional[float] = None


class SectionBreakdown(BaseModel):
    section: str
    correct: int
    wrong: int
    skipped: int
    ungraded: int = 0


class ResultQuestionOut(BaseModel):
    id: int
    order_index: int
    section: Optional[str] = None
    group_id: Optional[str] = None
    passage_text: Optional[str] = None
    chart_data: Optional[list] = None
    question_text: str
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    selected_answer: Optional[str] = None
    is_correct: Optional[bool] = None
    marks_awarded: Optional[float] = None


class MockTestResultsResponse(BaseModel):
    id: int
    status: str
    test_type: Optional[str] = None
    pyq_source_year: Optional[int] = None
    pyq_source_slot: Optional[str] = None
    raw_score: Optional[float] = None
    percentile_estimate: Optional[float] = None
    section_breakdown: List[SectionBreakdown]
    questions: List[ResultQuestionOut]
