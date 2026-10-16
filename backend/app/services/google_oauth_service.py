from fastapi import HTTPException, status
from google.auth.exceptions import GoogleAuthError
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.user import User


def authenticate_google_user(id_token_str: str, db: Session) -> User:
    try:
        token_info = id_token.verify_oauth2_token(
            id_token_str, google_requests.Request(), settings.google_client_id
        )
    except (GoogleAuthError, ValueError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Google ID token") from exc

    if not token_info.get("email_verified"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google email is not verified")

    sub = token_info["sub"]
    email = token_info["email"]
    name = token_info.get("name") or email.split("@")[0]

    user = db.query(User).filter(User.google_id == sub).first()
    if user is not None:
        return user

    user = db.query(User).filter(User.email == email).first()
    if user is not None:
        if user.google_id is not None and user.google_id != sub:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This account is already linked to a different Google account.",
            )
        user.google_id = sub
        user.is_verified = True
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    user = User(
        email=email,
        username=name,
        hashed_password=None,
        google_id=sub,
        auth_provider="google",
        is_verified=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
