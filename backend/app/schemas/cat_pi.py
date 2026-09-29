from typing import List, Optional

from pydantic import BaseModel


class PIQuestionOut(BaseModel):
    id: int
    question_text: str
    order_index: int
    follow_up_depth: int
    parent_question_id: Optional[int] = None


class PIAnswerOut(BaseModel):
    id: int
    score: Optional[float] = None
    feedback: Optional[str] = None
    strengths: Optional[List[str]] = None
    improvements: Optional[List[str]] = None


class PIQuestionWithAnswerOut(PIQuestionOut):
    answer: Optional[PIAnswerOut] = None


class PIStartResponse(BaseModel):
    session_id: int
    status: str
    question: PIQuestionOut


class PISessionDetailResponse(BaseModel):
    id: int
    status: str
    overall_score: Optional[float] = None
    feedback_text: Optional[str] = None
    questions: List[PIQuestionWithAnswerOut]


class PIAnswerRequest(BaseModel):
    pi_session_question_id: int
    answer_text: str


class PIAnswerResponse(BaseModel):
    answer: PIAnswerOut
    next_question: Optional[PIQuestionOut] = None
    session_status: str


class PIFinishResponse(BaseModel):
    session_id: int
    status: str
    overall_score: Optional[float] = None
    feedback_text: Optional[str] = None
