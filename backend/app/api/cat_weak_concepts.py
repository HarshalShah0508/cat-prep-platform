from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.cat_mock_tests import build_mock_test_detail_response
from app.core.feature_flags import AI_DISABLED_MESSAGE, AI_FEATURES_DISABLED
from app.database.database import get_db
from app.models.user import User
from app.schemas.cat_mock_test import MockTestDetailResponse
from app.schemas.cat_weak_concept import WeakConceptOut
from app.services import cat_weak_concept_service
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/cat/weak-concepts", tags=["cat-weak-concepts"])


@router.get("", response_model=List[WeakConceptOut])
def get_weak_concepts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return cat_weak_concept_service.list_weak_concepts(db, current_user)


@router.post("/{weak_concept_id}/practice", response_model=MockTestDetailResponse)
def practice_weak_concept(
    weak_concept_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    if AI_FEATURES_DISABLED:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=AI_DISABLED_MESSAGE)

    try:
        session = cat_weak_concept_service.start_drill(db, current_user, weak_concept_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return build_mock_test_detail_response(session)
