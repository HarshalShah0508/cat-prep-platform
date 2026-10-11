"""Fix the CAT 2024 DILR Slot 2 "daily product ratings" set: the Day 2
distribution stored in passage_text was wrong (75 buyers: 10,5,15,20,25)
versus the real official data (50 buyers: 5,10,5,20,10) - confirmed via web
search cross-check. Also fills the 2 missing answers (id 250, 252), which
both depend on/relate to this corrected data. id 253's existing answer
("between 5% and 8%") turns out to already be correct once the Day 2 data
is fixed, so it's left untouched.

Run with:
    python -m app.scripts.backfill_dilr_2024_slot2_ratings_set
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

CORRECTED_PASSAGE = (
    "An online e-commerce firm receives daily integer product ratings from 1 through 5 given by buyers. "
    "The daily average is the average of the ratings given on that day. The cumulative average is the "
    "average of all ratings given on or before that day. The rating system began on Day 1, and the "
    "cumulative averages were 3 and 3.1 at the end of Day 1 and Day 2, respectively. The distribution of "
    "ratings on Day 2 was: 5 buyers gave a rating of 1, 10 buyers gave a rating of 2, 5 buyers gave a "
    "rating of 3, 20 buyers gave a rating of 4, and 10 buyers gave a rating of 5 (50 buyers total, total "
    "rating points 170).\n\n"
    "The following information is known about ratings on Day 3.\n"
    "1. 100 buyers gave product ratings on Day 3.\n"
    "2. The modes of the product ratings were 4 and 5.\n"
    "3. The numbers of buyers giving each product rating are non-zero multiples of 10.\n"
    "4. The same number of buyers gave product ratings of 1 and 2, and that number is half the number of "
    "buyers who gave a rating of 3."
)

ANSWER_FIXES = {
    250: {
        "correct_answer": "150",
        "explanation": "Day 2's daily average is 170/50=3.4. With x Day 1 buyers (daily average 3, so total 3x), the cumulative average after Day 2 is (3x+170)/(x+50)=3.1. Solving: 3x+170=3.1x+155, so 0.1x=15 and x=150.",
    },
    252: {
        "correct_answer": "4",
        "explanation": "With 100 Day 3 buyers, modes 4 and 5 tied for highest frequency, counts as non-zero multiples of 10, and rating-1 count = rating-2 count = half of rating-3 count: solving gives counts 10,10,20,30,30 for ratings 1-5. Cumulatively, the 50th and 51st (of 100) values both fall in the rating-4 bracket (cumulative count 40 after rating 3, 70 after rating 4), so the median is 4.",
    },
}


def backfill() -> None:
    db = SessionLocal()
    try:
        set_rows = (
            db.query(CatQuestion)
            .filter(
                CatQuestion.section == "DILR",
                CatQuestion.source_year == 2024,
                CatQuestion.source_slot == "slot2",
                CatQuestion.group_id == (
                    db.query(CatQuestion.group_id).filter(CatQuestion.id == 250).scalar_subquery()
                ),
            )
            .all()
        )
        for row in set_rows:
            row.passage_text = CORRECTED_PASSAGE
        print(f"Corrected passage_text on {len(set_rows)} rows in this set.")

        updated = 0
        for question_id, fix in ANSWER_FIXES.items():
            row = db.query(CatQuestion).filter(CatQuestion.id == question_id).first()
            if row is None:
                print(f"NO MATCH: id={question_id}")
                continue
            row.question_type = "TITA"
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT 2024 DILR Slot 2 answers.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
