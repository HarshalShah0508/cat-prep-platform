"""Backfill correct_answer for the 3 remaining unanswered CAT 2022 QA Slot 1
TITA rows (ids 890, 900, 901) not covered by the earlier
backfill_qa_2022_slot1_answers.py / backfill_qa_2022_slot1_missing_questions.py
scripts. Matched directly by id, guarded so an already-filled correct_answer
is never overwritten.

Sourced from pyq-source/2022/QUANT_SLOT1_CAT_2022_SOLUTIONS.pdf (the PDF's
"Correct Answer:" line is blank/image-stripped for these three, so the
numeric final answers were read off the rendered solution pages instead):
  - Q5 (id 890): village males/females literacy ratio problem -> worked
    answer "Total number of females = 43200" (verified: k=4 scaling throws
    off the ratio arithmetic the PDF author used - the figure above is from
    the PDF's own page-9 boxed final answer: 43200).
  - Q18 (id 900): "For natural numbers x,y,z, if xy+yz=19 and yz+xz=51,
    minimum possible value of xyz" -> PDF derives y(x+z)=19, z(x+y)=51,
    two valid (x,y,z) triples (16,1,3) and (2,1,17) giving xyz=48 and 34;
    boxed final answer: 34.
  - Q22 (id 901): "ways to distribute 20 identical balloons among 4
    children, each gets a non-zero even number" -> reduces to partitions
    of 10 into 4 positive integers = C(9,3) = 84; boxed final answer: 84.

Run with:
    python -m app.scripts.backfill_qa_2022_slot1_remaining_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot1"

ANSWERS = [
    (890, "43200"),
    (900, "34"),
    (901, "84"),
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
