import httpx

from app.core.config import settings
from app.utils.otp import OTP_EXPIRY_MINUTES

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
REQUEST_TIMEOUT_SECONDS = 10


class EmailSendError(Exception):
    """Raised when Brevo rejects the request or the call times out/fails."""


def _send_email(to_email: str, subject: str, html_content: str) -> None:
    payload = {
        "sender": {"name": settings.brevo_sender_name, "email": settings.brevo_sender_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content,
    }
    headers = {
        "api-key": settings.brevo_api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        response = httpx.post(BREVO_API_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS)
    except httpx.RequestError as exc:
        raise EmailSendError(f"Brevo request failed: {exc}") from exc

    if response.status_code >= 300:
        raise EmailSendError(f"Brevo returned {response.status_code}: {response.text}")


def send_verification_otp_email(to_email: str, otp_code: str) -> None:
    subject = "Verify your CAT Prep Platform email"
    html_content = (
        f"<p>Your verification code is:</p><h2>{otp_code}</h2>"
        f"<p>This code expires in {OTP_EXPIRY_MINUTES} minutes. If you didn't request this, ignore this email.</p>"
    )
    _send_email(to_email, subject, html_content)


def send_password_reset_otp_email(to_email: str, otp_code: str) -> None:
    subject = "Reset your CAT Prep Platform password"
    html_content = (
        f"<p>Your password reset code is:</p><h2>{otp_code}</h2>"
        f"<p>This code expires in {OTP_EXPIRY_MINUTES} minutes. If you didn't request this, you can safely ignore this email.</p>"
    )
    _send_email(to_email, subject, html_content)
