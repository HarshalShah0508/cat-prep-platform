from typing import List, Optional

from pydantic import BaseModel, Field

from app.schemas.cat_feedback import PiFeedbackSurveyOut


class PIQuestionOut(BaseModel):
    id: int
    question_text: str
    order_index: int
    follow_up_depth: int
    parent_question_id: Optional[int] = None
    is_follow_up: bool = False


class PIAnswerOut(BaseModel):
    id: int
    score: Optional[float] = None
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    improvements: Optional[List[str]] = None
    delivery_feedback: Optional[str] = None


class PIQuestionWithAnswerOut(PIQuestionOut):
    answer: Optional[PIAnswerOut] = None


class PIStartRequest(BaseModel):
    resume_id: Optional[int] = None


class PIStartResponse(BaseModel):
    session_id: int
    status: str
    resume_id: Optional[int] = None
    questions: List[PIQuestionOut]


class PISessionDetailResponse(BaseModel):
    id: int
    status: str
    resume_id: Optional[int] = None
    overall_score: Optional[float] = None
    feedback_text: Optional[str] = None
    user_rating: Optional[int] = None
    user_feedback_text: Optional[str] = None
    questions: List[PIQuestionWithAnswerOut]


class PIAnswerRequest(BaseModel):
    pi_session_question_id: int
    answer_text: str
    delivery_signals: Optional[dict] = None


class PIAnswerResponse(BaseModel):
    answer: PIAnswerOut
    eligible_for_follow_up: bool
    model_answer: Optional[str] = None
    session_status: str


class PIFollowUpResponse(BaseModel):
    question: PIQuestionOut


class PIFinishResponse(BaseModel):
    session_id: int
    status: str
    overall_score: Optional[float] = None
    feedback_text: Optional[str] = None


class PISkippedQuestionInfo(BaseModel):
    question_number: int
    topic: str


class PISessionResultsResponse(BaseModel):
    session_id: int
    average_score: float
    questions_attempted: int
    strong_topics: List[str]
    weak_topics: List[str]
    skipped_questions: List[PISkippedQuestionInfo]
    is_finished: bool
    user_rating: Optional[int] = None
    user_feedback_text: Optional[str] = None
    survey: Optional[PiFeedbackSurveyOut] = None


class PIFeedbackRequest(BaseModel):
    rating: int = Field(ge=1, le=5)
    feedback_text: Optional[str] = None
