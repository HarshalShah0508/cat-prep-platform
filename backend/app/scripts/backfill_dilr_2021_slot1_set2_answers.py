"""Backfill correct_answer for CAT 2021 DILR Slot 1 Set 2 (journal papers /
eight authors set, group_id cat2021_dilr_slot1_set2), matched by
(source_year, source_slot, section, question_text).

Solved from scratch (no solutions PDF/answer key available for this slot):
with A,D,G,H capped at 1-3 papers each summing to 12, all four are forced to
exactly 3; B+C+E+F sum to 6 with F=1 fixed, giving B+C+E=5. Country/area
assignments follow directly from the automation-is-Indian-only rule plus
the "same country" and "no shared issue" clues for B/G. Issue schedule
falls out from capacity (5/5/4/4 across Jan/Apr/Jul/Oct) combined with the
B-G no-overlap rule (forces G to skip April, since B always has an April
paper) and the C/E consecutive-vs-not split (unique: E in Apr+Jul, C in
Jan+Oct - the only split where one is consecutive and the other isn't).

Run with:
    python -m app.scripts.backfill_dilr_2021_slot1_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot1"

ANSWERS = [
    (
        "What is the correct sequence of number of papers written by B, C, E and G, "
        "respectively?",
        "1, 2, 2, 3",
    ),
    ("How many papers were written by Indian authors?", "8"),
    (
        "Which of the following statement(s) MUST be true? Statement A: Every issue had "
        "at least one paper by author(s) from each country. Statement B: Every issue had "
        "at most two papers by author(s) from each area.",
        "Only Statement A",
    ),
    (
        "Which of the following statements is FALSE?",
        "Every issue had exactly two papers by authors from Logistics area.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        # Two questions share the literal text "Which of the following statements is
        # FALSE?" - match them in source order since .filter() alone can't distinguish.
        rows = (
            db.query(CatQuestion)
            .filter(
                CatQuestion.source_year == SOURCE_YEAR,
                CatQuestion.source_slot == SOURCE_SLOT,
                CatQuestion.section == "DILR",
                CatQuestion.group_id == "cat2021_dilr_slot1_set2",
                CatQuestion.question_text == "Which of the following statements is FALSE?",
            )
            .order_by(CatQuestion.id)
            .all()
        )
        false_answers = [
            "Every issue had exactly two papers by authors from Logistics area.",
            "There were exactly two papers by authors from Manufacturing area in the "
            "July issue.",
        ]
        for row, ans in zip(rows, false_answers):
            row.correct_answer = ans
            db.flush()
            updated += 1

        for question_text, correct_answer in ANSWERS:
            if question_text == "Which of the following statements is FALSE?":
                continue
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "DILR",
                    CatQuestion.group_id == "cat2021_dilr_slot1_set2",
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

        row = (
            db.query(CatQuestion)
            .filter(
                CatQuestion.source_year == SOURCE_YEAR,
                CatQuestion.source_slot == SOURCE_SLOT,
                CatQuestion.section == "DILR",
                CatQuestion.group_id == "cat2021_dilr_slot1_set2",
                CatQuestion.question_text
                == "Which of the following is the correct sequence of number of papers "
                "by authors from Automation, Manufacturing and Logistics areas, "
                "respectively?",
            )
            .first()
        )
        if row is not None:
            row.correct_answer = "6, 5, 7"
            db.flush()
            updated += 1
        else:
            print("NO MATCH: Automation/Manufacturing/Logistics sequence question")

        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} Set 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
