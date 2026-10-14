from fastapi import APIRouter, Depends, File, HTTPException, Request, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.core.feature_flags import AI_DISABLED_MESSAGE, AI_FEATURES_DISABLED
from app.core.rate_limiter import limiter
from app.database.database import get_db
from app.models.user import User
from app.schemas.cat_pi_resume import ResumeOut, ResumeUploadResponse
from app.services import cat_pi_resume_service
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/cat/resume", tags=["cat-resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
@limiter.limit("15/minute")
def upload_resume(
    request: Request,
    response: Response,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if AI_FEATURES_DISABLED:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=AI_DISABLED_MESSAGE)

    if file.content_type != "application/pdf":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF files are allowed")

    pdf_bytes = file.file.read()

    try:
        resume = cat_pi_resume_service.create_resume(db, current_user, file.filename, pdf_bytes)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ResumeUploadResponse(
        resume_id=resume.id,
        filename=resume.original_filename,
        message="Resume uploaded successfully",
    )


@router.get("", response_model=list[ResumeOut])
def get_resumes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return cat_pi_resume_service.list_resumes(db, current_user)


@router.delete("/{resume_id}")
def delete_resume(
    resume_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    cat_pi_resume_service.delete_resume(db, current_user, resume_id)
    return {"message": "Resume deleted successfully"}
