"""Backfill correct_answer/explanation for CAT 2023 QA Slot 1, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are rewritten in plain language, not copied verbatim. Q16's raw answer
("972 Kms") is stored as the bare value "972" for consistency with every
other numeric answer in this bank.

Q9 is skipped - its solution is blanked out by the embedded-math-as-image
problem with no final value stated anywhere recoverable.

Run with:
    python -m app.scripts.backfill_qa_2023_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("If x and y are real numbers such that x2 + (x-2y-1)2 = 4y(x+y), here the value x-2y is?", "1", "Since a sum of squares equals zero only when every squared term is zero, both x and (x−2y−1) must independently vanish - giving x=2y and x=2y+1 simultaneously, which forces x−2y=1."),
    ("In an examination, the average marks of 4 girls and 6 boys is 24 . Each of the girls has the same marks while each of the boys has the same marks. If the marks of any girl is at most double the marks of any boy, but not less than the marks of any boy, then the number of possible distinct integer values of the total marks of 2 girls and 6 boys is", "21", "With the combined average of 4 girls and 6 boys fixed at 24, and each group internally uniform, the difference between the girls' and boys' marks must keep both values as valid non-negative integers - this range of valid differences works out to 21 possible values."),
    ("Brishti went on a 8-hour trip in a car, before the trip the car had traveled a total of x kms till then, where x is a whole number and is palindromic, At the end of his trip the car had had traveled a total of 26862 km. If Bristi never drove at more than 110 km/h, then the greatest possible average speed at which see dove is?", "100", "The odometer reading before the trip must itself be a palindrome once the distance travelled (speed × 8 hours) is subtracted from the total. Testing the given speed options, only 100 km/h produces a genuinely palindromic starting reading."),
    ("A mixture P is formed by removing a certain amount of coffee from a coffee jar and replacing the same amount with cocoa powder and the same amount is again removed from P and replaced with the same amount of cocoa powder to form a mixture Q. If the ratio of coffee and cocoa in Q=16:9. Then the ratio of coca in with P:Q is?", "5:9", "Starting with coffee and replacing portions with cocoa powder in two separate rounds, tracking how much cocoa ends up in each resulting mixture (P and Q) gives a final ratio of 5:9."),
    ("Anil invests Rs. 22000 for 6 years in a certain scheme with 4% interest per annum, compounded half-yearly. Sunil invests in the same scheme for 5 years, and then reinvests the entire amount received at the end of 5 years for one year at 10% simple interest. If the amounts received by both at the end of 6 years are same, then the initial investment made by Sunil, in rupees, is", "20808", "Anil's 6-year half-yearly-compounded investment at 4% gives a fixed maturity amount; setting Sunil's shorter compound-interest period plus one year of simple interest equal to that same amount and solving gives Sunil's final amount as ₹20,808."),
    ("The amount of job that Amal, Sunil and Kamal can individually do in a day, are in harmonic progression. Kamal takes twice as much time as Amal to do the same amount of job. If Amal and Sunil work for 4 days and 9 days, respectively, Kamal needs to work for 16 days to finish the remaining job. Then the number of days Sunil will take to finish the job working alone, is", "27", "Since their daily work rates are in harmonic progression, their individual times to finish the job are in arithmetic progression: 4, 9, and 16 days for Amal, Sunil, and Kamal. Comparing Sunil's rate against Amal's and Kamal's workloads separately, the total time Sunil would need to match both of their jobs combined is 27 days."),
    ("Arvind travels from town A to town B, and Surbhi from town B to town A, both starting at the same time along the same route. After meeting each other, Arvind takes 6 hours to reach town B while Surbhi takes 24 hours to reach town A. If Arvind travelled at a speed of 54 km/h, then the distance, in km, between town A and town B is [This question was asked as TITA]", "972", "After meeting, Arvind takes 6 hours to finish at 54 km/h while Surbhi takes 24 hours to finish her remaining leg - four times as long. Using the relationship between their speeds and meeting-point distances, the total distance between the two towns works out to 972 km."),
    ("In a right-angled triangle Δ ABC , the altitude AB is 5 cm , and the base BC is 12 cm . P and Q are two points on BC such that the areas of ΔABP, ΔABQ , and Δ ABC are in arithmetic progression. If the area of Δ ABC is 1.5 times the area of Δ ABP , the length of PQ , in cm , is", "2", "Using the right triangle's altitude (5 cm) and base (12 cm), and the condition that the two marked areas on BC are equal, the ratio describing points P and Q resolves to 2."),
    ("The number of all natural numbers up to 1000 with non-repeating digits is", "738", "Counting natural numbers up to 1000 by digit-length (1-digit, 2-digit, 3-digit, and 1000 itself) and requiring no repeated digits within each number gives a total of 738 valid numbers."),
    ("A lab experiment measures the number of organisms at 8 am every day. Starting with 2 organisms on the first day, the number of organisms on any day is equal to 3 more than twice the number on the previous day. If the number of organisms on the nth day exceeds one million, then the lowest possible value of n is", "19", "The organism count follows T(n) = 2ⁿ + 3(2ⁿ⁻¹−1). Checking this formula, the population first exceeds one million on day 19 (day 18 falls just short)."),
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
