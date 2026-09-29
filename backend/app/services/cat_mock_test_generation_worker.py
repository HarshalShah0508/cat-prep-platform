import logging

from app.database.database import SessionLocal
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.enums import CatMockTestStatus
from app.models.user import User
from app.services.cat_mock_test_service import assemble_mock_test

logger = logging.getLogger(__name__)


def run(session_id: int) -> None:
    """Background task entry point: fills in the CatMockTestQuestion rows for an
    already-created (status=generating) CatMockTestSession, then flips it to ready."""
    db = SessionLocal()
    try:
        session = db.query(CatMockTestSession).filter(CatMockTestSession.id == session_id).first()
        if session is None:
            logger.error("Mock test generation worker: session_id=%s not found", session_id)
            return

        user = db.query(User).filter(User.id == session.user_id).first()
        if user is None:
            logger.error("Mock test generation worker: user for session_id=%s not found", session_id)
            return

        assemble_mock_test(db, user, session.test_type, session.sections_included, session=session)
    except Exception:
        logger.exception("Mock test generation failed for session_id=%s", session_id)
        db.rollback()
        session = db.query(CatMockTestSession).filter(CatMockTestSession.id == session_id).first()
        if session is not None and session.status != CatMockTestStatus.READY:
            # Leave status=generating so the client can retry/poll; the failure is logged above.
            session.status = CatMockTestStatus.GENERATING
            db.add(session)
            db.commit()
    finally:
        db.close()
