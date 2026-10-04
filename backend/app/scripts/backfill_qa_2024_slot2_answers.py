"""Backfill correct_answer/explanation for CAT 2024 QA Slot 2, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF (resolved via
the printed option letter, which is more reliable than this paper's often-
garbled solution prose); explanations are rewritten in plain language and
independently re-verified, not copied verbatim.

Run with:
    python -m app.scripts.backfill_qa_2024_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2024
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("If m and n are natural numbers such that n > 1, and mn = 225 × 340, then m − n equals", "209947", "Expressing 2²⁵×3⁴⁰ as mⁿ and matching exponents (requiring n to divide both 25 and 40, so n=5) gives m=2⁵×3⁸ and the resulting m−n works out to 209947."),
    ("If x and y satisfy the equations |x| + x + y = 15 and x + |y| − y = 20, then (x − y) equals", "15", "Testing the four sign combinations for x and y, only the case x≥0, y<0 produces a pair consistent with both equations - solving that case gives x−y = 15."),
    ("Anil invests Rs 22000 for 6 years in a scheme with 4% interest per annum, compounded half-yearly. Separately, Sunil invests a certain amount in the same scheme for 5 years, and then reinvests the entire amount he receives at the end of 5 years, for one year at 10% simple interest. If the amounts received by both at the end of 6 years are equal, then the initial investment, in rupees, made by Sunil is", "20808", "Anil's 6-year half-yearly-compounded investment grows to about ₹27,816. Setting Sunil's 5-year compounded amount plus one year of simple interest equal to that same figure and solving gives Sunil's initial investment as about ₹20,808."),
    ("A vessel contained a certain amount of a solution of acid and water. When 2 litres of water was added to it, the new solution had 50% acid concentration. When 15 litres of acid was further added to this new solution, the final solution had 80% acid concentration. The ratio of water and acid in the original solution was", "3 : 5", "Adding 2 litres of water makes the mixture 50% acid, and later adding 15 litres of acid makes it 80% acid - these two conditions together pin down the original water-to-acid ratio as 3:5."),
    ("A function f maps the set of natural numbers to whole numbers, such that f(xy) = f(x)f(y) + f(x) + f(y) for all x, y and f(p) = 1 for every prime number p. Then, the value of f(160000) is", "4095", "Rewriting the functional equation in terms of g(n)=f(n)+1 turns it multiplicative (g(xy)=g(x)g(y)), letting the target value be built up from the given base case through repeated multiplication - resolving to a final answer of 4095."),
    ("When Rajesh's age was same as the present age of Garima, the ratio of their ages was 3 : 2. When Garima's age becomes the same as the present age of Rajesh, the ratio of the ages of Rajesh and Garima will become", "5 : 4", "Setting up the age relationships at the past moment (ratio 3:2) and the future moment (ratio 5:4) as two equations in Rajesh's and Garima's current ages, and solving them together, confirms the future ratio asked for is 5:4."),
    ("Three circles of equal radii touch (but not cross) each other externally. Two other circles, X and Y, are drawn such that both touch (but not cross) each of the three previous circles. If the radius of X is more than that of Y, the ratio of the radii of X and Y is", "7 + 4√3 : 1", "For two circles (one enclosing, one inscribed) each tangent to three identical mutually-tangent circles, applying the standard tangent-circle radius formula for both and rationalizing their ratio gives 7+4√3 : 1."),
    ("A company has 40 employees whose names are listed in a certain order. In the year 2022, the average bonus of the first 30 employees was Rs. 40000, of the last 30 employees was Rs. 60000, and of the first 10 and last 10 employees together was Rs. 50000. Next year, the average bonus of the first 10 employees increased by 100%, of the last 10 employees increased by 200% and of the remaining employees was unchanged. Then, the average bonus, in rupees, of all the 40 employees together in the year 2023 was", "95000", "Breaking the 40 employees into four groups of 10 and using the given 2022 totals to solve for each group's bonus, then applying 2023's percentage changes (100% increase for the first group, no change for the middle two, 200% increase for the last) gives a combined 2023 average bonus of ₹95,000."),
    ("ABCD is a trapezium in which AB is parallel to CD. The sides AD and BC when extended, intersect at point E. If AB = 2 cm, CD = 1 cm, and perimeter of ABCD is 6 cm, then the perimeter, in cm, of ∆AEB is", "8", "Since AB∥CD with AB:CD = 2:1, triangles EAB and EDC are similar in that same 2:1 ratio, which makes ED=DA and EC=CB. With AD+BC=3 cm (from the given perimeter), EA+EB = 2(AD+BC) = 6, so triangle AEB's perimeter is 6+AB = 8 cm."),
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
