import httpx

from app.core.config import settings
from app.utils.jwt_handler import create_unsubscribe_token
from app.utils.otp import OTP_EXPIRY_MINUTES

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
REQUEST_TIMEOUT_SECONDS = 10

CTA_BUTTON_STYLE = (
    "background:#2563eb;color:white;padding:12px 20px;"
    "text-decoration:none;border-radius:8px;display:inline-block;"
)


class EmailSendError(Exception):
    """Raised when Brevo rejects the request or the call times out/fails."""


def _send_email(to_email: str, subject: str, html_content: str, headers: dict = None) -> None:
    payload = {
        "sender": {"name": settings.brevo_sender_name, "email": settings.brevo_sender_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content,
    }
    if headers:
        payload["headers"] = headers
    request_headers = {
        "api-key": settings.brevo_api_key,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        response = httpx.post(
            BREVO_API_URL, json=payload, headers=request_headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
    except httpx.RequestError as exc:
        raise EmailSendError(f"Brevo request failed: {exc}") from exc

    if response.status_code >= 300:
        raise EmailSendError(f"Brevo returned {response.status_code}: {response.text}")


def _unsubscribe_url(user_id: int) -> str:
    token = create_unsubscribe_token(user_id)
    return f"{settings.backend_url}/auth/unsubscribe?token={token}"


def _unsubscribe_footer(user_id: int) -> str:
    url = _unsubscribe_url(user_id)
    return (
        f'<p style="font-size:12px;color:#888;margin-top:24px;">'
        f'Don\'t want these emails? <a href="{url}" style="color:#888;">Unsubscribe</a></p>'
    )


def _unsubscribe_headers(user_id: int) -> dict:
    url = _unsubscribe_url(user_id)
    return {
        "List-Unsubscribe": f"<{url}>",
        "List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
    }


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


def _cta(label: str, url: str) -> str:
    return f'<p><a href="{url}" style="{CTA_BUTTON_STYLE}">{label}</a></p>'


def send_inactivity_2d_email(to_email: str, username: str, user_id: int, best_percentile: float = None) -> None:
    subject = "Your CAT prep streak needs you back"
    percentile_line = (
        f"<p>Your last mock put you at ~{best_percentile:.0f}%ile - let's keep climbing.</p>"
        if best_percentile is not None
        else ""
    )
    html_content = (
        f"<p>Hey {username},</p>"
        f"<p>It's been 2 days since you last practiced. Even a quick 20-minute topic drill "
        f"keeps your percentile gains from slipping.</p>"
        f"{percentile_line}"
        f"{_cta('Resume Practice', f'{settings.frontend_origin}/dashboard')}"
        f"{_unsubscribe_footer(user_id)}"
    )
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))


def send_inactivity_4d_email(to_email: str, username: str, user_id: int, feature: str, feature_url: str, pitch: str) -> None:
    subject = f"Haven't tried {feature} yet? 4 days is a lot of CAT prep time."
    html_content = (
        f"<p>Hey {username},</p>"
        f"<p>{pitch}</p>"
        f"{_cta(f'Try {feature}', feature_url)}"
        f"{_unsubscribe_footer(user_id)}"
    )
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))


def send_inactivity_6d_email(
    to_email: str,
    username: str,
    user_id: int,
    days_to_exam: int,
    mocks_taken: int,
    best_percentile: float = None,
    weak_flagged: int = 0,
    weak_resolved: int = 0,
) -> None:
    subject = f"{days_to_exam} days to CAT 2026 - here's where you left off"
    percentile_line = f"best percentile ~{best_percentile:.0f}%ile, " if best_percentile is not None else ""
    html_content = (
        f"<p>Hey {username},</p>"
        f"<p>Six days off CAT prep is six days your competition didn't take. Here's your progress so far: "
        f"{mocks_taken} mock test(s) taken, {percentile_line}"
        f"{weak_resolved}/{weak_flagged} weak concepts resolved. Only {days_to_exam} days remain to CAT 2026.</p>"
        f"{_cta('Back to Dashboard', f'{settings.frontend_origin}/dashboard')}"
        f"{_unsubscribe_footer(user_id)}"
    )
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))


def send_unfinished_mock_test_email(to_email: str, username: str, user_id: int, session_id: int) -> None:
    subject = "You left a mock test mid-way"
    html_content = (
        f"<p>Hey {username},</p>"
        f"<p>You started a mock test and didn't submit it. Pick up where you left off.</p>"
        f"{_cta('Resume Mock Test', f'{settings.frontend_origin}/mock-tests/{session_id}')}"
        f"{_unsubscribe_footer(user_id)}"
    )
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))


def send_unfinished_pi_session_email(to_email: str, username: str, user_id: int, session_id: int) -> None:
    subject = "Your mock Personal Interview is still open"
    html_content = (
        f"<p>Hey {username},</p>"
        f"<p>You started a mock Personal Interview round and it's still sitting unfinished. "
        f"Wrap it up to get your feedback and score.</p>"
        f"{_cta('Resume PI Session', f'{settings.frontend_origin}/pi/{session_id}')}"
        f"{_unsubscribe_footer(user_id)}"
    )
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))


EXAM_COUNTDOWN_SUBJECTS = {
    60: "60 days to CAT 2026 - time to build your study plan",
    30: "30 days to CAT 2026 - halfway through the final stretch",
    14: "14 days to CAT 2026 - shift into revision mode",
    7: "1 week to CAT 2026 - focus only on what moves the needle",
    1: "Tomorrow is CAT 2026. You've got this.",
}


def send_exam_countdown_email(to_email: str, username: str, user_id: int, days_left: int, has_plan: bool) -> None:
    subject = EXAM_COUNTDOWN_SUBJECTS.get(days_left, f"{days_left} days to CAT 2026")
    if has_plan:
        body = "<p>Stick with your study plan - you're on track.</p>"
        cta = _cta("View My Study Plan", f"{settings.frontend_origin}/study-plan")
    else:
        body = "<p>You don't have a study plan yet. Generate one now to make the most of the time left.</p>"
        cta = _cta("Generate My Study Plan", f"{settings.frontend_origin}/study-plan")
    html_content = f"<p>Hey {username},</p>{body}{cta}{_unsubscribe_footer(user_id)}"
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))


def send_weak_concept_nudge_email(
    to_email: str, username: str, user_id: int, open_count: int, concept: str, section: str
) -> None:
    subject = f"{open_count} weak concepts still open - close the gap before test day"
    html_content = (
        f"<p>Hey {username},</p>"
        f"<p>Your {section} concept <strong>{concept}</strong> is still flagged. {open_count} weak "
        f"concept(s) remain unresolved across your prep. A focused 30-minute drill session can "
        f"clear one off the list today.</p>"
        f"{_cta('Review Weak Concepts', f'{settings.frontend_origin}/weak-concepts')}"
        f"{_unsubscribe_footer(user_id)}"
    )
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))


def send_unverified_signup_nudge_email(to_email: str, username: str, user_id: int, otp_code: str) -> None:
    subject = "Verify your email to start your CAT prep"
    html_content = (
        f"<p>Hey {username},</p>"
        f"<p>You signed up for CAT Prep Platform but haven't verified your email yet. "
        f"Here's a fresh code:</p><h2>{otp_code}</h2>"
        f"<p>This code expires in {OTP_EXPIRY_MINUTES} minutes. Enter it on the verification "
        f"page to unlock your dashboard.</p>"
        f"{_cta('Verify My Email', f'{settings.frontend_origin}/verify-email')}"
        f"{_unsubscribe_footer(user_id)}"
    )
    _send_email(to_email, subject, html_content, headers=_unsubscribe_headers(user_id))
