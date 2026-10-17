"""Backfill correct_answer for CAT 2022 DILR Slot 3 Set 2 (Pulak/Qasim/
Ritesh/Suresh coin-betting set, group_id cat2022_dilr_slot3_set2), ids 589,
590 and 593. Matched directly by id, guarded so an already-filled
correct_answer is never overwritten.

Sourced from pyq-source/2022/DILR_SLOT3_CAT_2022_SOLUTIONS.pdf:
  - Q2.1 (id 589): "...amount of money that Ritesh had with him at the end
    of Round 8?" -> Correct Answer: (C) Exactly Rs.6
  - Q2.2 (id 590): "...amount of money that Pulak had with him at the end
    of Round 6?" -> Correct Answer: (A) Exactly Rs.12
  - Q2.5 (id 593): "Which of the following pairings was made in Round 5?"
    -> Correct Answer: (C) Pulak and Suresh

NOTE: id 592 ("How many games were played with a bet of Rs.2?", TITA) is
deliberately NOT included here. The source PDF leaves its "Correct Answer:"
field blank and its own worked solution is internally contradictory (it
tallies 4 games, then second-guesses itself with "needs alignment... the
disorder might have damaged the VIIIth round treatment" before asserting a
different final count of 6 with no valid derivation) - it also fabricates a
per-round amount table that does not conserve the fixed total of Rs.40
across the four players (e.g. Round 2 sums to 37, not 40), so none of its
numbers can be trusted. Left correct_answer NULL per instructions rather
than guess.

Run with:
    python -m app.scripts.backfill_dilr_2022_slot3_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot3"

ANSWERS = [
    (589, "Exactly ₹6"),
    (590, "Exactly ₹12"),
    (593, "Pulak and Suresh"),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, correct_answer in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH (or already filled): id={question_id}")
                continue
            row.correct_answer = correct_answer
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
