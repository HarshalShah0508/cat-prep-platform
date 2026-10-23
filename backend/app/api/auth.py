import logging
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.rate_limiter import limiter
from app.database.database import get_db
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    GoogleLoginRequest,
    LoginRequest,
    MessageResponse,
    ResendVerificationRequest,
    ResetPasswordRequest,
    SignupRequest,
    SignupResponse,
    TokenResponse,
    VerifyEmailRequest,
)
from app.services.brevo_email_service import (
    EmailSendError,
    send_password_reset_otp_email,
    send_verification_otp_email,
)
from app.services.google_oauth_service import authenticate_google_user
from app.utils.jwt_handler import create_access_token, verify_unsubscribe_token
from app.utils.otp import OTP_EXPIRY_MINUTES, generate_otp
from app.utils.security import hash_password, verify_password

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

GENERIC_VERIFICATION_RESENT_MESSAGE = "If this account needs verification, a new code has been sent."
GENERIC_RESET_REQUESTED_MESSAGE = "If an account exists for this email, a reset code has been sent."


def _otp_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(minutes=OTP_EXPIRY_MINUTES)


def _is_expired(expires_at) -> bool:
    return expires_at is None or datetime.now(timezone.utc) > expires_at


@router.post("/signup", response_model=SignupResponse)
@limiter.limit("5/minute")
def signup(request: Request, payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    otp_code = generate_otp()
    user = User(
        email=payload.email,
        hashed_password=hash_password(payload.password),
        username=payload.username,
        is_verified=False,
        email_verification_otp_hash=hash_password(otp_code),
        email_verification_otp_expires_at=_otp_expiry(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    try:
        send_verification_otp_email(user.email, otp_code)
    except EmailSendError as exc:
        db.delete(user)
        db.commit()
        logger.error("Failed to send verification email to %s: %s", payload.email, exc)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Could not send verification email. Please try again shortly.",
        ) from exc

    return SignupResponse(message="Account created. Check your email for a verification code.", email=user.email)


@router.post("/dev-login", response_model=TokenResponse)
def dev_login(db: Session = Depends(get_db)):
    """Local-development-only: get-or-create a fixed dev user, no password."""
    user = db.query(User).filter(User.email == "dev@catprep.local").first()
    if user is None:
        user = User(
            email="dev@catprep.local",
            hashed_password=hash_password("dev-local-only"),
            username="dev",
            is_verified=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    user.last_login_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token, user=user)


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(request: Request, payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if user.hashed_password is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This account was created using Google Sign-In. Please continue with Google.",
        )

    if not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="EMAIL_NOT_VERIFIED")

    user.last_login_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token, user=user)


@router.post("/google", response_model=TokenResponse)
@limiter.limit("10/minute")
def google_login(request: Request, payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    user = authenticate_google_user(payload.id_token, db)
    user.last_login_at = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token, user=user)


@router.post("/verify-email", response_model=TokenResponse)
@limiter.limit("10/minute")
def verify_email(request: Request, payload: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or code")

    if user.email_verification_otp_hash is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No pending verification for this email")

    if _is_expired(user.email_verification_otp_expires_at):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification code expired. Request a new one.")

    if not verify_password(payload.otp_code, user.email_verification_otp_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid verification code")

    user.is_verified = True
    user.email_verification_otp_hash = None
    user.email_verification_otp_expires_at = None
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token, user=user)


def _apply_unsubscribe(token: str, db: Session) -> None:
    user_id = verify_unsubscribe_token(token)
    if user_id is not None:
        user = db.query(User).filter(User.id == user_id).first()
        if user is not None:
            user.email_opt_out = True
            db.add(user)
            db.commit()


@router.get("/unsubscribe", response_class=HTMLResponse)
def unsubscribe(token: str = Query(...), db: Session = Depends(get_db)):
    _apply_unsubscribe(token, db)
    return (
        "<html><body style='font-family:sans-serif;text-align:center;padding:60px 20px;'>"
        "<h2>You've been unsubscribed</h2>"
        "<p>You won't receive reminder emails from CAT Prep Platform anymore.</p>"
        "</body></html>"
    )


@router.post("/unsubscribe")
def unsubscribe_one_click(token: str = Query(...), db: Session = Depends(get_db)):
    """RFC 8058 one-click target - what Gmail/Yahoo's built-in Unsubscribe button calls."""
    _apply_unsubscribe(token, db)
    return {"status": "unsubscribed"}


@router.post("/resend-verification", response_model=MessageResponse)
@limiter.limit("3/minute")
def resend_verification(request: Request, payload: ResendVerificationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is not None and not user.is_verified:
        otp_code = generate_otp()
        user.email_verification_otp_hash = hash_password(otp_code)
        user.email_verification_otp_expires_at = _otp_expiry()
        db.add(user)
        db.commit()

        try:
            send_verification_otp_email(user.email, otp_code)
        except EmailSendError as exc:
            logger.error("Failed to resend verification email to %s: %s", payload.email, exc)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Could not send verification email. Please try again shortly.",
            ) from exc

    return MessageResponse(message=GENERIC_VERIFICATION_RESENT_MESSAGE)


@router.post("/forgot-password", response_model=MessageResponse)
@limiter.limit("3/minute")
def forgot_password(request: Request, payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is not None:
        otp_code = generate_otp()
        user.password_reset_otp_hash = hash_password(otp_code)
        user.password_reset_otp_expires_at = _otp_expiry()
        db.add(user)
        db.commit()

        try:
            send_password_reset_otp_email(user.email, otp_code)
        except EmailSendError as exc:
            logger.error("Failed to send password reset email to %s: %s", payload.email, exc)

    return MessageResponse(message=GENERIC_RESET_REQUESTED_MESSAGE)


@router.post("/reset-password", response_model=TokenResponse)
@limiter.limit("10/minute")
def reset_password(request: Request, payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email or code")

    if user.password_reset_otp_hash is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No pending reset for this email")

    if _is_expired(user.password_reset_otp_expires_at):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Reset code expired. Request a new one.")

    if not verify_password(payload.otp_code, user.password_reset_otp_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reset code")

    user.hashed_password = hash_password(payload.new_password)
    user.password_reset_otp_hash = None
    user.password_reset_otp_expires_at = None
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token, user=user)
