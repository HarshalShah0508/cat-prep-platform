from typing import Optional

from pydantic import BaseModel


class CatProfileUpdateRequest(BaseModel):
    cat_academic_background: Optional[str] = None
    cat_years_experience_band: Optional[str] = None
    cat_current_company: Optional[str] = None
    cat_target_percentile_min: Optional[float] = None
    cat_target_percentile_max: Optional[float] = None


class CatProfileResponse(BaseModel):
    id: int
    email: str
    username: str
    cat_academic_background: Optional[str] = None
    cat_years_experience_band: Optional[str] = None
    cat_current_company: Optional[str] = None
    cat_target_percentile_min: Optional[float] = None
    cat_target_percentile_max: Optional[float] = None

    class Config:
        from_attributes = True
