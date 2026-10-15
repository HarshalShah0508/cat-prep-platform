from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.user import User
from app.schemas.cat_study_plan import GeneratePlanRequest, StudyPlanResponse
from app.services import cat_study_plan_service
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/cat/study-plan", tags=["cat-study-plan"])


@router.post("/generate", response_model=StudyPlanResponse)
def generate_plan(
    payload: GeneratePlanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    session = None
    if payload.source == "single_test":
        if payload.session_id is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="session_id is required")
        session = (
            db.query(CatMockTestSession)
            .filter(CatMockTestSession.id == payload.session_id)
            .first()
        )
        if session is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test not found")

    try:
        plan = cat_study_plan_service.generate_plan(db, current_user, payload.source, session)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return plan


@router.get("", response_model=StudyPlanResponse)
def get_plan(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    plan = cat_study_plan_service.get_latest_plan(db, current_user)
    if plan is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No study plan generated yet")
    return plan
