from typing import Optional

from pydantic import BaseModel


class LatestMockResult(BaseModel):
    session_id: int
    test_type: str
    raw_score: Optional[float] = None
    percentile_estimate: Optional[float] = None


class LatestPISession(BaseModel):
    session_id: int
    status: str
    overall_score: Optional[float] = None


class DashboardResponse(BaseModel):
    username: str
    email: str
    mock_tests_taken: int
    avg_percentile: Optional[float] = None
    pi_sessions_completed: int
    weak_concepts_flagged: int
    weak_concepts_resolved: int
    latest_mock_result: Optional[LatestMockResult] = None
    latest_pi_session: Optional[LatestPISession] = None
