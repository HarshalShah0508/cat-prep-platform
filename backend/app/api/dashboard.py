from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.cat_pi_session import CatPISession
from app.models.enums import CatMockTestStatus, CatPIStatus, CatTestType
from app.models.user import User
from app.schemas.dashboard import DashboardResponse, LatestMockResult, LatestPISession
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    mock_sessions = (
        db.query(CatMockTestSession)
        .filter(
            CatMockTestSession.user_id == current_user.id,
            CatMockTestSession.status == CatMockTestStatus.SUBMITTED,
            CatMockTestSession.test_type != CatTestType.TOPIC_DRILL,
        )
        .order_by(CatMockTestSession.created_at.desc())
        .all()
    )

    mock_tests_taken = len(mock_sessions)
    last_five = mock_sessions[:5]
    percentiles = [s.percentile_estimate for s in last_five if s.percentile_estimate is not None]
    avg_percentile = sum(percentiles) / len(percentiles) if percentiles else None

    pi_sessions = (
        db.query(CatPISession)
        .filter(CatPISession.user_id == current_user.id, CatPISession.status == CatPIStatus.FINISHED)
        .order_by(CatPISession.created_at.desc())
        .all()
    )
    pi_sessions_completed = len(pi_sessions)

    latest_mock_result = None
    if mock_sessions:
        latest = mock_sessions[0]
        latest_mock_result = LatestMockResult(
            session_id=latest.id,
            test_type=latest.test_type.value,
            raw_score=latest.raw_score,
            percentile_estimate=latest.percentile_estimate,
        )

    latest_pi_session = None
    if pi_sessions:
        latest_pi = pi_sessions[0]
        latest_pi_session = LatestPISession(
            session_id=latest_pi.id,
            status=latest_pi.status.value,
            overall_score=latest_pi.overall_score,
        )

    return DashboardResponse(
        username=current_user.username,
        email=current_user.email,
        mock_tests_taken=mock_tests_taken,
        avg_percentile=avg_percentile,
        pi_sessions_completed=pi_sessions_completed,
        weak_concepts_flagged=current_user.cat_weak_concepts_flagged_total,
        weak_concepts_resolved=current_user.cat_weak_concepts_resolved_total,
        latest_mock_result=latest_mock_result,
        latest_pi_session=latest_pi_session,
    )
