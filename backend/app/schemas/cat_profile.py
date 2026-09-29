from typing import List, Optional

from pydantic import BaseModel


class CatProfileUpdateRequest(BaseModel):
    cat_academic_background: Optional[str] = None
    cat_target_iims: Optional[List[str]] = None
    cat_target_percentile: Optional[float] = None


class CatProfileResponse(BaseModel):
    id: int
    email: str
    username: str
    cat_academic_background: Optional[str] = None
    cat_target_iims: Optional[List[str]] = None
    cat_target_percentile: Optional[float] = None

    class Config:
        from_attributes = True
