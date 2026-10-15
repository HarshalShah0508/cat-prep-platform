from datetime import date, timedelta
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from app.models.cat_mock_test_session import CatMockTestSession
from app.models.cat_study_plan import CatStudyPlan
from app.models.cat_weak_concept import CatWeakConcept
from app.models.enums import CatMockTestStatus, CatTestType, CatWeakConceptStatus
from app.models.user import User
from app.services.cat_mock_test_service import (
    TOPIC_OPTIONS_BY_SECTION,
    compute_session_topic_stats,
)

EXAM_DATE = date(2026, 11, 29)  # hardcoded CAT exam date - update here for future years

TAPER_DAYS_DEFAULT = 3
WEAK_RATIO = 0.60
STRONG_RATIO = 0.25
MOCK_RATIO = 0.15
MIN_SECTION_WEIGHT = 0.15

SECTIONS = ["VARC", "DILR", "QA"]


def _topic_stats_from_session(session: CatMockTestSession) -> Dict[str, dict]:
    raw_stats = compute_session_topic_stats(session)
    sections_included = set(session.sections_included or [])

    result = {}
    for section in SECTIONS:
        if section not in sections_included:
            result[section] = {
                "weak_topics": [],
                "strong_topics": [],
                "has_data": False,
                "error_rate": None,
            }
            continue

        topics = raw_stats.get(section, {})
        weak = sorted(
            (topic for topic, c in topics.items() if c["wrong"] >= 1),
            key=lambda t: topics[t]["wrong"],
            reverse=True,
        )
        strong = [topic for topic, c in topics.items() if c["correct"] >= 1 and c["wrong"] == 0]
        wrong_total = sum(c["wrong"] for c in topics.values())
        correct_total = sum(c["correct"] for c in topics.values())
        error_rate = wrong_total / (wrong_total + correct_total) if (wrong_total + correct_total) else 0.0

        result[section] = {
            "weak_topics": weak,
            "strong_topics": strong,
            "has_data": True,
            "error_rate": error_rate,
        }

    return result


def _topic_stats_from_history(db: Session, user: User) -> Dict[str, dict]:
    sessions = (
        db.query(CatMockTestSession)
        .filter(
            CatMockTestSession.user_id == user.id,
            CatMockTestSession.status == CatMockTestStatus.SUBMITTED,
            CatMockTestSession.test_type != CatTestType.TOPIC_DRILL,
        )
        .all()
    )
    if not sessions:
        raise ValueError("No mock test history yet - take at least one mock test first.")

    aggregate: Dict[str, Dict[str, Dict[str, int]]] = {}
    for session in sessions:
        session_stats = compute_session_topic_stats(session)
        for section, topics in session_stats.items():
            section_agg = aggregate.setdefault(section, {})
            for topic, counts in topics.items():
                topic_agg = section_agg.setdefault(topic, {"correct": 0, "wrong": 0})
                topic_agg["correct"] += counts["correct"]
                topic_agg["wrong"] += counts["wrong"]

    weak_concepts = (
        db.query(CatWeakConcept)
        .filter(
            CatWeakConcept.user_id == user.id,
            CatWeakConcept.status != CatWeakConceptStatus.RESOLVED,
        )
        .order_by(CatWeakConcept.created_at.asc())
        .all()
    )

    result = {}
    for section in SECTIONS:
        weak = [wc.concept for wc in weak_concepts if wc.section == section]
        topics = aggregate.get(section, {})
        strong = [
            topic
            for topic, c in topics.items()
            if c["correct"] >= 1 and c["wrong"] == 0 and topic not in weak
        ]
        has_data = bool(topics)
        wrong_total = sum(c["wrong"] for c in topics.values())
        correct_total = sum(c["correct"] for c in topics.values())
        error_rate = wrong_total / (wrong_total + correct_total) if (wrong_total + correct_total) else 0.0

        result[section] = {
            "weak_topics": weak,
            "strong_topics": strong,
            "has_data": has_data,
            "error_rate": error_rate if has_data else None,
        }

    return result


def _apply_fallback(section_stats: Dict[str, dict]) -> Dict[str, dict]:
    """A section with no diagnostic data gets the full canonical topic list for both its
    weak and strong rotation - we don't know yet whether it's weak or strong, so give it
    broad, even baseline coverage instead of skipping it."""
    for section, stats in section_stats.items():
        if not stats["has_data"]:
            baseline = list(TOPIC_OPTIONS_BY_SECTION.get(section, ["General practice"]))
            stats["weak_topics"] = baseline
            stats["strong_topics"] = baseline
    return section_stats


def _deficit_round_robin(ratios: Dict[str, float], total: int) -> List[str]:
    """Spreads `total` slots across the keys of `ratios` as evenly as the ratios allow,
    instead of bunching all of one type together - at each step picks the type with the
    largest gap between its target share-so-far and what it's actually received so far."""
    if total <= 0:
        return []

    assigned = {k: 0 for k in ratios}
    sequence = []
    for i in range(1, total + 1):
        best_key = max(ratios, key=lambda k: ratios[k] * i - assigned[k])
        assigned[best_key] += 1
        sequence.append(best_key)
    return sequence


def _section_quota(weights: Dict[str, float], total: int) -> Dict[str, int]:
    """Splits `total` slots across sections proportional to `weights`, rounding so the
    quotas always sum exactly to `total` (remainder goes to the heaviest-weighted section)."""
    if total <= 0:
        return {k: 0 for k in weights}

    total_weight = sum(weights.values()) or 1.0
    normalized = {k: v / total_weight for k, v in weights.items()}
    quotas = {k: round(v * total) for k, v in normalized.items()}

    diff = total - sum(quotas.values())
    if diff != 0:
        adjust_key = max(normalized, key=normalized.get)
        quotas[adjust_key] += diff

    return quotas


def _next_section_with_quota(quota: Dict[str, int], cursor: Dict[str, int]) -> Optional[str]:
    """Round-robins across sections that still have quota remaining, so a day-type's slots
    don't all go to one section back-to-back even when quotas are uneven."""
    remaining = [s for s in SECTIONS if quota.get(s, 0) > 0]
    if not remaining:
        return None

    order_idx = cursor["_pos"] % len(SECTIONS)
    for offset in range(len(SECTIONS)):
        candidate = SECTIONS[(order_idx + offset) % len(SECTIONS)]
        if quota.get(candidate, 0) > 0:
            cursor["_pos"] += offset + 1
            quota[candidate] -= 1
            return candidate
    return None


def _build_days(section_stats: Dict[str, dict], today: date, exam_date: date) -> List[dict]:
    total_days = (exam_date - today).days
    if total_days <= 0:
        raise ValueError("Exam date has passed - cannot generate a plan.")

    taper_days = min(TAPER_DAYS_DEFAULT, max(total_days - 5, 0))
    pool_days = total_days - taper_days

    weak_days = round(pool_days * WEAK_RATIO)
    mock_days = round(pool_days * MOCK_RATIO)
    strong_days = pool_days - weak_days - mock_days

    weak_weights = {}
    for section in SECTIONS:
        error_rate = section_stats[section]["error_rate"]
        weak_weights[section] = MIN_SECTION_WEIGHT + (error_rate or 0.33) * (1 - MIN_SECTION_WEIGHT)

    weak_quota = _section_quota(weak_weights, weak_days)
    strong_quota = _section_quota({s: 1.0 for s in SECTIONS}, strong_days)

    exact_counts = {"weak_focus": weak_days, "strong_revision": strong_days, "mock_test": mock_days}
    type_sequence = _deficit_round_robin(
        {k: v / pool_days if pool_days else 0 for k, v in exact_counts.items()}, pool_days
    )

    topic_cursor = {"weak_focus": {s: 0 for s in SECTIONS}, "strong_revision": {s: 0 for s in SECTIONS}}
    section_cursor = {"weak_focus": {"_pos": 0}, "strong_revision": {"_pos": 0}}
    quotas = {"weak_focus": weak_quota, "strong_revision": strong_quota}

    days: List[dict] = []
    day_number = 1
    current_date = today

    def _add_day(day_type: str, section: Optional[str], topics: List[str], note: str) -> None:
        nonlocal day_number, current_date
        days.append(
            {
                "date": current_date.isoformat(),
                "day_number": day_number,
                "day_type": day_type,
                "section": section,
                "topics": topics,
                "duration_minutes": 120,
                "note": note,
            }
        )
        day_number += 1
        current_date = current_date + timedelta(days=1)

    for day_type in type_sequence:
        if day_type == "mock_test":
            _add_day(
                "mock_test",
                None,
                [],
                "Take a full mock test - simulate exam conditions and track percentile progress.",
            )
            continue

        section = _next_section_with_quota(quotas[day_type], section_cursor[day_type])
        if section is None:
            section = SECTIONS[day_number % len(SECTIONS)]

        stats = section_stats[section]
        topic_key = "weak_topics" if day_type == "weak_focus" else "strong_topics"
        topic_list = stats[topic_key] or TOPIC_OPTIONS_BY_SECTION.get(section, ["General practice"])
        cursor = topic_cursor[day_type][section]
        topic = topic_list[cursor % len(topic_list)]
        topic_cursor[day_type][section] += 1

        if day_type == "weak_focus":
            note = (
                f"Focus on {topic} ({section}) - not yet tested, building baseline familiarity."
                if not stats["has_data"]
                else f"Focus on {topic} ({section}) - flagged as a weak area."
            )
        else:
            note = f"Quick revision: {topic} ({section}) - keep this sharp."

        _add_day(day_type, section, [topic], note)

    for _ in range(taper_days):
        _add_day(
            "taper_revision",
            None,
            [],
            "Final stretch - light revision of previously flagged concepts and formulas "
            "across all sections. No new material.",
        )

    return days


def generate_plan(
    db: Session, user: User, source: str, session: Optional[CatMockTestSession] = None
) -> CatStudyPlan:
    if source not in ("single_test", "full_history"):
        raise ValueError("source must be 'single_test' or 'full_history'.")

    if source == "single_test":
        if session is None:
            raise ValueError("session_id is required for source='single_test'.")
        if session.user_id != user.id:
            raise ValueError("That test does not belong to this account.")
        if session.status != CatMockTestStatus.SUBMITTED:
            raise ValueError("That test has not been submitted yet.")
        if session.test_type == CatTestType.TOPIC_DRILL:
            raise ValueError(
                "Topic drills can't be used as a plan basis - use a sectional or full mock test."
            )
        section_stats = _topic_stats_from_session(session)
    else:
        section_stats = _topic_stats_from_history(db, user)

    section_stats = _apply_fallback(section_stats)
    days = _build_days(section_stats, date.today(), EXAM_DATE)

    plan = CatStudyPlan(
        user_id=user.id,
        source=source,
        source_session_id=session.id if session else None,
        exam_date=EXAM_DATE,
        days=days,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_latest_plan(db: Session, user: User) -> Optional[CatStudyPlan]:
    return (
        db.query(CatStudyPlan)
        .filter(CatStudyPlan.user_id == user.id)
        .order_by(CatStudyPlan.generated_at.desc())
        .first()
    )
