from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WeakConceptOut(BaseModel):
    id: int
    section: str
    concept: str
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True
