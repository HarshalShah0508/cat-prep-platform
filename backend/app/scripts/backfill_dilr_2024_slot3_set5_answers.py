"""Backfill correct_answer for CAT 2024 DILR Slot 3 Set 5 (ATM network grid
set, group_id cat2024_slot3_dilr_set5), matched by id.

Not transcribed from any solutions PDF - solved from scratch directly from
the grid figure in DILR_SLOT3_CAT_2024.pdf (page 9): 3 horizontal roads
R-A/R-B/R-C and 3 vertical roads V1/V2/V3, with V1-V2=4km, V2-V3=7km,
R-A-R-B=3km, R-B-R-C=5km. Row cash-requirement totals: R-A=22, R-B=20,
R-C=20. Column totals: V1=15, V2=21, V3=26. Six of the nine intersections
have an ATM, each with a distinct integer cash requirement in Lakhs; given
facts: (1) the min (7) and max (15) ATMs share a road; (2) the road
(Manhattan) distance from the 2nd-highest-cash ATM to the ATM at (R-C,V3)
is 12 km.

Using grid coordinates (V1=0,V2=4,V3=11 horizontally; R-A=0,R-B=3,R-C=8
vertically), checking every intersection's distance to (R-C,V3)=(11,8)
shows only (R-B,V2) is exactly 12 km away - so the 2nd-highest ATM sits at
(R-B,V2). Testing the "exactly one empty cell per row and per column"
structures consistent with that (4 candidate permutations), only one
(empty cells at R-A/V2, R-B/V3, R-C/V1) yields an integer solution matching
every row/column sum, all-distinct values, and min=7/max=15 - with a free
parameter u solved uniquely at u=7 (every other integer u in range produces
a duplicate value or the wrong min/max). The resulting grid:
    V1    V2    V3
R-A  7     -    15
R-B  8    12     -
R-C  -     9    11
(min=7 at R-A/V1, max=15 at R-A/V3 - both on road R-A, confirming fact 1;
2nd-highest=12 at R-B/V2, confirming fact 2's distance exactly).

Q18: (R-C,V2)=9 Lakhs. Q19: values >=10 are 11,12,15 -> 3 ATMs. Q20: every
row and every column has exactly 2 ATMs in this grid, so both statements
are true. Q21: 2nd-highest(12, at R-B/V2) to 2nd-lowest(8, at R-B/V1) are on
the same row, distance = |V2-V1| = 4 km. Q22: the full grid (all 6
locations and values) is uniquely determined, so all 6 ATMs qualify.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot3_set5_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"

# id -> correct_answer
ANSWERS = {
    696: "The ATM placed at the (R-C, V2) intersection has a cash requirement of Rs. 9 Lakhs.",  # MCQ
    697: "3",     # How many ATMs have cash requirements of Rs. 10 Lakhs or more?
    698: "Both Statement A and Statement B",  # MCQ
    699: "4 km",  # Road distance between 2nd-highest and 2nd-lowest cash ATMs (MCQ)
    700: "6",     # Number of ATMs whose location and cash requirement are both unique
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 5 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
