"""Backfill correct_answer/explanation for CAT 2024 QA Slot 3, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF (resolved via
the printed option letter, which is more reliable than this paper's often-
garbled solution prose); explanations are rewritten in plain language and
independently re-verified, not copied verbatim.

Run with:
    python -m app.scripts.backfill_qa_2024_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("Rajesh and Vimal own 20 hectares and 30 hectares of agricultural land, respectively, which are entirely covered by wheat and mustard crops. The cultivation area of wheat and mustard in the land owned by Vimal are in the ratio of 5 : 3. If the total cultivation area of wheat and mustard are in the ratio 11 : 9, then the ratio of cultivation area of wheat and mustard in the land owned by Rajesh is", "7 : 9", "With Vimal's 30 hectares split 5:3 between wheat and mustard, and the combined wheat-to-mustard ratio across both farmers' land fixed at 11:9, solving for Rajesh's own wheat-to-mustard split on his 20 hectares gives a ratio of 7:9."),
    ("is divided by 13, the remainder is is", "9", "Using Fermat's Little Theorem (since 13 is prime) to reduce the large exponent, then working out the resulting power modulo 13, gives a remainder of 9."),
    ("A train travelled a certain distance at a uniform speed. Had the speed been 6 km per hour more, it would have needed 4 hours less. Had the speed been 6 km per hour less,it would have needed 6 hours more. The distance, in km, travelled by the train is", "720", "Setting up the two time-difference conditions (4 hours less at +6 km/h, 6 hours more at −6 km/h) as two equations in the original speed and distance, and solving them together, gives a travelled distance of 720 km."),
    ("After two successive increments, Gopal's salary became 187.5% of his initial salary. If the percentage of salary increase in the second increment was twice of that in the first increment, then the percentage of salary increase in the first increment was", "25", "With the first increment of x% followed by a second increment of (x+20)%, the combined effect must multiply the salary by 1.875. Solving the resulting quadratic for x gives a first increment of 25%."),
    ("In a group of 250 students, the percentage of girls was at least 44% and at most 60%. The rest of the students were boys. Each student opted for either swimming or running or both. If 50% of the boys and 80% of the girls opted for swimming while 70% of the boys and 60% of the girls opted for running, then the minimum and maximum possible number of students who opted for both swimming and running, are", "72 and 80, respectively", "Using inclusion-exclusion on the swimming and running participation among boys and girls, and testing the extremes of the 44%-60% girls range, gives a minimum of 72 and a maximum of 80 students who participated in both activities."),
    ("Gopi marks a price on a product in order to make 20% profit. Ravi gets 10% discount on this marked price, and thus saves Rs 15. Then, the profit, in rupees, made by Gopi by selling the product to Ravi, is", "10", "With the marked price set at 1.2× cost price and a 10% discount on that mark-up saving Ravi ₹15, solving for the cost price and then the actual selling price shows Gopi's real profit on this sale was ₹10."),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "QA",
                    CatQuestion.question_text == question_text,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
