from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.cat_profile import CatProfileResponse, CatProfileUpdateRequest
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/cat/profile", tags=["cat-profile"])


@router.put("", response_model=CatProfileResponse)
def update_profile(
    payload: CatProfileUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.cat_academic_background is not None:
        current_user.cat_academic_background = payload.cat_academic_background
    if payload.cat_years_experience_band is not None:
        current_user.cat_years_experience_band = payload.cat_years_experience_band
    if payload.cat_current_company is not None:
        current_user.cat_current_company = payload.cat_current_company
    if payload.cat_target_percentile_min is not None:
        current_user.cat_target_percentile_min = payload.cat_target_percentile_min
    if payload.cat_target_percentile_max is not None:
        current_user.cat_target_percentile_max = payload.cat_target_percentile_max

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.get("", response_model=CatProfileResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
