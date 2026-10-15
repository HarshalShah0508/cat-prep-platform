import os
from typing import List

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables (.env)."""

    def __init__(self) -> None:
        raw_database_url = os.environ.get(
            "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/catprep"
        )
        # Pin the driver to psycopg2 (the driver installed via requirements.txt) so a bare
        # "postgresql://" URL doesn't get resolved against a different default dialect.
        if raw_database_url.startswith("postgresql://"):
            raw_database_url = raw_database_url.replace(
                "postgresql://", "postgresql+psycopg2://", 1
            )
        self.database_url: str = raw_database_url

        gemini_api_keys_raw = os.environ.get("GEMINI_API_KEYS")
        if not gemini_api_keys_raw:
            raise ValueError(
                "GEMINI_API_KEYS environment variable is required (comma-separated list of "
                "Google Gemini API keys)."
            )
        self.gemini_api_keys: List[str] = [
            key.strip() for key in gemini_api_keys_raw.split(",") if key.strip()
        ]
        if not self.gemini_api_keys:
            raise ValueError("GEMINI_API_KEYS is set but contains no usable keys.")

        secret_key = os.environ.get("SECRET_KEY")
        if not secret_key:
            raise ValueError("SECRET_KEY environment variable is required.")
        self.secret_key: str = secret_key

        brevo_api_key = os.environ.get("BREVO_API_KEY")
        if not brevo_api_key:
            raise ValueError("BREVO_API_KEY environment variable is required.")
        self.brevo_api_key: str = brevo_api_key

        brevo_sender_email = os.environ.get("BREVO_SENDER_EMAIL")
        if not brevo_sender_email:
            raise ValueError("BREVO_SENDER_EMAIL environment variable is required.")
        self.brevo_sender_email: str = brevo_sender_email

        self.brevo_sender_name: str = os.environ.get("BREVO_SENDER_NAME", "CAT Prep Platform")

        self.jwt_algorithm: str = os.environ.get("JWT_ALGORITHM", "HS256")
        self.jwt_expire_minutes: int = int(os.environ.get("JWT_EXPIRE_MINUTES", "1440"))
        self.frontend_origin: str = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")
        self.rate_limit_default: str = os.environ.get("RATE_LIMIT_DEFAULT", "60/minute")
        self.rate_limit_storage_uri: str = os.environ.get("RATE_LIMIT_STORAGE_URI", "memory://")


settings = Settings()
