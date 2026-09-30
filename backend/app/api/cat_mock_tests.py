from datetime import datetime, timedelta, timezone
from typing import Dict, List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.enums import CatMockTestStatus, CatTestType
from app.models.user import User
from app.schemas.cat_mock_test import (
    AnswerSubmission,
    MockTestDetailResponse,
    MockTestQuestionOut,
    MockTestResultsResponse,
    MockTestSectionOut,
    MockTestStartRequest,
    MockTestStartResponse,
    MockTestStatusResponse,
    ResultQuestionOut,
    SectionAnswersRequest,
    SectionAnswersResponse,
    SectionBreakdown,
    SectionStartResponse,
    SubmitResponse,
)
from app.services import cat_mock_test_generation_worker as worker
from app.services import cat_mock_test_service, cat_weak_concept_service
from app.services.cat_mock_test_service import SECTION_TIME_LIMIT_SECONDS
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/cat/mock-tests", tags=["cat-mock-tests"])


def _get_owned_session(db: Session, session_id: int, current_user: User) -> CatMockTestSession:
    session = (
        db.query(CatMockTestSession)
        .filter(CatMockTestSession.id == session_id, CatMockTestSession.user_id == current_user.id)
        .first()
    )
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mock test session not found")
    return session


def build_mock_test_detail_response(session: CatMockTestSession) -> MockTestDetailResponse:
    sections_map: Dict[str, List[MockTestQuestionOut]] = {}

    for mtq in session.questions:
        data = cat_mock_test_service.get_question_data(mtq)
        section = data.get("section") or "UNKNOWN"
        sections_map.setdefault(section, []).append(
            MockTestQuestionOut(
                id=mtq.id,
                order_index=mtq.order_index,
                section=section,
                question_type=data.get("question_type"),
                topic=data.get("topic"),
                difficulty=data.get("difficulty"),
                group_id=data.get("group_id"),
                passage_text=data.get("passage_text"),
                question_text=data.get("question_text") or "",
                options=data.get("options"),
                selected_answer=mtq.selected_answer,
                was_skipped=mtq.was_skipped,
            )
        )

    sections_out = [
        MockTestSectionOut(
            section=section,
            time_limit_seconds=SECTION_TIME_LIMIT_SECONDS,
            questions=sorted(qs, key=lambda q: q.order_index),
        )
        for section, qs in sections_map.items()
    ]

    return MockTestDetailResponse(
        id=session.id,
        test_type=session.test_type.value,
        status=session.status.value,
        sections=sections_out,
        section_started_at=session.section_started_at,
        section_submitted_at=session.section_submitted_at,
    )


@router.post("/start", response_model=MockTestStartResponse)
def start_mock_test(
    payload: MockTestStartRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = CatMockTestSession(
        user_id=current_user.id,
        test_type=payload.test_type,
        sections_included=payload.sections,
        status=CatMockTestStatus.GENERATING,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    background_tasks.add_task(worker.run, session.id)

    return MockTestStartResponse(session_id=session.id, status=session.status.value)


@router.get("/{session_id}/status", response_model=MockTestStatusResponse)
def get_mock_test_status(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)
    return MockTestStatusResponse(status=session.status.value)


@router.get("/{session_id}", response_model=MockTestDetailResponse)
def get_mock_test(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)
    return build_mock_test_detail_response(session)


@router.post("/{session_id}/sections/{section}/start", response_model=SectionStartResponse)
def start_section(
    session_id: int,
    section: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = _get_owned_session(db, session_id, current_user)

    now = datetime.now(timezone.utc)
    started = dict(session.section_started_at or {})
    started[section] = now.isoformat()
    session.section_started_at = started

    if session.status == CatMockTestStatus.READY:
        session.status = CatMockTestStatus.IN_PROGRESS

    db.add(session)
    db.commit()

    deadline = now + timedelta(seconds=SECTION_TIME_LIMIT_SECONDS)
    return SectionStartResponse(section=section, started_at=now, deadline=deadline)


@router.post("/{session_id}/sections/{section}/answers", response_model=SectionAnswersResponse)
def submit_section_answers(
    session_id: int,
    section: str,
    payload: SectionAnswersRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = _get_owned_session(db, session_id, current_user)
    question_map = {mtq.id: mtq for mtq in session.questions}

    answer: AnswerSubmission
    for answer in payload.answers:
        mtq = question_map.get(answer.question_id)
        if mtq is None:
            continue
        mtq.selected_answer = answer.selected_answer
        mtq.time_spent_seconds = answer.time_spent_seconds
        mtq.was_skipped = answer.was_skipped
        db.add(mtq)

    now = datetime.now(timezone.utc)
    submitted = dict(session.section_submitted_at or {})
    submitted[section] = now.isoformat()
    session.section_submitted_at = submitted
    db.add(session)
    db.commit()

    return SectionAnswersResponse(section=section, submitted_at=now)


@router.post("/{session_id}/submit", response_model=SubmitResponse)
def submit_mock_test(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)
    session = cat_mock_test_service.score_submission(db, session)

    if session.test_type == CatTestType.TOPIC_DRILL:
        cat_weak_concept_service.resolve_drill_session(db, session)

    return SubmitResponse(
        session_id=session.id,
        status=session.status.value,
        raw_score=session.raw_score,
        percentile_estimate=session.percentile_estimate,
    )


@router.get("/{session_id}/results", response_model=MockTestResultsResponse)
def get_mock_test_results(
    session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    session = _get_owned_session(db, session_id, current_user)
    if session.status != CatMockTestStatus.SUBMITTED:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Test has not been submitted yet")

    breakdown_map: Dict[str, Dict[str, int]] = {}
    questions_out: List[ResultQuestionOut] = []

    for mtq in sorted(session.questions, key=lambda q: q.order_index):
        data = cat_mock_test_service.get_question_data(mtq)
        section = data.get("section") or "UNKNOWN"
        stats = breakdown_map.setdefault(
            section, {"correct": 0, "wrong": 0, "skipped": 0, "ungraded": 0}
        )

        if mtq.was_skipped or mtq.selected_answer is None:
            stats["skipped"] += 1
        elif mtq.is_correct is None:
            # Answered, but the question's answer key hasn't been transcribed yet.
            stats["ungraded"] += 1
        elif mtq.is_correct:
            stats["correct"] += 1
        else:
            stats["wrong"] += 1

        questions_out.append(
            ResultQuestionOut(
                id=mtq.id,
                order_index=mtq.order_index,
                section=section,
                group_id=data.get("group_id"),
                passage_text=data.get("passage_text"),
                question_text=data.get("question_text") or "",
                options=data.get("options"),
                correct_answer=data.get("correct_answer"),
                explanation=data.get("explanation"),
                selected_answer=mtq.selected_answer,
                is_correct=mtq.is_correct,
                marks_awarded=mtq.marks_awarded,
            )
        )

    section_breakdown = [
        SectionBreakdown(
            section=section,
            correct=s["correct"],
            wrong=s["wrong"],
            skipped=s["skipped"],
            ungraded=s["ungraded"],
        )
        for section, s in breakdown_map.items()
    ]

    return MockTestResultsResponse(
        id=session.id,
        status=session.status.value,
        raw_score=session.raw_score,
        percentile_estimate=session.percentile_estimate,
        section_breakdown=section_breakdown,
        questions=questions_out,
    )
