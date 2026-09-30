import json
import math
import random
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.cat_mock_test_question import CatMockTestQuestion
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.cat_question import CatQuestion
from app.models.cat_weak_concept import CatWeakConcept
from app.models.enums import (
    CatMockTestStatus,
    CatQuestionSource,
    CatQuestionSourcePreference,
    CatQuestionType,
    CatWeakConceptStatus,
)
from app.models.user import User
from app.services.gemini_key_manager import gemini_key_manager
from app.services.prompts.cat_question_prompt import build_cat_question_prompt

SECTION_QUESTION_COUNTS: Dict[str, int] = {"VARC": 24, "DILR": 22, "QA": 22}
SECTION_TIME_LIMIT_SECONDS = 40 * 60

BANK_SHARE = 0.6

# When a user has no active weak concepts yet, nudge question selection toward the section
# their academic background typically finds hardest.
BACKGROUND_WEAK_SECTION = {
    "engineering": "VARC",
    "commerce": "DILR",
    "humanities": "QA",
}

FALLBACK_TOPICS = {
    "VARC": ["Reading Comprehension", "Para-jumbles", "Paragraph Summary", "Odd Sentence Out"],
    "DILR": ["Data Table Interpretation", "Logical Arrangement", "Data Sufficiency", "Venn Diagrams"],
    "QA": ["Arithmetic", "Algebra", "Number Systems", "Geometry", "Modern Math"],
}

DIFFICULTIES = ["easy", "medium", "hard"]

PERCENTILE_TABLE = [
    (150.0, 99.0),
    (120.0, 95.0),
    (100.0, 90.0),
    (80.0, 80.0),
    (60.0, 65.0),
    (40.0, 45.0),
]
PERCENTILE_FLOOR = 20.0


def estimate_percentile(raw_score: float) -> float:
    """Static heuristic mapping a raw score out of ~204 to an approximate percentile."""
    for threshold, percentile in PERCENTILE_TABLE:
        if raw_score >= threshold:
            return percentile
    return PERCENTILE_FLOOR


def _weak_topics_for_section(db: Session, user: User, section: str) -> List[str]:
    concepts = (
        db.query(CatWeakConcept)
        .filter(
            CatWeakConcept.user_id == user.id,
            CatWeakConcept.section == section,
            CatWeakConcept.status != CatWeakConceptStatus.RESOLVED,
        )
        .all()
    )
    return [c.concept for c in concepts]


def _pick_bank_questions(db: Session, user: User, section: str, count: int) -> List[CatQuestion]:
    """Pick ~`count` bank questions for a section, weighted toward weak concepts /
    background-implied weak sections. Questions sharing a `group_id` (e.g. a DILR set
    with one shared passage across 4-6 questions) are always selected and ordered as a
    whole group - splitting a group would leave the passage's other questions
    unanswerable, so a chosen group may push the total slightly over `count` rather
    than being cut short."""
    if count <= 0:
        return []

    weak_topics = _weak_topics_for_section(db, user, section)
    background_weak_section = BACKGROUND_WEAK_SECTION.get(user.cat_academic_background or "")

    candidates = (
        db.query(CatQuestion)
        .filter(CatQuestion.section == section, CatQuestion.is_active.is_(True))
        .order_by(CatQuestion.id.asc())
        .all()
    )
    if not candidates:
        return []

    def weight(q: CatQuestion) -> float:
        w = 1.0
        if q.source == CatQuestionSource.PYQ:
            w *= 2.0
        if weak_topics:
            if q.topic in weak_topics:
                w *= 3.0
        elif background_weak_section == section:
            w *= 1.5
        return w

    groups: Dict[str, List[CatQuestion]] = {}
    standalone: List[CatQuestion] = []
    for q in candidates:
        if q.group_id:
            groups.setdefault(q.group_id, []).append(q)
        else:
            standalone.append(q)

    # Each "unit" is either a whole group (kept in original order) or a single
    # standalone question; units are weighted by their average member weight.
    units: List[List[CatQuestion]] = [members for members in groups.values()] + [[q] for q in standalone]
    unit_weights = [sum(weight(q) for q in unit) / len(unit) for unit in units]

    pool = list(zip(units, unit_weights))
    random.shuffle(pool)

    selected: List[CatQuestion] = []
    while pool and len(selected) < count:
        total_weight = sum(w for _, w in pool)
        r = random.uniform(0, total_weight)
        upto = 0.0
        chosen_index = len(pool) - 1
        for idx, (_, w) in enumerate(pool):
            upto += w
            if upto >= r:
                chosen_index = idx
                break
        unit, _ = pool.pop(chosen_index)
        selected.extend(unit)

    return selected


def _random_topic(section: str, weak_topics: List[str]) -> str:
    if weak_topics and random.random() < 0.5:
        return random.choice(weak_topics)
    return random.choice(FALLBACK_TOPICS[section])


def _generate_ai_question(section: str, topic: str, difficulty: str, question_type: str) -> dict:
    prompt = build_cat_question_prompt(section, topic, difficulty, question_type)
    result = gemini_key_manager.generate_content(prompt, purpose=f"cat_question:{section}:{topic}")
    return json.loads(result) if isinstance(result, str) else result


def assemble_mock_test(
    db: Session,
    user: User,
    test_type,
    sections: List[str],
    session: Optional[CatMockTestSession] = None,
    question_source: str = CatQuestionSourcePreference.MIXED.value,
) -> CatMockTestSession:
    """Populate `session` (creating one if not given) with a full set of
    CatMockTestQuestion rows for each requested section. `question_source` controls the
    PYQ-bank / AI-generated mix: "mixed" (default) is ~60% bank / ~40% fresh Gemini
    generation, weighted toward weak concepts / background-implied weak sections;
    "pyq_only" pulls entirely from the question bank; "ai_only" generates entirely fresh
    questions via Gemini, skipping the bank."""
    if session is None:
        session = CatMockTestSession(
            user_id=user.id,
            test_type=test_type,
            sections_included=sections,
            question_source=question_source,
            status=CatMockTestStatus.GENERATING,
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    order_index = 0
    for section in sections:
        total_count = SECTION_QUESTION_COUNTS.get(section, 0)

        if question_source == CatQuestionSourcePreference.AI_ONLY.value:
            bank_count = 0
        elif question_source == CatQuestionSourcePreference.PYQ_ONLY.value:
            bank_count = total_count
        else:
            bank_count = math.ceil(total_count * BANK_SHARE)
        ai_count = total_count - bank_count

        bank_questions = _pick_bank_questions(db, user, section, bank_count) if bank_count > 0 else []
        if question_source != CatQuestionSourcePreference.PYQ_ONLY.value and len(bank_questions) < bank_count:
            ai_count += bank_count - len(bank_questions)

        for q in bank_questions:
            db.add(
                CatMockTestQuestion(
                    session_id=session.id,
                    question_id=q.id,
                    order_index=order_index,
                    was_skipped=False,
                )
            )
            order_index += 1

        weak_topics = _weak_topics_for_section(db, user, section)
        for _ in range(ai_count):
            topic = _random_topic(section, weak_topics)
            difficulty = random.choice(DIFFICULTIES)
            question_type = (
                CatQuestionType.TITA.value
                if section == "QA" and random.random() < 0.3
                else CatQuestionType.MCQ.value
            )
            try:
                data = _generate_ai_question(section, topic, difficulty, question_type)
            except Exception:
                continue

            snapshot = {
                "section": section,
                "question_type": question_type,
                "topic": data.get("topic", topic),
                "difficulty": data.get("difficulty", difficulty),
                "source": CatQuestionSource.AI_GENERATED.value,
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
            order_index += 1

    session.status = CatMockTestStatus.READY
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def list_available_pyq_papers(db: Session) -> List[dict]:
    """Distinct (source_year, source_slot) PYQ papers currently in the bank, with a
    per-section question count for each."""
    rows = (
        db.query(
            CatQuestion.source_year,
            CatQuestion.source_slot,
            CatQuestion.section,
        )
        .filter(
            CatQuestion.source == CatQuestionSource.PYQ,
            CatQuestion.source_year.isnot(None),
            CatQuestion.source_slot.isnot(None),
            CatQuestion.is_active.is_(True),
        )
        .all()
    )

    papers: Dict[tuple, Dict[str, int]] = {}
    for source_year, source_slot, section in rows:
        key = (source_year, source_slot)
        section_value = section.value if hasattr(section, "value") else section
        section_counts = papers.setdefault(key, {})
        section_counts[section_value] = section_counts.get(section_value, 0) + 1

    return [
        {"source_year": year, "source_slot": slot, "sections": sections}
        for (year, slot), sections in sorted(papers.items(), key=lambda item: (-item[0][0], item[0][1]))
    ]


def assemble_pyq_paper(
    db: Session,
    session: CatMockTestSession,
    source_year: int,
    source_slot: str,
    sections: Optional[List[str]] = None,
) -> CatMockTestSession:
    """Populate `session` with every bank question for one specific real paper
    (source_year + source_slot), in original order, across the given sections (or every
    section that has data for that paper if none given). Synchronous - no Gemini calls."""
    query = db.query(CatQuestion).filter(
        CatQuestion.source == CatQuestionSource.PYQ,
        CatQuestion.source_year == source_year,
        CatQuestion.source_slot == source_slot,
        CatQuestion.is_active.is_(True),
    )
    if sections:
        query = query.filter(CatQuestion.section.in_(sections))

    questions = query.order_by(CatQuestion.id.asc()).all()

    section_order = list(SECTION_QUESTION_COUNTS.keys())
    found_sections = sorted({q.section.value for q in questions}, key=lambda s: section_order.index(s))
    session.sections_included = found_sections

    for order_index, question in enumerate(questions):
        db.add(
            CatMockTestQuestion(
                session_id=session.id,
                question_id=question.id,
                order_index=order_index,
                was_skipped=False,
            )
        )

    session.status = CatMockTestStatus.READY
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_question_data(mtq: CatMockTestQuestion) -> dict:
    """Normalized view of a CatMockTestQuestion's underlying question, whether it points at
    a bank CatQuestion or carries an inline AI-generated snapshot."""
    if mtq.question is not None:
        q = mtq.question
        return {
            "section": q.section.value,
            "question_type": q.question_type.value,
            "topic": q.topic,
            "difficulty": q.difficulty,
            "group_id": q.group_id,
            "passage_text": q.passage_text,
            "question_text": q.question_text,
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
        }
    snapshot = mtq.question_snapshot or {}
    return {
        "section": snapshot.get("section"),
        "question_type": snapshot.get("question_type"),
        "topic": snapshot.get("topic"),
        "difficulty": snapshot.get("difficulty"),
        "group_id": None,
        "passage_text": None,
        "question_text": snapshot.get("question_text"),
        "options": snapshot.get("options"),
        "correct_answer": snapshot.get("correct_answer"),
        "explanation": snapshot.get("explanation"),
    }


def _flag_weak_concepts(db: Session, user_id: int, wrong_topic_counts: Dict[tuple, int]) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return

    for (section, topic), count in wrong_topic_counts.items():
        if count < 2 or not section or not topic:
            continue

        existing = (
            db.query(CatWeakConcept)
            .filter(
                CatWeakConcept.user_id == user_id,
                CatWeakConcept.section == section,
                CatWeakConcept.concept == topic,
                CatWeakConcept.status != CatWeakConceptStatus.RESOLVED,
            )
            .first()
        )
        if existing:
            continue

        db.add(
            CatWeakConcept(
                user_id=user_id,
                section=section,
                concept=topic,
                status=CatWeakConceptStatus.FLAGGED,
            )
        )
        user.cat_weak_concepts_flagged_total = (user.cat_weak_concepts_flagged_total or 0) + 1

    db.add(user)
    db.commit()


def score_submission(db: Session, session: CatMockTestSession) -> CatMockTestSession:
    wrong_topic_counts: Dict[tuple, int] = {}
    total_score = 0.0

    for mtq in session.questions:
        data = get_question_data(mtq)
        correct_answer_raw = data.get("correct_answer")
        question_type = data.get("question_type")

        if not correct_answer_raw:
            # PYQ loaded before its answer key was transcribed - ungraded, not wrong.
            mtq.marks_awarded = 0.0
            mtq.is_correct = None
        elif mtq.was_skipped or mtq.selected_answer is None:
            mtq.marks_awarded = 0.0
            mtq.is_correct = None
        else:
            correct_answer = correct_answer_raw.strip().lower()
            is_correct = (mtq.selected_answer or "").strip().lower() == correct_answer
            mtq.is_correct = is_correct
            if is_correct:
                mtq.marks_awarded = 3.0
            else:
                mtq.marks_awarded = -1.0 if question_type == CatQuestionType.MCQ.value else 0.0

        total_score += mtq.marks_awarded or 0.0

        if mtq.is_correct is False:
            key = (data.get("section"), data.get("topic"))
            wrong_topic_counts[key] = wrong_topic_counts.get(key, 0) + 1

        db.add(mtq)

    session.raw_score = total_score
    session.percentile_estimate = estimate_percentile(total_score)
    session.status = CatMockTestStatus.SUBMITTED
    db.add(session)
    db.commit()
    db.refresh(session)

    _flag_weak_concepts(db, session.user_id, wrong_topic_counts)

    return session
