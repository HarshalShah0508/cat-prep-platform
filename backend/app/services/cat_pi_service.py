import json
from datetime import datetime, timezone
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.cat_pi_session import CatPISession
from app.models.enums import CatPIStatus
from app.models.pi_session_answer import PISessionAnswer
from app.models.pi_session_question import PISessionQuestion
from app.models.user import User
from app.services.gemini_key_manager import gemini_key_manager
from app.services.prompts.cat_pi_evaluation_prompt import (
    FOLLOW_UP_SCORE_THRESHOLD,
    MAX_FOLLOW_UP_DEPTH,
    PIAnswerEvaluation,
    build_cat_pi_evaluation_prompt,
)
from app.services.prompts.cat_pi_prompt import build_cat_pi_followup_prompt, build_cat_pi_prompt

MAX_TOTAL_QUESTIONS = 8


def _history(session: CatPISession) -> List[Tuple[str, str]]:
    pairs = []
    for q in sorted(session.questions, key=lambda x: x.order_index):
        if q.answer is not None:
            pairs.append((q.question_text, q.answer.answer_text))
    return pairs


def _generate_question_text(target_iims, history: List[Tuple[str, str]]) -> str:
    prompt = build_cat_pi_prompt(target_iims, None, history)
    result = gemini_key_manager.generate_content(prompt, purpose="cat_pi_question")
    data = json.loads(result) if isinstance(result, str) else result
    return data.get("question_text", "Tell me about yourself.")


def start_session(db: Session, user: User) -> Tuple[CatPISession, PISessionQuestion]:
    session = CatPISession(
        user_id=user.id,
        target_iims=user.cat_target_iims,
        target_percentile=user.cat_target_percentile,
        status=CatPIStatus.IN_PROGRESS,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    question_text = _generate_question_text(user.cat_target_iims, [])
    question = PISessionQuestion(
        pi_session_id=session.id,
        question_text=question_text,
        order_index=0,
        follow_up_depth=0,
        parent_question_id=None,
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    db.refresh(session)
    return session, question


def _evaluate_answer(question_text: str, answer_text: str) -> PIAnswerEvaluation:
    prompt = build_cat_pi_evaluation_prompt(question_text, answer_text)
    result = gemini_key_manager.generate_content(
        prompt, response_schema=PIAnswerEvaluation, purpose="cat_pi_evaluation"
    )
    if isinstance(result, PIAnswerEvaluation):
        return result
    if isinstance(result, str):
        return PIAnswerEvaluation.model_validate_json(result)
    return PIAnswerEvaluation.model_validate(result)


def submit_answer(
    db: Session, pi_question: PISessionQuestion, answer_text: str
) -> Tuple[PISessionAnswer, Optional[PISessionQuestion]]:
    evaluation = _evaluate_answer(pi_question.question_text, answer_text)

    answer = PISessionAnswer(
        pi_session_question_id=pi_question.id,
        answer_text=answer_text,
        score=evaluation.score,
        feedback=evaluation.feedback,
        strengths=evaluation.strengths,
        improvements=evaluation.improvements,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)

    session = pi_question.pi_session
    db.refresh(session)
    total_questions = len(session.questions)

    next_question: Optional[PISessionQuestion] = None

    if total_questions >= MAX_TOTAL_QUESTIONS:
        session.status = CatPIStatus.FINISHED
        session.finished_at = datetime.now(timezone.utc)
        db.add(session)
        db.commit()
    elif evaluation.score < FOLLOW_UP_SCORE_THRESHOLD and pi_question.follow_up_depth < MAX_FOLLOW_UP_DEPTH:
        followup_prompt = build_cat_pi_followup_prompt(pi_question.question_text, answer_text)
        result = gemini_key_manager.generate_content(followup_prompt, purpose="cat_pi_followup")
        data = json.loads(result) if isinstance(result, str) else result
        next_question = PISessionQuestion(
            pi_session_id=session.id,
            question_text=data.get("question_text", "Can you elaborate further on that?"),
            order_index=total_questions,
            follow_up_depth=pi_question.follow_up_depth + 1,
            parent_question_id=pi_question.id,
        )
        db.add(next_question)
        db.commit()
        db.refresh(next_question)
    else:
        history = _history(session)
        question_text = _generate_question_text(session.target_iims, history)
        next_question = PISessionQuestion(
            pi_session_id=session.id,
            question_text=question_text,
            order_index=total_questions,
            follow_up_depth=0,
            parent_question_id=None,
        )
        db.add(next_question)
        db.commit()
        db.refresh(next_question)

    db.refresh(session)
    return answer, next_question


def finish_session(db: Session, session: CatPISession) -> CatPISession:
    scores = [
        q.answer.score for q in session.questions if q.answer is not None and q.answer.score is not None
    ]
    overall_score = sum(scores) / len(scores) if scores else None

    session.overall_score = overall_score
    session.status = CatPIStatus.FINISHED
    if session.finished_at is None:
        session.finished_at = datetime.now(timezone.utc)

    if overall_score is not None:
        if overall_score >= 8:
            summary = "Strong performance overall — confident, well-structured answers."
        elif overall_score >= 6:
            summary = "Solid performance with some areas that could be sharper."
        elif overall_score >= 4:
            summary = "Mixed performance — several answers need more depth and structure."
        else:
            summary = "Weak performance overall — focus on clarity, substance, and structure."
        session.feedback_text = summary

    db.add(session)
    db.commit()
    db.refresh(session)
    return session
