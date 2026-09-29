from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cat_pi_session import CatPISession
from app.models.pi_session_question import PISessionQuestion
from app.models.user import User
from app.schemas.cat_pi import (
    PIAnswerOut,
    PIAnswerRequest,
    PIAnswerResponse,
    PIFinishResponse,
    PIQuestionOut,
    PIQuestionWithAnswerOut,
    PISessionDetailResponse,
    PIStartResponse,
)
from app.services import cat_pi_service
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/cat/pi", tags=["cat-pi"])


def _get_owned_session(db: Session, session_id: int, current_user: User) -> CatPISession:
    session = (
        db.query(CatPISession)
        .filter(CatPISession.id == session_id, CatPISession.user_id == current_user.id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PI session not found")
    return session


@router.post("/start", response_model=PIStartResponse)
def start_pi(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    session, first_question = cat_pi_service.start_session(db, current_user)
    return PIStartResponse(
        session_id=session.id,
        status=session.status.value,
        question=PIQuestionOut(
            id=first_question.id,
            question_text=first_question.question_text,
            order_index=first_question.order_index,
            follow_up_depth=first_question.follow_up_depth,
            parent_question_id=first_question.parent_question_id,
        ),
    )


@router.get("/{session_id}", response_model=PISessionDetailResponse)
def get_pi_session(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)

    questions_out = []
    for q in sorted(session.questions, key=lambda x: x.order_index):
        answer_out = None
        if q.answer is not None:
            answer_out = PIAnswerOut(
                id=q.answer.id,
                score=q.answer.score,
                feedback=q.answer.feedback,
                strengths=q.answer.strengths,
                improvements=q.answer.improvements,
            )
        questions_out.append(
            PIQuestionWithAnswerOut(
                id=q.id,
                question_text=q.question_text,
                order_index=q.order_index,
                follow_up_depth=q.follow_up_depth,
                parent_question_id=q.parent_question_id,
                answer=answer_out,
            )
        )

    return PISessionDetailResponse(
        id=session.id,
        status=session.status.value,
        overall_score=session.overall_score,
        feedback_text=session.feedback_text,
        questions=questions_out,
    )


@router.post("/{session_id}/answer", response_model=PIAnswerResponse)
def answer_pi_question(
    session_id: int,
    payload: PIAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = _get_owned_session(db, session_id, current_user)

    pi_question = (
        db.query(PISessionQuestion)
        .filter(
            PISessionQuestion.id == payload.pi_session_question_id,
            PISessionQuestion.pi_session_id == session.id,
        )
        .first()
    )
    if pi_question is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")

    answer, next_question = cat_pi_service.submit_answer(db, pi_question, payload.answer_text)
    db.refresh(session)

    next_question_out = None
    if next_question is not None:
        next_question_out = PIQuestionOut(
            id=next_question.id,
            question_text=next_question.question_text,
            order_index=next_question.order_index,
            follow_up_depth=next_question.follow_up_depth,
            parent_question_id=next_question.parent_question_id,
        )

    return PIAnswerResponse(
        answer=PIAnswerOut(
            id=answer.id,
            score=answer.score,
            feedback=answer.feedback,
            strengths=answer.strengths,
            improvements=answer.improvements,
        ),
        next_question=next_question_out,
        session_status=session.status.value,
    )


@router.post("/{session_id}/finish", response_model=PIFinishResponse)
def finish_pi(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)
    session = cat_pi_service.finish_session(db, session)
    return PIFinishResponse(
        session_id=session.id,
        status=session.status.value,
        overall_score=session.overall_score,
        feedback_text=session.feedback_text,
    )
