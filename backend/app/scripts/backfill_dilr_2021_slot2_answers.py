"""Backfill missing correct_answer/explanation for CAT 2021 DILR Slot 2 PYQ rows.

Sources:
- Set 1 (order/ship-mode bar chart, ids 504/505/507): the "_SOLUTIONS" PDF for this
  set is reliable for Q1 and Q4, but Q2 ("average processing time ... only one
  ship mode") has no resolvable number in that PDF - it was worked out here
  directly from the bar chart image in DILR_SLOT2_CAT_2021.pdf (page 1): the only
  two categories with a single ship mode are Accessories (one Standard-Class
  order, Sep 1 -> Sep 19, 18 days) and Envelopes (one Standard-Class order,
  Sep 3 -> Sep 7, 4 days), giving an average of (18 + 4) / 2 = 11 days.
- Set 2 (ten-object envy allocation among Amar/Barat/Charles/Disha/Elise, ids
  508-513): the "_SOLUTIONS" PDF does not cover this set at all (its content for
  slot 2 beyond set 1 is garbled/unrelated to the real paper). The values table
  needed to solve it only exists as an image in DILR_SLOT2_CAT_2021.pdf (page 2)
  and was read off there, then the puzzle was solved by exhaustive search over
  all ways to partition the 10 objects into 5 bundles of 2, checking the 6 given
  facts - exactly one assignment satisfies all of them:
    Barat = {o7, o9} (16), Elise = {o5, o10} (16), Charles = {o3, o8} (16),
    Amar = {o2, o6} (12), Disha = {o1, o4} (13).

Matched by id directly (ids pulled from a DB query for source='pyq' AND
source_year=2021 AND source_slot='slot2' AND section='DILR' AND
correct_answer IS NULL). Every update is guarded by `correct_answer.is_(None)`
so an already-answered row can never be clobbered.

Run with:
    python -m app.scripts.backfill_dilr_2021_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot2"

_ENVY_SOLUTION_NOTE = (
    "Solving the full puzzle (facts 1-6: the '10'-value rule, o1/o2/o3 to three "
    "different people, o1 and o8 to different people, exactly three bundles worth "
    "16 with none higher, Disha's bundle odd and everyone else's even, and envy "
    "only flowing from a sub-16 person to a 16-valuer) gives a unique allocation: "
    "Barat = {o7, o9} = 16, Elise = {o5, o10} = 16, Charles = {o3, o8} = 16, "
    "Amar = {o2, o6} = 12, Disha = {o1, o4} = 13. Amar envies Barat and Charles; "
    "Disha envies Barat."
)

# id -> (correct_answer, explanation)
ANSWERS = {
    # --- Set 1: order / ship-mode bar chart ---
    504: (
        "1",
        "Reading the booking days (left edges of the bars) for every category between "
        "Sep 1 and Sep 14 gives Sep 1-11, 13, 14 - only Sep 12 has no booking.",
    ),
    505: (
        "11",
        "The only two categories that used a single ship mode throughout are Accessories "
        "(one Standard-Class order, booked Sep 1 and dispatched Sep 19 - 18 days) and "
        "Envelopes (one Standard-Class order, booked Sep 3 and dispatched Sep 7 - 4 days). "
        "Average processing time = (18 + 4) / 2 = 11 days.",
    ),
    507: (
        "20%",
        "Counting orders with a processing time of exactly one day against the total "
        "number of orders placed between Sep 1 and Sep 22 works out to approximately 20%.",
    ),
    # --- Set 2: envy-free allocation of o1..o10 ---
    508: ("o8 was given to Charles", _ENVY_SOLUTION_NOTE),
    509: ("Amar", _ENVY_SOLUTION_NOTE + " Amar is the one who envies someone else."),
    510: ("12", _ENVY_SOLUTION_NOTE + " Amar's own bundle {o2, o6} is worth 9 + 3 = 12 to him."),
    511: ("Disha", _ENVY_SOLUTION_NOTE + " Object o4 is part of Disha's bundle {o1, o4}."),
    512: ("Elise", _ENVY_SOLUTION_NOTE + " Object o5 is part of Elise's bundle {o5, o10}."),
    513: ("o1 was given to Disha", _ENVY_SOLUTION_NOTE),
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, (correct_answer, explanation) in ANSWERS.items():
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH / already answered: id={question_id}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
