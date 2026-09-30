from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.enums import CatMockTestStatus, CatQuestionSourcePreference, CatTestType
from app.models.user import User
from app.schemas.cat_mock_test import MockTestStartResponse
from app.schemas.cat_pyq import PyqPaperOption, PyqStartRequest
from app.services import cat_mock_test_service
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/cat/pyq", tags=["cat-pyq"])


@router.get("/available", response_model=list[PyqPaperOption])
def list_available_pyq_papers(db: Session = Depends(get_db)):
    return cat_mock_test_service.list_available_pyq_papers(db)


@router.post("/start", response_model=MockTestStartResponse)
def start_pyq_paper(
    payload: PyqStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    available = cat_mock_test_service.list_available_pyq_papers(db)
    match = next(
        (
            p
            for p in available
            if p["source_year"] == payload.source_year and p["source_slot"] == payload.source_slot
        ),
        None,
    )
    if match is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="PYQ paper not found")

    sections = payload.sections or list(match["sections"].keys())

    session = CatMockTestSession(
        user_id=current_user.id,
        test_type=CatTestType.PYQ_PAPER,
        sections_included=sections,
        question_source=CatQuestionSourcePreference.PYQ_ONLY,
        pyq_source_year=payload.source_year,
        pyq_source_slot=payload.source_slot,
        status=CatMockTestStatus.GENERATING,
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    session = cat_mock_test_service.assemble_pyq_paper(
        db, session, payload.source_year, payload.source_slot, sections
    )

    return MockTestStartResponse(session_id=session.id, status=session.status.value)
