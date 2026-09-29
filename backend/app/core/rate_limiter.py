from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from app.core.config import settings
from app.utils.jwt_handler import decode_access_token


def rate_limit_key(request: Request) -> str:
    """Key by the account's email decoded straight from the JWT `sub` claim when a valid
    bearer token is present, else fall back to the client IP."""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.lower().startswith("bearer "):
        token = auth_header.split(" ", 1)[1].strip()
        payload = decode_access_token(token)
        if payload and payload.get("sub"):
            return payload["sub"]
    return get_remote_address(request)


limiter = Limiter(
    key_func=rate_limit_key,
    default_limits=[settings.rate_limit_default],
    storage_uri=settings.rate_limit_storage_uri,
)
