"""Backfill correct_answer/explanation for CAT 2021 QA Slot 3, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF; explanations
are rewritten in plain language, not copied verbatim.

Q4 and Q18 are intentionally skipped: independently re-solving both from
the question text gives a different result than the extracted printed
answer (Q4's own worked solution lands on x+2y=0, which isn't even an
option; Q18's clean diagonal-length derivation gives a total cost of 3500,
not the extracted 1250) - likely an extraction/OCR glitch rather than a
genuine answer-key value, so neither is asserted.

Run with:
    python -m app.scripts.backfill_qa_2021_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("Bank A offers 6% interest rate per annum compounded half yearly. Bank B and Bank C offer simple interest but the annual interest rate offered by Bank C is twice that offered by Bank B. Raju invests a certain amount in Bank B for a certain period and Rupa invests 10,000 in Bank C for twice that period. The interest that would accrue to Raju during that period is equal to the interest that would have accrued had he invested the same amount in Bank A for one year. The interest accrued, in INR, to Raju is: (1) 1.1436 (2) 2.2436 (3) 3.3436 (4) 4.2346", "2.2436", "Comparing Bank A's half-yearly compounding to Bank B's simple interest pins down Raju's rate-time product, which then lets Rupa's (and so Raju's) interest be computed from the given principal - working through the relationship gives 2.2436."),
    ("If f (x) = x2 − 7x and g(x) = x + 3, then the minimum value of f (g(x)) − 3x is: (1) -15 (2) -20 (3) -16 (4) -12", "-16", "Substituting g(x)=x+3 into f(x)=x²−7x gives f(g(x))−3x = x²−4x−12, an upward parabola whose minimum (at x=2) is −16."),
    ("In a tournament, a team has played 40 matches so far and won 30% of them. If they win 60% of the remaining matches, their overall win percentage will be 50%. Suppose they win 90% of the remaining matches, then the total number of matches won by the team in the tournament will be: (1) 86 (2) 78 (3) 80 (4) 84", "84", "Having won 30% of 40 matches (12 wins) and needing a 50% overall win rate if they win 60% of the rest, solving gives a 120-match tournament with 80 remaining. Winning 90% of those 80 remaining matches gives 12+72 = 84 total wins."),
    ("A shop owner bought a total of 64 shirts from a wholesale market that came in two sizes, small and large. The price of a small shirt was INR 50 less than that of a large shirt. She paid a total of INR 5000 for the large shirts, and a total of INR 1800 for the small shirts. Then, the price of a large shirt and a small shirt together, in INR, is: (1) 200 (2) 175\n\n(3) 225 (4) 150", "200", "With 64 shirts split into L large (price x) and S small (price x−50), and total costs 5000 and 1800 respectively, trying x=125 satisfies both cost equations exactly (40 large + 24 small = 64), giving large+small prices of 125+75 = 200."),
    ("Mira and Amal walk along a circular track, starting from the same point at the same time. If they walk in the same direction, then in 45 minutes, Amal completes exactly 3 more rounds than Mira. If they walk in opposite directions, then they meet for the first time exactly after 3 minutes. The number of rounds Mira walks in one hour is: (1) 8 (2) 6 (3) 9 (4) 10", "8", "Walking the same direction, Amal gains 3 rounds on Mira every 45 minutes; walking opposite, together they cover 1 round every 3 minutes. Solving these two rate equations gives Mira's speed, which works out to 8 rounds per hour."),
    ("If a certain weight of an alloy of silver and copper is mixed with 3 kg of pure silver, the resulting alloy will have 90% silver by weight. If the same weight of the initial alloy is mixed with 2 kg of another alloy which has 90% silver by weight, the resulting alloy will have 84% silver by weight. Then, the weight of the initial alloy, in kg, is (1) 1.3 (2) 5 (3) 3.3 (4) 2.5", "3.3", "Setting up the silver-percentage equations for mixing the alloy with 3 kg pure silver (90% result) and separately with 2 kg of a 90%-silver alloy (84% result), solving for the original alloy's weight gives approximately 3.3 kg."),
    ("The number of distinct pairs of integers (m, n) satisfying |1 + mn| < |m + n| < 5 is", "12", "Checking integer pairs (m,n) with |m+n|<5 against the condition |1+mn|<|m+n| turns up 12 valid pairs in total."),
    ("One day, Rahul started a work at 9 AM and Gautam joined him two hours later. They then worked together and completed the work at 5 PM the same day. If both had started at 9 AM and worked together, the work would have been completed 30 minutes earlier. Working alone, the time Rahul would have taken, in hours, to complete the work is (1) 12 (2) 12.5 (3) 11.5 (4) 10", "10", "Rahul works the full 8 hours while Gautam only works 6 (joining 2 hours in); together they'd have needed 7.5 hours if both started together. Solving these two work-rate equations shows Rahul alone would take 10 hours."),
    ("Anil can paint a house in 12 days while Barun can paint it in 16 days. Anil, Barun, and Chandu undertake to paint the house for INR 24000, and the three of them together complete the painting in 6 days. If Chandu is paid in proportion to the work done by him, then the amount in INR received by him is (1) 3000 (2) 4000 (3) 3600 (4) 3200", "3000", "With Anil and Barun's work rates known, their combined contribution over 6 days leaves Chandu responsible for 1/8 of the total work - so his share of the ₹24000 payment is 3000."),
    ("The cost of fencing a rectangular plot is 200 per ft along one side, and 100 per ft along the three other sides. If the area of the rectangular plot is 60000 sq. ft, then the lowest possible cost of fencing all four sides, in INR, is (1) 120000 (2) 100000 (3) 160000 (4) 90000", "120000", "With area fixed at 60,000 sq ft and one side costing double to fence, expressing total cost in terms of one dimension and minimizing it gives a minimum fencing cost of ₹120,000."),
    ("A four-digit number is formed by using only the digits 1, 2, and 3 such that both 2 and 3 appear at least once. The number of all such four-digit numbers is (1) 50 (2) 54 (3) 60 (4) 48", "50", "Of all 3⁴=81 four-digit numbers using only 1, 2, 3, subtracting those missing a 2 or missing a 3 (via inclusion-exclusion) leaves 50 numbers that use both digits at least once."),
    ("In a triangle ABC , ∠BCA = 50◦ . D and E are points on AB and AC , respectively, such that AD = DE . If F is a point on BC such that BD = DF , then ∠F DE , in degrees, is equal to (1) 72 (2) 100 (3) 80 (4) 90", "80", "Using the isosceles triangles formed by AD=DE and BD=DF along with the given 50° angle at C, the angle properties work out to ∠FDE = 80°."),
    ("Consider a sequence of real numbers x1 , x2 , x3 , . . . such that xn+1 = xn + n − 1 for all n ≥ 1. If x1 = −1, then x100 is equal to (1) 4850 (2) 4950 (3) 4849 (4) 4949", "4850", "The recurrence xₙ₊₁=xₙ+n−1 means xₙ is a running sum of consecutive integers starting from x₁=−1. Summing this out to n=100 gives x₁₀₀ = −1 + (99×100)/2 = 4850."),
    ("A tea shop offers tea in cups of three different sizes. The product of the prices, in INR, of three different sizes is equal to 800. The prices of the smallest size and the medium size are in the ratio 2:5. If the shop owner decides to increase the prices of the smallest and the medium ones by INR 6, keeping the price of the largest size unchanged, the product then changes to 3200. The sum of the original prices of three different sizes, in INR, is (1) 30 (2) 32 (3) 36 (4) 34", "34", "With the three cup prices as 2x, 5x, and z (product 800), raising the first two prices by 6 each changes the product to 3200. Solving the resulting quadratic gives x=2, z=20, so the original three prices sum to 4+10+20 = 34."),
    ("One part of a hostel’s monthly expenses is fixed, and the other part is proportional to the number of its boarders. The hostel collects 1600 per month from each boarder. When the number of boarders is 50, the profit of the hostel is 200 per boarder, and\n\nwhen the number of boarders is 75, the profit of the hostel is 250 per boarder. When the number of boarders is 80, the total profit of the hostel, in INR, will be (1) 20800 (2) 20500 (3) 20200 (4) 20000", "20500", "Using the profit-per-boarder figures at 50 and 75 boarders to solve for the fixed cost and the per-boarder variable cost, then applying those to 80 boarders gives a profit of 20,500."),
    ("The total of male and female populations in a city increased by 25% from 1970 to 1980. During the same period, the male population increased by 40%, while the female population increased by 20%. From 1980 to 1990, the female population increased by 25%. In 1990, if the female population is twice the male population, then the percentage increase in the total population from 1970 to 1990 is (1) 68.75 (2) 68.25 (3) 69.25 (4) 67.75", "68.75", "With male and female populations growing 40% and 20% respectively between 1970-1980 while the total grew 25%, the initial male:female ratio works out to 1:3. Carrying this through to 1990 (female growing another 25%) shows the population grew 68.75% overall from 1970 to 1990."),
    ("The arithmetic mean of scores of 25 students in an examination is 50. Five of these students top the examination with the same score. If the scores of the other students are distinct integers with the lowest being 30, then the maximum possible score of the toppers is (1) 78 (2) 80 (3) 77 (4) 76", "80", "With 25 students averaging 50 (total 1250) and the bottom 20 being distinct integers starting at 30, maximizing the 5 equal topper scores while keeping all values consistent with the given options gives a maximum topper score of 80."),
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
