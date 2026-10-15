from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.rate_limiter import limiter
from app.database.database import get_db
from app.models.cat_pi_resume import CatPIResume
from app.models.cat_pi_session import CatPISession
from app.models.pi_session_answer import PISessionAnswer
from app.models.pi_session_question import PISessionQuestion
from app.models.user import User
from app.schemas.cat_pi import (
    PIAnswerOut,
    PIAnswerRequest,
    PIAnswerResponse,
    PIFeedbackRequest,
    PIFinishResponse,
    PIFollowUpResponse,
    PIQuestionOut,
    PIQuestionWithAnswerOut,
    PISessionDetailResponse,
    PISessionResultsResponse,
    PISkippedQuestionInfo,
    PIStartRequest,
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


def _question_out(question: PISessionQuestion) -> PIQuestionOut:
    return PIQuestionOut(
        id=question.id,
        question_text=question.question_text,
        order_index=question.order_index,
        follow_up_depth=question.follow_up_depth,
        parent_question_id=question.parent_question_id,
        is_follow_up=question.parent_question_id is not None,
    )


def _answer_out(answer: PISessionAnswer) -> PIAnswerOut:
    return PIAnswerOut(
        id=answer.id,
        score=answer.score,
        feedback=answer.feedback,
        strengths=answer.strengths,
        improvements=answer.improvements,
        delivery_feedback=answer.delivery_feedback,
    )


@router.post("/start", response_model=PIStartResponse)
@limiter.limit("15/minute")
def start_pi(
    request: Request,
    response: Response,
    payload: PIStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    resume = None
    if payload.resume_id is not None:
        resume = (
            db.query(CatPIResume)
            .filter(CatPIResume.id == payload.resume_id, CatPIResume.user_id == current_user.id)
            .first()
        )
        if resume is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found")

    try:
        session, questions = cat_pi_service.start_session(db, current_user, resume)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The PI question generator is temporarily unavailable. Please try again in a moment.",
        ) from exc

    return PIStartResponse(
        session_id=session.id,
        status=session.status.value,
        resume_id=session.resume_id,
        questions=[_question_out(q) for q in questions],
    )


@router.get("/{session_id}", response_model=PISessionDetailResponse)
def get_pi_session(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)

    questions_out = []
    for q in sorted(session.questions, key=lambda x: x.order_index):
        answer_out = _answer_out(q.answer) if q.answer is not None else None
        base = _question_out(q)
        questions_out.append(PIQuestionWithAnswerOut(**base.model_dump(), answer=answer_out))

    return PISessionDetailResponse(
        id=session.id,
        status=session.status.value,
        resume_id=session.resume_id,
        overall_score=session.overall_score,
        feedback_text=session.feedback_text,
        user_rating=session.user_rating,
        user_feedback_text=session.user_feedback_text,
        questions=questions_out,
    )


@router.post("/{session_id}/answer", response_model=PIAnswerResponse)
@limiter.limit("15/minute")
def answer_pi_question(
    request: Request,
    response: Response,
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
    if pi_question.answer is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This question has already been answered")

    try:
        answer, eligible_for_follow_up, model_answer = cat_pi_service.submit_answer(
            db, pi_question, payload.answer_text, payload.delivery_signals
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The answer evaluation service is temporarily unavailable. Please try submitting again in a moment.",
        ) from exc

    return PIAnswerResponse(
        answer=_answer_out(answer),
        eligible_for_follow_up=eligible_for_follow_up,
        model_answer=model_answer,
        session_status=session.status.value,
    )


@router.post("/{session_id}/answers/{answer_id}/follow-up", response_model=PIFollowUpResponse)
def follow_up_pi_question(
    session_id: int,
    answer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = _get_owned_session(db, session_id, current_user)

    answer = (
        db.query(PISessionAnswer)
        .join(PISessionQuestion, PISessionAnswer.pi_session_question_id == PISessionQuestion.id)
        .filter(PISessionAnswer.id == answer_id, PISessionQuestion.pi_session_id == session.id)
        .first()
    )
    if answer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found")

    try:
        follow_up = cat_pi_service.generate_follow_up(db, answer)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Could not generate a follow-up question right now. Please try again in a moment.",
        ) from exc

    return PIFollowUpResponse(question=_question_out(follow_up))


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


@router.get("/{session_id}/results", response_model=PISessionResultsResponse)
def get_pi_session_results(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)
    results = cat_pi_service.get_session_results(db, session)

    return PISessionResultsResponse(
        session_id=session.id,
        average_score=results["average_score"],
        questions_attempted=results["questions_attempted"],
        strong_topics=results["strong_topics"],
        weak_topics=results["weak_topics"],
        skipped_questions=[PISkippedQuestionInfo(**s) for s in results["skipped_questions"]],
        is_finished=session.finished_at is not None,
        user_rating=session.user_rating,
        user_feedback_text=session.user_feedback_text,
    )


@router.post("/{session_id}/feedback")
def submit_pi_feedback(
    session_id: int,
    payload: PIFeedbackRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = _get_owned_session(db, session_id, current_user)
    cat_pi_service.submit_session_feedback(db, session, payload.rating, payload.feedback_text)
    return {"saved": True}
