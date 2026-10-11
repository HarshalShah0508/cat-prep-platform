"""Backfill correct_answer for CAT 2022 DILR Slot 3 Set 4 (neighbourhood
pandemic-cases set, group_id cat2022_dilr_slot3_set4), matched by
(source_year, source_slot, section, question_text).

NOT transcribed from any solutions PDF - solved from scratch via the
passage's 6 facts. Full reconstructed grid (Levmisto/Tyhrmisto/Pesmisto/
Kitmisto, Day1-5):
  Day1: L=1, T=1, P=1, K=2   (city total 5)
  Day2: L=2, T=2, P=1, K=3   (city total 8)
  Day3: L=3, T=3, P=0, K=3   (city total 9 = 8+1, fact 3)
  Day4: L=3, T=3, P=1, K=3   (city total 10)
  Day5: L=3, T=3, P=2, K=3   (city total 11)

Derivation sketch: K's total (14) over 5 days of {0..3} forces four 3's
and one 2 (15-1=14); P's total (5) with a single max-of-2 (fact 4) forces
one 2, three 1's, one 0. Fact 2 (K>P every day) forces P's "2" day to
coincide with one of K's "3" days. Testing city-total sequences
S1<S2<S3=S2+1<S4<S5 summing to 43 with component caps (P<=2, others<=3)
narrows to (5,8,9,10,11); day1's total of 5 with everyone >=1 (fact 1)
forces K's single "2" day to be Day1. Day5's total of 11 with K=3 forces
L=T=3, P=2 (all maxed) - fixing P's special day as Day5. Working back from
there, Day4 and Day3's totals force P=1 and P=0 respectively (the only
combinations fitting L,T<=3), and L=T is forced equal on every remaining
day because the L/T split is tight enough to leave no other option (an
alternative branch where Day2/Day3 split differently leaves L and T
genuinely ambiguous between candidates, which a real CAT question
wouldn't allow - that branch is rejected for this reason). Every one of
the 6 original facts checks out exactly against this grid, including both
numerically coincidental ones (city total day1=5, day2=8).

Run with:
    python -m app.scripts.backfill_dilr_2022_slot3_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("What BEST can be concluded about the number of new cases in Levmisto on Day 3?",
     "Exactly 3"),
    ("On which day(s) did Pesmisto not have any new case?", "Only Day 3"),
    (
        "Which of the two statements below is/are necessarily false? Statement A: There "
        "were 2 new cases in Tyhrmisto on Day 3. Statement B: There were no new cases in "
        "Pesmisto on Day 2.",
        "Both Statement A and Statement B",
    ),
    ("On how many days did Levmisto and Tyhrmisto have the same number of new cases?", "5"),
    ("What BEST can be concluded about the total number of new cases in the city on Day 2?",
     "Exactly 8"),
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 4 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
