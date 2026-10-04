"""Backfill correct_answer/explanation for CAT 2022 QA Slot 2, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are rewritten in plain language, not copied verbatim.

Several TITA questions print "Correct Answer: --" (the real value is only
stated inside the solution prose, e.g. "Hence, the answer is 47" or
"Correct Option: 24"). Q15 is independently re-derived from the intact
question text since its own solution is blanked out by the embedded-math
problem. Q19 is skipped entirely - both its raw answer and its solution are
blanked with no recoverable final value.

Run with:
    python -m app.scripts.backfill_qa_2022_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2022
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("The number of distinct integer values of n satisfying , is", "47", "The fraction is negative only when its numerator and denominator have opposite signs, which happens exactly for n strictly between 16 and 64. That range contains 47 integers."),
    ("If a and b are non-negative real numbers such that a+2b=6, then the average of the maximum and minimum possible values of (a+b) is", "4.5", "From a+2b=6 with both non-negative, a+b ranges between b=0 (a+b=6) and a=0 (a+b=3). Averaging these two extremes gives 4.5."),
    ("The number of integers greater than 2000 that can be formed with the digits 0,1,2,3,4,5 using each digit at most once,is", "1440", "Counting integers above 2000 formed from 0-5 (no repeats) by thousands-digit range (2xxx, 3-4xxx, 5xxx) and summing each case's permutation count gives 1440 valid numbers."),
    ("Manu earns ₹4000 per month and wants to save an average of ₹550 per month in a year. In the first nine months, his monthly expense was ₹3500, and he foresees that, tenth month onward, his monthly expense will increase to ₹3700. In order to meet his yearly savings target, his monthly earnings, in rupees, from the tenth month onward should be", "4400", "Manu needs ₹6600 total savings for the year; the first 9 months at ₹500/month savings cover ₹4500, leaving ₹2100 to save over the last 3 months (₹700/month). With expenses rising to ₹3700/month in that period, he needs to earn ₹4400/month."),
    ("On day one,there are 100 particles in a laboratory experiment.On day n,where n≥2,one out of every n particles produces another particle.If the total number of particles in the laboratory experiment increases to 1000 on day m,then m equals", "19", "Each day after the first, the particle count rises by a steady 50 (half of 100, a third of 150, etc. all equal 50). Going from 100 to 1000 needs 900 more particles, which takes 18 more days - day 19."),
    ("Five students,including Amit,appear for an examination in which possible marks are integers between 0 and 50,both inclusive.The average marks for all the students is 38 and exactly three students got more than 32.If no two students got the same marks and Amit got the least marks among the five students,then the difference between the highest and lowest possible marks of Amit is", "20", "With the five students averaging 38 (total 190) and exactly three scoring above 32, testing the extreme assignments for the top three scores while keeping all marks distinct gives Amit's highest possible score as 31 and lowest as 11 - a difference of 20."),
    ("Two ships meet mid-ocean,and then,one ship goes south and the other ship goes west,both travelling at constant speeds.Two hours later,they are 60 km apart.If the speed of one of the ships is 6km per hour more than the other one,then the speed,in km per hour,of the slower ship is", "18", "Two hours after meeting, the slower ship (speed v) has gone 2v km and the faster (v+6) has gone 2(v+6) km, perpendicular to each other, 60 km apart. Solving v²+(v+6)²=900 (from the Pythagorean relation) gives v = 18 km/h."),
    ("In an examination,there were 75 questions.3 marks were awarded for each correct answer,1 mark was deducted for each wrong answer and 1 mark was awarded for each unattempted question.Rayan scored a total of 97 marks in the examination.If the number of unattempted questions was\n\nhigher than the number of attempted questions,then the maximum number of correct answers that Rayan could have given in the examination is", "24", "With 75 questions scored +3/-1/+1 and both the total marks and the number of wrong answers constrained, maximizing the correct-answer count under these equations caps it at 24."),
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
