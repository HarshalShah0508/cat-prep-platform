import json
from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from app.models.cat_mock_test_question import CatMockTestQuestion
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.cat_weak_concept import CatWeakConcept
from app.models.enums import CatMockTestStatus, CatQuestionType, CatTestType, CatWeakConceptStatus
from app.models.user import User
from app.services.gemini_key_manager import gemini_key_manager
from app.services.prompts.cat_question_prompt import build_cat_question_prompt

DRILL_QUESTION_COUNT = 3
DRILL_DIFFICULTY = "medium"


def list_weak_concepts(db: Session, user: User) -> List[CatWeakConcept]:
    return (
        db.query(CatWeakConcept)
        .filter(CatWeakConcept.user_id == user.id)
        .order_by(CatWeakConcept.created_at.desc())
        .all()
    )


def start_drill(db: Session, user: User, weak_concept_id: int) -> CatMockTestSession:
    weak_concept = (
        db.query(CatWeakConcept)
        .filter(CatWeakConcept.id == weak_concept_id, CatWeakConcept.user_id == user.id)
        .first()
    )
    if weak_concept is None:
        raise ValueError("Weak concept not found")

    session = CatMockTestSession(
        user_id=user.id,
        test_type=CatTestType.TOPIC_DRILL,
        sections_included=[weak_concept.section],
        status=CatMockTestStatus.READY,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    question_type = CatQuestionType.MCQ.value
    for order_index in range(DRILL_QUESTION_COUNT):
        prompt = build_cat_question_prompt(
            weak_concept.section, weak_concept.concept, DRILL_DIFFICULTY, question_type
        )
        result = gemini_key_manager.generate_content(
            prompt, purpose=f"weak_concept_drill:{weak_concept.concept}"
        )
        data = json.loads(result) if isinstance(result, str) else result

        snapshot = {
            "section": weak_concept.section,
            "question_type": question_type,
            "topic": data.get("topic", weak_concept.concept),
            "difficulty": data.get("difficulty", DRILL_DIFFICULTY),
            "source": "ai_generated",
            "question_text": data.get("question_text", ""),
            "options": data.get("options"),
            "correct_answer": data.get("correct_answer", ""),
            "explanation": data.get("explanation", ""),
        }
        db.add(
            CatMockTestQuestion(
                session_id=session.id,
                question_id=None,
                order_index=order_index,
                question_snapshot=snapshot,
                was_skipped=False,
            )
        )

    weak_concept.status = CatWeakConceptStatus.DRILLING
    db.add(weak_concept)
    db.commit()
    db.refresh(session)
    return session


def resolve_if_mastered(
    db: Session, weak_concept: CatWeakConcept, drill_session: CatMockTestSession
) -> None:
    """Called after a topic_drill session is submitted: if every question in the drill was
    answered correctly, mark the weak concept resolved; otherwise leave it flagged for retry."""
    questions = drill_session.questions
    if not questions:
        return

    all_correct = all(q.is_correct for q in questions)
    if all_correct:
        weak_concept.status = CatWeakConceptStatus.RESOLVED
        weak_concept.resolved_at = datetime.now(timezone.utc)

        user = db.query(User).filter(User.id == weak_concept.user_id).first()
        if user is not None:
            user.cat_weak_concepts_resolved_total = (user.cat_weak_concepts_resolved_total or 0) + 1
            db.add(user)
    else:
        weak_concept.status = CatWeakConceptStatus.FLAGGED

    db.add(weak_concept)
    db.commit()


def resolve_drill_session(db: Session, session: CatMockTestSession) -> None:
    """Locate the CatWeakConcept a just-submitted topic_drill session was practicing (by
    section + concept, matched against the drill's first question's topic) and resolve it
    if mastered."""
    if session.test_type != CatTestType.TOPIC_DRILL or not session.sections_included:
        return

    section = session.sections_included[0]
    topic = None
    if session.questions and session.questions[0].question_snapshot:
        topic = session.questions[0].question_snapshot.get("topic")

    query = db.query(CatWeakConcept).filter(
        CatWeakConcept.user_id == session.user_id,
        CatWeakConcept.section == section,
        CatWeakConcept.status == CatWeakConceptStatus.DRILLING,
    )
    if topic:
        query = query.filter(CatWeakConcept.concept == topic)

    weak_concept = query.order_by(CatWeakConcept.created_at.desc()).first()
    if weak_concept is not None:
        resolve_if_mastered(db, weak_concept, session)
