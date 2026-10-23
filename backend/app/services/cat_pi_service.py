import logging
import re
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.models.cat_pi_resume import CatPIResume
from app.models.cat_pi_session import CatPISession
from app.models.enums import CatPIStatus
from app.models.pi_session_answer import PISessionAnswer
from app.models.pi_session_question import PISessionQuestion
from app.models.user import User
from app.services.gemini_key_manager import gemini_key_manager
from app.services.prompts.cat_pi_delivery_feedback_prompt import build_cat_pi_delivery_feedback_prompt
from app.services.prompts.cat_pi_evaluation_prompt import (
    FOLLOW_UP_SCORE_THRESHOLD,
    MAX_FOLLOW_UP_DEPTH,
    PIAnswerEvaluation,
    build_cat_pi_evaluation_prompt,
)
from app.services.prompts.cat_pi_model_answer_prompt import build_cat_pi_model_answer_prompt
from app.services.prompts.cat_pi_prompt import (
    BASE_QUESTION_COUNT,
    build_cat_pi_batch_prompt,
    build_cat_pi_followup_prompt,
)
from app.services.prompts.cat_pi_skipped_topics_prompt import (
    SkippedTopicsResponse,
    build_cat_pi_skipped_topics_prompt,
)

logger = logging.getLogger(__name__)

# Shared enrichment-call budget for the concurrent delivery-feedback/model-answer wave fired
# alongside every answer evaluation - mirrors InterviewAI's ANSWER_ENRICHMENT_TIMEOUT_SECONDS.
ANSWER_ENRICHMENT_TIMEOUT_SECONDS = 12


def _parse_numbered_questions(text: str) -> List[str]:
    """Parses a Gemini batch response like '1. ...\\n2. ...' into individual question
    strings, with the leading 'N. ' numbering stripped."""
    raw_result = text if isinstance(text, str) else str(text)
    chunks = re.findall(r"^\d+\..*?(?=^\d+\.|\Z)", raw_result, flags=re.MULTILINE | re.DOTALL)
    questions = []
    for chunk in chunks:
        cleaned = re.sub(r"^\d+\.\s*", "", chunk.strip(), count=1).strip()
        if cleaned:
            questions.append(cleaned)
    return questions


def start_session(
    db: Session, user: User, resume: Optional[CatPIResume] = None
) -> Tuple[CatPISession, List[PISessionQuestion]]:
    snapshot_percentile = None
    if user.cat_target_percentile_min is not None and user.cat_target_percentile_max is not None:
        snapshot_percentile = (user.cat_target_percentile_min + user.cat_target_percentile_max) / 2

    session = CatPISession(
        user_id=user.id,
        resume_id=resume.id if resume else None,
        target_percentile=snapshot_percentile,
        status=CatPIStatus.IN_PROGRESS,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    resume_text = resume.extracted_text if resume else None
    prompt = build_cat_pi_batch_prompt(
        user.cat_target_percentile_min, user.cat_target_percentile_max, resume_text, count=BASE_QUESTION_COUNT
    )

    try:
        result = gemini_key_manager.generate_content(
            prompt, purpose="cat_pi_batch_questions", user_id=user.id
        )
        question_texts = _parse_numbered_questions(result)
        if not question_texts:
            raise RuntimeError("Gemini returned no parseable PI questions.")
    except Exception:
        db.delete(session)
        db.commit()
        raise

    questions: List[PISessionQuestion] = []
    for index, question_text in enumerate(question_texts):
        question = PISessionQuestion(
            pi_session_id=session.id,
            question_text=question_text,
            order_index=index,
            follow_up_depth=0,
            parent_question_id=None,
        )
        db.add(question)
        questions.append(question)

    db.commit()
    for question in questions:
        db.refresh(question)
    db.refresh(session)

    return session, questions


def _evaluate_answer(
    question_text: str, answer_text: str, user_id: Optional[int] = None
) -> PIAnswerEvaluation:
    prompt = build_cat_pi_evaluation_prompt(question_text, answer_text)
    result = gemini_key_manager.generate_content(
        prompt, response_schema=PIAnswerEvaluation, purpose="cat_pi_evaluation", user_id=user_id
    )
    if isinstance(result, PIAnswerEvaluation):
        return result
    if isinstance(result, str):
        return PIAnswerEvaluation.model_validate_json(result)
    return PIAnswerEvaluation.model_validate(result)


def _generate_delivery_feedback(delivery_signals: dict, user_id: Optional[int] = None) -> Optional[str]:
    try:
        prompt = build_cat_pi_delivery_feedback_prompt(delivery_signals)
        result = gemini_key_manager.generate_content(
            prompt, purpose="cat_pi_delivery_feedback", user_id=user_id
        )
        text = result.strip() if isinstance(result, str) else result
        return text or None
    except Exception as exc:  # noqa: BLE001 - delivery feedback is a soft-fail enrichment
        logger.warning("Delivery feedback generation failed: %s", exc)
        return None


def _generate_model_answer(question_text: str, user_id: Optional[int] = None) -> Optional[str]:
    try:
        prompt = build_cat_pi_model_answer_prompt(question_text)
        result = gemini_key_manager.generate_content(
            prompt, purpose="cat_pi_model_answer", user_id=user_id
        )
        text = result.strip() if isinstance(result, str) else result
        return text or None
    except Exception as exc:  # noqa: BLE001 - model answer is a soft-fail enrichment
        logger.warning("Model answer generation failed: %s", exc)
        return None


def submit_answer(
    db: Session,
    pi_question: PISessionQuestion,
    answer_text: str,
    delivery_signals: Optional[dict] = None,
) -> Tuple[PISessionAnswer, bool, Optional[str]]:
    eval_error: Optional[Exception] = None
    evaluation: Optional[PIAnswerEvaluation] = None
    delivery_feedback: Optional[str] = None
    model_answer: Optional[str] = None
    user_id = pi_question.pi_session.user_id

    wave_start = time.time()
    executor = ThreadPoolExecutor(max_workers=3)
    try:
        eval_future = executor.submit(
            _evaluate_answer, pi_question.question_text, answer_text, user_id
        )
        delivery_future = (
            executor.submit(_generate_delivery_feedback, delivery_signals, user_id)
            if delivery_signals
            else None
        )
        model_answer_future = executor.submit(_generate_model_answer, pi_question.question_text, user_id)

        try:
            evaluation = eval_future.result()
        except Exception as exc:  # noqa: BLE001 - surfaced to the caller below
            eval_error = exc

        def _remaining_budget() -> float:
            elapsed = time.time() - wave_start
            return max(0.1, ANSWER_ENRICHMENT_TIMEOUT_SECONDS - elapsed)

        if delivery_future is not None:
            try:
                delivery_feedback = delivery_future.result(timeout=_remaining_budget())
            except FutureTimeoutError:
                logger.info("Delivery feedback generation timed out")

        try:
            model_answer = model_answer_future.result(timeout=_remaining_budget())
        except FutureTimeoutError:
            logger.info("Model answer generation timed out")
    finally:
        executor.shutdown(wait=False)

    if eval_error is not None:
        raise eval_error

    if evaluation.score >= 7:
        model_answer = None

    eligible_for_follow_up = (
        evaluation.score < FOLLOW_UP_SCORE_THRESHOLD and pi_question.follow_up_depth < MAX_FOLLOW_UP_DEPTH
    )

    answer = PISessionAnswer(
        pi_session_question_id=pi_question.id,
        answer_text=answer_text,
        score=evaluation.score,
        feedback=evaluation.feedback,
        strengths=evaluation.strengths,
        improvements=evaluation.improvements,
        delivery_signals=delivery_signals,
        delivery_feedback=delivery_feedback,
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)

    return answer, eligible_for_follow_up, model_answer


def generate_follow_up(db: Session, answer: PISessionAnswer) -> PISessionQuestion:
    question = answer.question
    session = question.pi_session

    existing = (
        db.query(PISessionQuestion)
        .filter(PISessionQuestion.parent_question_id == question.id)
        .first()
    )
    if existing is not None:
        return existing

    if not (
        answer.score is not None
        and answer.score < FOLLOW_UP_SCORE_THRESHOLD
        and question.follow_up_depth < MAX_FOLLOW_UP_DEPTH
    ):
        raise ValueError("This question is not eligible for a follow-up.")

    evaluation = {
        "score": answer.score,
        "feedback": answer.feedback,
        "strengths": answer.strengths,
        "improvements": answer.improvements,
    }
    prompt = build_cat_pi_followup_prompt(question.question_text, answer.answer_text, evaluation)
    result = gemini_key_manager.generate_content(
        prompt, purpose="cat_pi_followup", user_id=session.user_id
    )
    follow_up_text = result.strip() if isinstance(result, str) else result

    if not follow_up_text:
        raise RuntimeError("Could not generate a follow-up question.")

    total_questions = len(session.questions)
    follow_up = PISessionQuestion(
        pi_session_id=session.id,
        question_text=follow_up_text,
        order_index=total_questions,
        follow_up_depth=question.follow_up_depth + 1,
        parent_question_id=question.id,
    )
    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)
    return follow_up


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


# Question stems that indicate a value is a leaked question/instruction rather than a
# concise concept label - a lightweight safety net on top of the prompt's own instructions.
_QUESTION_STEM_PREFIXES = ("explain", "describe", "what", "how", "why", "define", "discuss", "elaborate")


def _looks_like_concept(raw_concept: str) -> bool:
    text = raw_concept.strip()
    if not text:
        return False
    if re.fullmatch(r"question\s*#?\s*\d+", text, flags=re.IGNORECASE):
        return False
    if text.endswith("?"):
        return False
    if len(text.split()) > 8:
        return False
    first_word = text.split()[0].lower().strip(":,.")
    if first_word in _QUESTION_STEM_PREFIXES:
        return False
    return True


def _track_concept(concepts: Dict[str, dict], raw_concept: str) -> Optional[dict]:
    if not raw_concept or not _looks_like_concept(raw_concept):
        return None
    key = " ".join(raw_concept.strip().split()).lower()
    if key not in concepts:
        concepts[key] = {"display": raw_concept.strip(), "count": 0, "scores": []}
    return concepts[key]


def _build_skipped_questions(
    skipped_main_questions: List[Tuple[int, PISessionQuestion]], user_id: Optional[int] = None
) -> List[dict]:
    if not skipped_main_questions:
        return []

    try:
        prompt = build_cat_pi_skipped_topics_prompt(
            [question.question_text for _, question in skipped_main_questions]
        )
        result = gemini_key_manager.generate_content(
            prompt,
            response_schema=SkippedTopicsResponse,
            purpose="cat_pi_skipped_topics",
            user_id=user_id,
        )
        if isinstance(result, SkippedTopicsResponse):
            topics = result.topics
        elif isinstance(result, str):
            topics = SkippedTopicsResponse.model_validate_json(result).topics
        else:
            topics = SkippedTopicsResponse.model_validate(result).topics
    except Exception as exc:  # noqa: BLE001 - fall back to a generic label per question
        logger.warning("Skipped-topics generation failed: %s", exc)
        topics = []

    return [
        {
            "question_number": question_number,
            "topic": topics[index] if index < len(topics) else "Review This Topic",
        }
        for index, (question_number, _) in enumerate(skipped_main_questions)
    ]


def get_session_results(db: Session, session: CatPISession) -> dict:
    questions = sorted(session.questions, key=lambda q: q.order_index)
    main_questions = [q for q in questions if q.parent_question_id is None]

    skipped_main_questions = [
        (index + 1, question) for index, question in enumerate(main_questions) if question.answer is None
    ]
    skipped_questions = _build_skipped_questions(skipped_main_questions, user_id=session.user_id)

    answered_questions = [q for q in questions if q.answer is not None]

    if not answered_questions:
        return {
            "average_score": 0.0,
            "questions_attempted": 0,
            "strong_topics": [],
            "weak_topics": [],
            "skipped_questions": skipped_questions,
        }

    total_score = 0.0
    strength_concepts: Dict[str, dict] = {}
    weak_concepts: Dict[str, dict] = {}

    for question in answered_questions:
        answer = question.answer
        total_score += answer.score or 0

        for concept in answer.strengths or []:
            entry = _track_concept(strength_concepts, concept)
            if entry:
                entry["count"] += 1

        for concept in answer.improvements or []:
            entry = _track_concept(weak_concepts, concept)
            if entry:
                entry["count"] += 1
                entry["scores"].append(answer.score or 0)

    strong_topics = [
        entry["display"] for entry in sorted(strength_concepts.values(), key=lambda entry: -entry["count"])
    ]
    weak_topics = [
        entry["display"]
        for entry in sorted(
            weak_concepts.values(),
            key=lambda entry: (-entry["count"], sum(entry["scores"]) / len(entry["scores"])),
        )
    ]

    return {
        "average_score": round(total_score / len(answered_questions), 2),
        "questions_attempted": len(answered_questions),
        "strong_topics": strong_topics,
        "weak_topics": weak_topics,
        "skipped_questions": skipped_questions,
    }


def submit_session_feedback(
    db: Session, session: CatPISession, rating: int, feedback_text: Optional[str]
) -> CatPISession:
    session.user_rating = rating
    session.user_feedback_text = feedback_text
    db.add(session)
    db.commit()
    db.refresh(session)
    return session
