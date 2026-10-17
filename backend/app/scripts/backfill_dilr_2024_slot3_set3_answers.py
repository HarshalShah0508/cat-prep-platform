"""Backfill correct_answer for CAT 2024 DILR Slot 3 Set 3 (AC inside/outside
temperature set, group_id cat2024_slot3_dilr_set3), matched by id.

Not transcribed from any solutions PDF - solved from scratch directly from
the inside-temperature graph in DILR_SLOT3_CAT_2024.pdf (page 4). Graph
values (deg C) at each half-hour mark: 23:00=38, 23:30=32 (on the same
straight segment as 23:00-0:00, no kink), 0:00=26, 0:30=31, 1:00=26,
1:30=30, 2:00=28.

Any RISING segment can only happen while the AC is off (AC modes only cool).
Two such segments appear, each lasting only 30 minutes before being cut off
by the AC turning back on - but the passage's "off" rule says inside temp
reaches outside temp after a full 1 hour if left off, at a constant rate.
Extrapolating each 30-minute rise to a full hour gives the outside
temperature at the moment the AC was switched off:
  - 0:00-0:30 rises 26->31 (+5/30min); extrapolated to 60 min: +10, so
    outside temp at 0:00 = 36 degC.
  - 1:00-1:30 rises 26->30 (+4/30min); extrapolated to 60 min: +8, so
    outside temp at 1:00 = 34 degC (this directly answers Q10).
Outside temperature falls at a constant rate (given), so the rate is
(34-36)/1hr = -2 degC/hr. Outside temp at 9pm (3 hours before midnight) =
36 + 2*3 = 42 degC (Q11).

The 23:00-0:00 cooling segment is ambiguous by design: it could be either a
single 60-minute REGULAR-mode run (target 26), or two consecutive 30-minute
POWER-mode runs (target 32 at 23:30, then target 26 at 0:00) - both produce
an identical straight line on the graph. This does not affect any outside/
inside temperature values, but it is exactly why Q12's answer is "Either 2
or 3": turn-on/setting-change events strictly after 11:01pm and before
1:59am are {0:30, 1:30} (2 events) under the single-REGULAR reading, or
{23:30, 0:30, 1:30} (3 events) under the two-POWER reading.

Q9 ("how many times was the AC turned off") is unambiguous regardless of
that reading: exactly 2 turn-offs occur in the window, at 0:00 and 1:00.

Q13 (max |outside - inside| between 11:01pm and 1:59am): both temperature
functions are piecewise-linear, so the max difference occurs at one of the
half-hourly points. outside(t) = 36 - 2*(hours after midnight); tabulating
outside vs inside at each point gives differences of 0, 5, 10, 4, 8, 3, 4 -
maximum is 10, at midnight (0:00).

Run with:
    python -m app.scripts.backfill_dilr_2024_slot3_set3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"

# id -> correct_answer
ANSWERS = {
    687: "2",               # How many times must the AC have been turned off? (MCQ)
    688: "34",              # Outside temperature at 1 am
    689: "42",              # Outside temperature at 9 pm
    690: "Either 2 or 3",   # Turned on / setting altered between 11:01pm-1:59am (MCQ)
    691: "10",              # Max |outside - inside| between 11:01pm-1:59am
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, correct_answer in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={qid}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 3 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
