"""Backfill correct_answer for CAT 2025 DILR Slot 1 Set 2 (group
promotion/rating puzzle, group_id cat2025_slot1_set2), matched by
(source_year, source_slot, section, question_text).

Only 2 of the 5 questions are answered here. The full quarter-by-quarter
reconstruction is solid through Q3 (Bunty demoted end-Q1, Asha demoted
end-Q2, Chintu demoted end-Q3; Novice-for-Q3 = {Bunty, Dolly, Asha} with
Lalu ratings Asha=1, Dolly=2, Bunty=3 - giving Q3) and pins Asha's Q2
rating at 1 in every valid branch (giving Q5). But fact 2 ("Dolly and
Falguni were the only employees who got the same rating across all the
quarters") cannot be reconciled with the rest of the puzzle under either
reading tried: read as "Falguni's own rating never changes quarter to
quarter," neither candidate for Falguni (the Novice member promoted after
Q1, nor the one promoted after Q2) ever turns out to have a constant
rating in any valid branch; read as "Dolly and Falguni get the same
rating AS EACH OTHER," that's impossible outright since they're both in
Novice together in Q1 and in-group ratings must be distinct that quarter.
Q1 (Eklavya's score, which needs Eklavya's P1/N1 identity - exactly what
this contradiction leaves unresolved), Q2 (group-change count, same
dependency), and Q4 (count of certainly-known Q3 scores, same dependency)
are left unanswered rather than guessed.

Run with:
    python -m app.scripts.backfill_dilr_2025_slot1_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("What was Bunty's score at the end of Quarter 3?", "5"),
    (
        "Which of the following statements is/are NECESSARILY true?\n"
        "I. Asha received a rating of 2 in Quarter 1.\n"
        "II. Asha received a rating of 1 in Quarter 2.",
        "Only II",
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
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
