"""Daily engagement-email batch job - run via `python -m app.scripts.send_reminder_emails`.

Invoked by .github/workflows/reminder-emails.yml (GitHub Actions cron), since Render's
free tier spins the backend down and can't run its own always-on scheduler.
"""
import argparse
import os
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import func, text

from app.core.config import settings
from app.database.database import SessionLocal
from app.models.cat_mock_test_session import CatMockTestSession
from app.models.cat_pi_session import CatPISession
from app.models.cat_study_plan import CatStudyPlan
from app.models.cat_weak_concept import CatWeakConcept
from app.models.enums import CatMockTestStatus, CatPIStatus, CatWeakConceptStatus
from app.models.reminder_email_log import ReminderEmailLog
from app.models.user import User
from app.services.brevo_email_service import (
    EmailSendError,
    send_exam_countdown_email,
    send_inactivity_2d_email,
    send_inactivity_4d_email,
    send_inactivity_6d_email,
    send_unfinished_mock_test_email,
    send_unfinished_pi_session_email,
    send_unverified_signup_nudge_email,
    send_weak_concept_nudge_email,
)
from app.services.cat_study_plan_service import EXAM_DATE, get_latest_plan
from app.utils.otp import OTP_EXPIRY_MINUTES, generate_otp
from app.utils.security import hash_password

ADVISORY_LOCK_KEY = 741852

TIME_TIERS = [
    ("inactive_6d", timedelta(days=6)),
    ("inactive_4d", timedelta(days=4)),
    ("inactive_2d", timedelta(days=2)),
]
TIER_COOLDOWN = timedelta(days=2)
GROUP_A_REMINDER_TYPES = ["exam_countdown", "inactive_2d", "inactive_4d", "inactive_6d", "weak_concept_nudge"]
GROUP_A_CAP_WINDOW = timedelta(hours=20)
WEAK_CONCEPT_COOLDOWN = timedelta(days=5)
UNFINISHED_SESSION_AGE = timedelta(hours=3)
UNVERIFIED_SIGNUP_AGE = timedelta(hours=3)
VERIFY_NUDGE_INTERVAL = timedelta(days=3)
EXAM_COUNTDOWN_MILESTONES = (60, 30, 14, 7, 1)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_allowlist():
    raw = os.environ.get("REMINDER_EMAIL_ALLOWLIST")
    if not raw:
        return None
    return {e.strip().lower() for e in raw.split(",") if e.strip()}


def _already_sent(db, user_id, reminder_type, target_id=None, since=None):
    query = db.query(ReminderEmailLog.id).filter(
        ReminderEmailLog.user_id == user_id,
        ReminderEmailLog.reminder_type == reminder_type,
    )
    if target_id is not None:
        query = query.filter(ReminderEmailLog.target_id == target_id)
    if since is not None:
        query = query.filter(ReminderEmailLog.sent_at >= since)
    return query.first() is not None


def _sent_any_group_a_today(db, user_id):
    cutoff = _now() - GROUP_A_CAP_WINDOW
    return (
        db.query(ReminderEmailLog.id)
        .filter(
            ReminderEmailLog.user_id == user_id,
            ReminderEmailLog.reminder_type.in_(GROUP_A_REMINDER_TYPES),
            ReminderEmailLog.sent_at >= cutoff,
        )
        .first()
        is not None
    )


def _tier_cooldown_active(db, user_id):
    cutoff = _now() - TIER_COOLDOWN
    return (
        db.query(ReminderEmailLog.id)
        .filter(
            ReminderEmailLog.user_id == user_id,
            ReminderEmailLog.reminder_type.in_([t for t, _ in TIME_TIERS]),
            ReminderEmailLog.sent_at >= cutoff,
        )
        .first()
        is not None
    )


def _last_activity(db, user):
    last_mock_at = (
        db.query(func.max(CatMockTestSession.created_at))
        .filter(CatMockTestSession.user_id == user.id)
        .scalar()
    )
    last_pi_at = (
        db.query(func.max(CatPISession.created_at)).filter(CatPISession.user_id == user.id).scalar()
    )
    candidates = [t for t in (user.last_login_at, last_mock_at, last_pi_at) if t]
    return max(candidates) if candidates else user.created_at


def _pick_tier(db, user, last_activity):
    inactive_for = _now() - last_activity
    for reminder_type, threshold in TIME_TIERS:
        if inactive_for < threshold:
            continue
        if _already_sent(db, user.id, reminder_type, since=last_activity):
            continue
        return reminder_type
    return None


def _pick_unused_feature(db, user):
    has_mock = db.query(CatMockTestSession.id).filter(CatMockTestSession.user_id == user.id).first()
    if has_mock is None:
        return (
            "a mock test",
            f"{settings.frontend_origin}/mock-tests/new",
            "A full-length simulated mock test is the single best way to see where you really "
            "stand before CAT 2026 - try one.",
        )
    has_pi = db.query(CatPISession.id).filter(CatPISession.user_id == user.id).first()
    if has_pi is None:
        return (
            "a mock Personal Interview",
            f"{settings.frontend_origin}/pi/new",
            "A simulated AI Personal Interview round shows you exactly how IIM panels will "
            "probe your profile - try one before test day.",
        )
    has_plan = db.query(CatStudyPlan.id).filter(CatStudyPlan.user_id == user.id).first()
    if has_plan is None:
        return (
            "a study plan",
            f"{settings.frontend_origin}/study-plan",
            "A day-by-day study plan tailored to your weak areas keeps your prep focused "
            "instead of scattered - generate one.",
        )
    return (
        "another mock test",
        f"{settings.frontend_origin}/mock-tests/new",
        "You've tried every feature once - time to take another mock test and track your improvement.",
    )


def _dispatch(db, dry_run, allowlist, user, reminder_type, target_id, send_callable, summary):
    if allowlist is not None and user.email.lower() not in allowlist:
        print(f"[skip-not-allowlisted] user={user.id} type={reminder_type} target={target_id}")
        return
    print(
        f"[{'dry-run' if dry_run else 'send'}] user={user.id} email={user.email} "
        f"type={reminder_type} target={target_id} {summary}"
    )
    if dry_run:
        return
    try:
        send_callable()
    except EmailSendError as exc:
        print(f"[error] failed to send {reminder_type} to user={user.id}: {exc}")
        return
    db.add(ReminderEmailLog(user_id=user.id, reminder_type=reminder_type, target_id=target_id))
    db.commit()


def _send_tier_email(db, dry_run, allowlist, user, tier):
    if tier == "inactive_2d":
        best = (
            db.query(func.max(CatMockTestSession.percentile_estimate))
            .filter(
                CatMockTestSession.user_id == user.id,
                CatMockTestSession.status == CatMockTestStatus.SUBMITTED,
            )
            .scalar()
        )
        _dispatch(
            db, dry_run, allowlist, user, tier, None,
            lambda: send_inactivity_2d_email(user.email, user.username, user.id, best),
            f"best_percentile={best}",
        )
    elif tier == "inactive_4d":
        feature, url, pitch = _pick_unused_feature(db, user)
        _dispatch(
            db, dry_run, allowlist, user, tier, None,
            lambda: send_inactivity_4d_email(user.email, user.username, user.id, feature, url, pitch),
            f"feature={feature}",
        )
    else:  # inactive_6d
        mocks_taken = (
            db.query(func.count(CatMockTestSession.id))
            .filter(
                CatMockTestSession.user_id == user.id,
                CatMockTestSession.status == CatMockTestStatus.SUBMITTED,
            )
            .scalar()
        )
        best = (
            db.query(func.max(CatMockTestSession.percentile_estimate))
            .filter(
                CatMockTestSession.user_id == user.id,
                CatMockTestSession.status == CatMockTestStatus.SUBMITTED,
            )
            .scalar()
        )
        days_to_exam = (EXAM_DATE - date.today()).days
        _dispatch(
            db, dry_run, allowlist, user, tier, None,
            lambda: send_inactivity_6d_email(
                user.email, user.username, user.id, days_to_exam, mocks_taken or 0, best,
                user.cat_weak_concepts_flagged_total, user.cat_weak_concepts_resolved_total,
            ),
            f"mocks={mocks_taken} best={best}",
        )


def _run_group_a(db, dry_run, allowlist):
    """Inactivity tiers, exam countdown, weak-concept nudge - max 1 email/user/run
    (exam_countdown > inactivity tier > weak_concept_nudge priority)."""
    today = date.today()
    days_left = (EXAM_DATE - today).days
    milestone = days_left if days_left in EXAM_COUNTDOWN_MILESTONES else None

    users = (
        db.query(User)
        .filter((User.auth_provider != "local") | (User.is_verified.is_(True)))
        .filter(User.email_opt_out.is_(False))
        .all()
    )
    for user in users:
        if _sent_any_group_a_today(db, user.id):
            continue

        if milestone is not None and not _already_sent(db, user.id, "exam_countdown", target_id=milestone):
            plan = get_latest_plan(db, user)
            _dispatch(
                db, dry_run, allowlist, user, "exam_countdown", milestone,
                lambda: send_exam_countdown_email(
                    user.email, user.username, user.id, milestone, plan is not None
                ),
                f"days_left={milestone}",
            )
            continue

        if not _tier_cooldown_active(db, user.id):
            last_activity = _last_activity(db, user)
            tier = _pick_tier(db, user, last_activity)
            if tier is not None:
                _send_tier_email(db, dry_run, allowlist, user, tier)
                continue

        open_weak = user.cat_weak_concepts_flagged_total - user.cat_weak_concepts_resolved_total
        if open_weak > 0 and not _already_sent(
            db, user.id, "weak_concept_nudge", since=_now() - WEAK_CONCEPT_COOLDOWN
        ):
            concept = (
                db.query(CatWeakConcept)
                .filter(
                    CatWeakConcept.user_id == user.id,
                    CatWeakConcept.status != CatWeakConceptStatus.RESOLVED,
                )
                .order_by(CatWeakConcept.created_at.asc())
                .first()
            )
            if concept is not None:
                _dispatch(
                    db, dry_run, allowlist, user, "weak_concept_nudge", None,
                    lambda: send_weak_concept_nudge_email(
                        user.email, user.username, user.id, open_weak, concept.concept, concept.section
                    ),
                    f"open={open_weak} concept={concept.concept}",
                )


def _run_unfinished_sessions(db, dry_run, allowlist):
    """Unfinished mock test / PI session nudges - event-based, exempt from the Group A cap."""
    cutoff = _now() - UNFINISHED_SESSION_AGE

    unfinished_mocks = (
        db.query(CatMockTestSession)
        .filter(
            CatMockTestSession.status == CatMockTestStatus.IN_PROGRESS,
            CatMockTestSession.created_at <= cutoff,
        )
        .all()
    )
    for session in unfinished_mocks:
        user = db.query(User).filter(User.id == session.user_id).first()
        if user is None or user.email_opt_out:
            continue
        if _already_sent(db, user.id, "unfinished_mock_test", target_id=session.id):
            continue
        _dispatch(
            db, dry_run, allowlist, user, "unfinished_mock_test", session.id,
            lambda: send_unfinished_mock_test_email(user.email, user.username, user.id, session.id),
            f"session={session.id}",
        )

    unfinished_pis = (
        db.query(CatPISession)
        .filter(
            CatPISession.status == CatPIStatus.IN_PROGRESS,
            CatPISession.created_at <= cutoff,
        )
        .all()
    )
    for session in unfinished_pis:
        user = db.query(User).filter(User.id == session.user_id).first()
        if user is None or user.email_opt_out:
            continue
        if _already_sent(db, user.id, "unfinished_pi_session", target_id=session.id):
            continue
        _dispatch(
            db, dry_run, allowlist, user, "unfinished_pi_session", session.id,
            lambda: send_unfinished_pi_session_email(user.email, user.username, user.id, session.id),
            f"session={session.id}",
        )


def _run_unverified_signup_nudges(db, dry_run, allowlist):
    """Re-nudge local signups stuck unverified. Issues a fresh OTP, so the OTP write only
    happens when a send is actually about to be attempted (not skipped by allowlist/dry-run)."""
    cutoff = _now() - UNVERIFIED_SIGNUP_AGE
    since = _now() - VERIFY_NUDGE_INTERVAL

    users = (
        db.query(User)
        .filter(
            User.auth_provider == "local",
            User.is_verified.is_(False),
            User.email_opt_out.is_(False),
            User.created_at <= cutoff,
        )
        .all()
    )
    for user in users:
        if _already_sent(db, user.id, "unverified_signup_nudge", since=since):
            continue
        if allowlist is not None and user.email.lower() not in allowlist:
            print(f"[skip-not-allowlisted] user={user.id} type=unverified_signup_nudge")
            continue
        print(f"[{'dry-run' if dry_run else 'send'}] user={user.id} email={user.email} type=unverified_signup_nudge")
        if dry_run:
            continue

        otp_code = generate_otp()
        user.email_verification_otp_hash = hash_password(otp_code)
        user.email_verification_otp_expires_at = _now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        db.add(user)
        db.commit()

        try:
            send_unverified_signup_nudge_email(user.email, user.username, user.id, otp_code)
        except EmailSendError as exc:
            print(f"[error] failed to send unverified_signup_nudge to user={user.id}: {exc}")
            continue

        db.add(ReminderEmailLog(user_id=user.id, reminder_type="unverified_signup_nudge"))
        db.commit()


def run(dry_run: bool = False) -> None:
    allowlist = _parse_allowlist()
    db = SessionLocal()
    lock_acquired = False
    try:
        lock_acquired = bool(
            db.execute(text("SELECT pg_try_advisory_lock(:key)"), {"key": ADVISORY_LOCK_KEY}).scalar()
        )
        if not lock_acquired:
            print("[skip] another run holds the advisory lock")
            return

        _run_group_a(db, dry_run, allowlist)
        _run_unfinished_sessions(db, dry_run, allowlist)
        _run_unverified_signup_nudges(db, dry_run, allowlist)
    finally:
        if lock_acquired:
            db.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": ADVISORY_LOCK_KEY})
            db.commit()
        db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
