"""Backfill correct_answer for CAT 2024 DILR Slot 2 Set 5 (product-ratings
cumulative-average set, group_id cat2024_slot2_dilr_set5), matched by
(source_year, source_slot, section, question_text).

This set's Day 2 bar-chart distribution in the seed passage was corrected
earlier in the same edit that added this script (it previously held
10/5/15/20/25 buyers for ratings 1-5; the real chart, per a user-supplied
screenshot, shows 5/10/5/20/10). All four answers below were independently
derived from that corrected distribution and the given Day 3 constraints,
and all four land exactly on values/options the user's screenshots had
already confirmed (Day 1 buyers = 150, Day 3 daily average = 3.6, Day 3
median = 4, cumulative average increase = "between 5% and 8%") - strong
confirmation the corrected chart values are right.

Day 1: cumulative average 3 at day's end means Day 1's own total = 3 x
(Day 1 buyers). Day 2 total points = 170 (from the corrected distribution).
Solving (3*D1 + 170)/(D1 + 50) = 3.1 gives D1 = 150.

Day 3: letting rating-1 count = rating-2 count = k, rating-3 = 2k, and
testing the two multiple-of-10 values of k consistent with "modes are 4
and 5" (k=20 fails - it makes rating-3's count exceed ratings 4/5) leaves
k=10, giving counts 10/10/20/30/30 for ratings 1-5 (sum 100, points 360).

Run with:
    python -m app.scripts.backfill_dilr_2024_slot2_set5_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("How many buyers gave ratings on Day 1?", "150"),
    ("What is the daily average rating of Day 3?", "3.6"),
    ("What is the median of all ratings given on Day 3?", "4"),
    (
        "Which of the following is true about the cumulative average ratings of Day 2 "
        "and Day 3?",
        "The cumulative average of Day 3 increased by a percentage between 5% and 8% "
        "from Day 2",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.question_text == question_text,
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 5 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
