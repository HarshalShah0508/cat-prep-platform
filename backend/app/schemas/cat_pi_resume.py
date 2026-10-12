from datetime import datetime

from pydantic import BaseModel


class ResumeOut(BaseModel):
    id: int
    original_filename: str
    created_at: datetime

    class Config:
        from_attributes = True


class ResumeUploadResponse(BaseModel):
    resume_id: int
    filename: str
    message: str
