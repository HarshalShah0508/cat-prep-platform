"""Backfill correct_answer for CAT 2024 DILR Slot 1 Set 2 (six web surfers /
four bloggers stars set, group_id cat2024_slot1_dilr_set2), matched by id.

Not transcribed from any solutions PDF - solved from scratch directly from
the chart in DILR_SLOT1_CAT_2024.pdf (page 2): stars given to bloggers A and
B by each of the six surfers (M, N, O, P, X, Y):
  M: A=10, B=0   N: A=25, B=0   O: A=0, B=0
  P: A=5, B=25   X: A=0, B=0    Y: A=5, B=20

Each surfer gives 30 stars total. Totals received by A (10+25+0+5+0+5=45)
and B (0+0+0+25+0+20=45) already match the "all bloggers received the same
total" fact exactly, so O and X (who gave 0 to both A and B) must have given
their full 30 stars entirely to C or D (consistent with fact 4: "two
surfers gave all their stars to a single blogger" - these are the only two
candidates, since every other surfer already splits across at least A/B and
C/D). Total needed for C and D is 45 each (180 total / 4 bloggers); the
non-O/X contribution to C+D is M(20)+N(5)+P(0)+Y(5)=30, so O and X supply
the remaining 60 between them - one giving all 30 to C, the other all 30 to
D (giving both to the same blogger would push that blogger's total to 60+,
exceeding 45, which is impossible).

Fact 3 (each blogger received a different amount from M: M gave A=10, B=0,
so M's C and D amounts must differ from each other and from 10 and 0, while
summing to 20 - only {5,15} fits) and fact 5 (D > C from Y, with Y's C+D=5,
multiples of 5 - only {C=0, D=5} fits) pin down Y_D=5 directly (Q6).
Total stars received by D = 45 globally (Q5, from the equal-totals fact).
Counting how many bloggers each surfer spread stars across: M->3 (A,C,D),
N->2 (A + one of C/D), O->1, P->2 (A,B), X->1, Y->3 (A,B,D); so exactly 2
surfers (N and P) used exactly 2 bloggers (Q7).

Run with:
    python -m app.scripts.backfill_dilr_2024_slot1_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot1"

# id -> correct_answer
ANSWERS = {
    648: "45",  # What was the total number of stars received by D?
    649: "5",   # What was the number of stars received by D from Y? (MCQ)
    650: "2",   # How many surfers distributed their stars among exactly 2 bloggers?
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
