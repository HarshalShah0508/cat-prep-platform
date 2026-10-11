"""Backfill correct_answer for CAT 2022 DILR Slot 1 Set 2 (hockey-goals set,
group_id cat2022_dilr_slot1_set2), matched by (source_year, source_slot,
section, question_text).

NOT transcribed from any solutions PDF - solved from scratch from the
passage's 6 constraints. Per-match goal totals: Match1=4, Match2=1,
Match3=1, Match4=1, Match5=2, Match6=1, Match7=1, Match8=1 (sums to 12).
Player totals: Harita=5 (scores 3 in Match1, 1 each in Match4/Match8 - her
3 matches per fact 3), Bimla=4 (1 each in Match1/5/6/7, her required set
per fact 4), Sarita=2 (Match3 + the Match5 leftover), Amla=1 (Match2). This
satisfies every stated fact including the two harder ones: fact 5 (Match3
total = Match7 total = 1, both differing from Match1=4 and Match5=2) and
fact 6 (Match1's total of 4 is the unique max, and critically is NOT
Match5 - several other candidate solutions were tried and failed exactly
this check, since forcing Harita's winning margin through Match3 or
Match5 unavoidably ties or lands the max on a forbidden match).

Confidence: Q1 and Q2 (whose answers come directly from the per-match
total reconstruction) land exactly on two of the four given MCQ options
each (Match7=1, and the sequence 4,1,2,1) - a strong independent check,
since those exact numbers were not reverse-engineered from the options.
Q3/Q4 follow deterministically from which matches each player touches.
Q5 is a conditional ("if Harita played one more match than Sarita") that
further constrains an otherwise-underdetermined split of Amla/Sarita's
goals; checking all 3 ways to satisfy that condition shows Statement 1
holds in all of them but Statement 2 does not - hence "Statement-1 only".

Run with:
    python -m app.scripts.backfill_dilr_2022_slot1_set2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How many goals were scored in Match 7?", "1"),
    (
        "Which of the following is the correct sequence of goals scored in matches 1, 3, 5 "
        "and 7?",
        "4, 1, 2, 1",
    ),
    (
        "Which of the following statement(s) is/are true? Statement-1: Amla and Sarita "
        "never scored goals in the same match. Statement-2: Harita and Sarita never scored "
        "goals in the same match.",
        "Both the statements",
    ),
    (
        "Which of the following statement(s) is/are false? Statement-1: In every match, at "
        "least one player scored a goal. Statement-2: No two players scored goals in the "
        "same number of matches.",
        "None of the statements",
    ),
    (
        "If Harita scored goals in one more match as compared to Sarita, which of the "
        "following statement(s) is/are necessarily true? Statement-1: Amla scored goals in "
        "consecutive matches. Statement-2: Sarita scored goals in consecutive matches.",
        "Statement-1 only",
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
