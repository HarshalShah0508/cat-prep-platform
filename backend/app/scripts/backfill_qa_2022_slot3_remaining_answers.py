"""Backfill correct_answer for the 3 remaining unanswered CAT 2022 QA Slot 3
TITA rows (ids 912, 916, 917) not covered by the earlier
backfill_qa_2022_slot3_answers.py / backfill_qa_2022_slot3_missing_questions.py
scripts. Matched directly by id, guarded so an already-filled correct_answer
is never overwritten.

Sourced from pyq-source/2022/QUANT_SLOT3_CAT_2022_SOLUTIONS.pdf (numeric
final answers read off the rendered solution pages, since the PDF's
"Correct Answer:" text field is blank/image-stripped for all three):
  - Q4 (id 912): medians BD, CE of triangle ABC meet at centroid O, area
    ABC = 108 -> area ADE = 27, centroid splits it BEO:EOD = 2:1, so
    EOD = 27/3 = 9. Boxed final answer: "9 sq cm".
  - Q12 (id 916): section A (avg 32) has 10 fewer students than section B
    (avg 60); combined average must be an integer; find max-min spread of
    section A's student count. The PDF's own algebra has an error (it
    claims the combined average simplifies to "a = y - 5", which is
    degree-inconsistent and wrong), so this was re-derived independently:
    with x = y-10, a = (92y-320)/(2y-10) = 46 + 70/(y-5). For a to be an
    integer, (y-5) must be a divisor of 70; with y >= 11 (so x >= 1),
    valid (y-5) in {7,10,14,35,70} giving x = y-10 in {2,5,9,30,65}.
    Max - min = 65 - 2 = 63. Verified both extremes numerically (x=2,y=12
    -> avg 56; x=65,y=75 -> avg 47 - both integers).
  - Q15 (id 917): Moody's escalator problem - walking at speed W takes 30s,
    at 2W takes 20s; standing still (speed = escalator speed E) takes how
    long? From 30(W+E)=1 and 20(2W+E)=1 (distance=1 unit): W=E=1/60, so
    standing-still time = 1/E = 60 seconds.

Run with:
    python -m app.scripts.backfill_qa_2022_slot3_remaining_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot3"

ANSWERS = [
    (912, "9"),
    (916, "63"),
    (917, "60"),
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
                    CatQuestion.section == "QA",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} remaining answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
