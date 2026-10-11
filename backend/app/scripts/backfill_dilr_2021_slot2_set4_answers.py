"""Backfill correct_answer for CAT 2021 DILR Slot 2 Set 4 (Ravi's customer
ratings set, group_id cat2021_dilr_slot2_set4), matched by (source_year,
source_slot, section, question_text).

Solved from scratch (no solutions PDF/answer key available for this slot).
Behaviour is forced (range 5-7, unique max/min): Atal=7, Bihari=Chirag=6,
Deepak=5. Timeliness forces Atal to be the lone different value among four,
with two algebraic solutions (t=5,Atal=6 or t=4,Atal=9). Packaging/Hygiene
have two solution branches each from the rank-matching fact (Atal and
Deepak must occupy the same relative rank in both parameters). Combined,
that's 4 total scenarios - three of them produce a required tip amount of
60 for a single customer under the "bonus at total>=25, tip 30 or 50
otherwise" rule, which is impossible, leaving exactly one internally
consistent scenario: Packaging {Bihari=9, Chirag=8, Deepak=7, Atal=5},
Hygiene {Chirag=8, Bihari=7, Deepak=6, Atal=5}, Timeliness {Atal=6,
Bihari=Chirag=Deepak=5}. Bihari and Chirag both total 27 (bonus, no tip);
Atal and Deepak both total 23 (no bonus), splitting tips 30/50 between
them to make the totals sum to 120 - which one of them gets which is NOT
determinable from the given facts, so that specific split is not asserted.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot2_set4_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot2"

ANSWERS = [
    (
        "What was the minimum rating that Ravi received from any customer in any "
        "parameter?",
        "5",
    ),
    (
        "The COMPLETE list of customers who gave the maximum total rating points to "
        "Ravi is",
        "Bihari and Chirag",
    ),
    ("What rating did Atal give on Timeliness?", "6"),
    (
        "What BEST can be concluded about the tip amount given by Deepak?",
        "Either 30 or 50",
    ),
    (
        "In which parameter did Atal give the maximum rating points to Ravi?",
        "Behaviour",
    ),
    ("What rating did Deepak give on Packaging?", "7"),
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
                    CatQuestion.group_id == "cat2021_dilr_slot2_set4",
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
