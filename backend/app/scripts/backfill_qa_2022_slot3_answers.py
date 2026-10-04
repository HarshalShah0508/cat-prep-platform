"""Backfill correct_answer/explanation for CAT 2022 QA Slot 3, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF, with Q1/Q5
independently re-derived from the intact question text (their own solutions
print "Correct Answer: --" with only a partial/blanked derivation) and
cross-checked for internal consistency; explanations are rewritten in plain
language, not copied verbatim.

Q4, Q12, Q15 are skipped - their solutions are blanked out by the embedded-
math-as-image problem with no final value stated anywhere recoverable.

Run with:
    python -m app.scripts.backfill_qa_2022_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("A donation box can receive only cheques of ₹100,₹250 and ₹500. On one good day,the donation box was found to contain exactly 100 cheques amounting to a total sum of ₹15250. Then, the maximum possible number of cheques of ₹500 that the donation box may have contained,is", "12", "With 100 cheques totaling ₹15250 across ₹100/₹250/₹500 denominations, simplifying the two equations gives 3b+8c=105 (b = number of ₹250 cheques, c = number of ₹500 cheques). The largest integer c that keeps b a non-negative whole number is 12."),
    ("Bob can finish a job in 40 days,if he works alone. Alex is twice as fast as Bob and thrice as fast as Cole in the same job.Suppose Alex and Bob work together on the first day,Bob and Cole work together on the second day,Cole and Alex work together on the third day and then,they continue the work by repeating this three-day roster,with Alex and Bob working together on the fourth day and so on.Then,the total number of days Alex would have worked when the job gets finished,is", "11", "Bob, Alex, and Cole work at rates 3, 6, and 2 units/day, with the job totaling 120 units (Bob alone takes 40 days). Cycling through the 3-day roster, 15 days complete 110 units, and the job finishes partway through day 17 - with Alex having worked on 10 of the first 15 days plus day 16, for 11 days total."),
    ("Consider six distinct natural numbers such that the average of the two smallest numbers is 14 and the average of the two largest numbers is 28. Then,the maximum possible value of the average of these six numbers is", "22.5", "To maximize the average of six distinct natural numbers with the two smallest averaging 14 and the two largest averaging a fixed value, the middle two numbers should be pushed as high as possible while keeping all six distinct - this gives a maximum overall average of 22.5."),
    ("Two ships are approaching a port along straight routes at constant speeds. Initially,the two ships and the port formed an equilateral triangle with sides of length 24 km. When the slower ship travelled 8 km,the triangle formed by the new positions of the two ships and the port became right-angled. When the faster ship reaches the port, the distance,in km,between the other ship and the port will be", "12", "The two ships and the port start as an equilateral triangle of side 24 km. After the slower ship closes 8 km toward the port while the faster ship's path creates a right angle at the port, the geometry of the resulting right triangle gives the remaining distance between the other ship and the port as 12 km."),
    ("The arithmetic mean of all the distinct numbers that can be obtained by rearranging the digits in 1421, including itself, is", "2222", "The digits of 1421 (with the digit '1' repeated) give 4!/2! = 12 distinct 4-digit rearrangements. By symmetry each digit occupies each place value equally often, and summing out that structure gives a mean of 2222 across all 12 numbers."),
    ("The lengths of all four sides of a quadrilateral are integer valued.If three of its sides are of length 1cm,2cm and 4cm,then the total number of possible lengths of the fourth side is", "5", "For sides 1, 2, 4, and an unknown fourth side x to form a valid quadrilateral, x must satisfy the quadrilateral inequality (each side less than the sum of the other three). Working out that range leaves exactly 5 valid integer values for x."),
    ("Two cars travel from different locations at constant speeds. To meet each other after starting at the same time, they take 1.5 hours if they travel towards each other, but 10.5 hours if they travel in the same direction. If the speed of the slower car is 60km/hr, then the distance traveled, in km,\n\nby the slower car when it meets the other car while traveling towards each other, is", "90", "With the slower car at 60 km/h, comparing the \"towards each other\" (1.5 hr) and \"same direction\" (10.5 hr) meeting scenarios gives an equation for the faster car's speed. Using that speed and the 1.5-hour towards-each-other case, the slower car covers 90 km before they meet."),
    ("The average of all 3-digit terms in the arithmetic progression 38,55,72,...,is", "548", "In the AP 38, 55, 72,... (common difference 17), the 3-digit terms run from 106 up to 990. Averaging an arithmetic progression's terms just means averaging its first and last values, giving (106+990)/2 = 548."),
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
