"""Backfill correct_answer for CAT 2024 DILR Slot 1 Set 1 (Dheeraj/Samantha/
Nitesh countries-visited set, group_id cat2024_slot1_dilr_set1), matched by id.

Not transcribed from any solutions PDF - that PDF's own chart tables for
this set are self-contradictory between consecutive sub-questions (it
re-invents a different Dheeraj/Samantha/Nitesh breakdown for almost every
question), so it was solved from scratch directly from the chart embedded
in DILR_SLOT1_CAT_2024.pdf (page 1), read via pdftoppm at 400dpi.

Chart (bar values, "Number of countries visited"):
  Dheeraj:  Asia=3, Europe=7, ROW=1
  Samantha: Asia=0, Europe=9, ROW=4
  Nitesh:   Asia=1, Europe=6, ROW=12

Facts used: (1) union of all three = 32 countries; (2) USA (ROW) is the only
country visited by all three, i.e. the full D∩S∩N = {USA}, in ROW only;
(3) China (Asia) is the only country visited by D and N but not S - read as
a GLOBAL statement, so D∩N\\S = {China} everywhere, meaning D∩N\\S = 0 in
both Europe and ROW; (4) France (Europe) is the only country outside Asia
visited by D and S but not N, so D∩S\\N = 0 in ROW; (5) half of D∩S∩N... no,
half of S∩N (all regions) are in Europe - since Samantha visited 0 Asian
countries, this means S∩N splits evenly between Europe and ROW.

Region-by-region inclusion-exclusion with those facts resolves every cell
uniquely; the resulting totals (Asia union=3, Europe union=17, ROW union=12)
sum to exactly 32, confirming the solution. Full breakdown used:
  Asia:   D∩N (excl. S) = China = 1; union = 3+1-1 = 3.
  Europe: D∩S (excl. N) = France = 1; D∩N (excl. S) = 0; S∩N (full) = 4;
          D-only=6, S-only=4, N-only=2 (exactly-one total = 12).
  ROW:    triple (USA) = 1; D∩N (full, excl. triple) = 0 (Dheeraj's only ROW
          country is USA itself, since D_ROW total = 1); D∩S (full) = 1
          (also just USA); S∩N (full) = 4 (the other half of the 8 total
          S∩N countries); N-only = 8.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot1_set1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot1"

# id -> correct_answer
ANSWERS = {
    644: "3",   # How many countries in Asia were visited by at least one of D, S, N?
    645: "2",   # How many countries in Europe were visited only by Nitesh?
    646: "4",   # How many countries in the ROW were visited by both Nitesh and Samantha?
    647: "12",  # How many countries in Europe were visited by exactly one of D, S, N? (MCQ)
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 1 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
