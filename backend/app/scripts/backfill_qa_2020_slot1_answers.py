"""Backfill correct_answer/explanation for CAT 2020 QA Slot 1, matched
against already-loaded rows by (source_year, source_slot, section,
question_text). Answers come from the official solutions PDF (pdftotext
extraction, not re-typed); explanations are rewritten in plain language
from that source, not copied verbatim.

Q7, Q19, Q20 are skipped - their printed answer itself is corrupted by
the same embedded-math-as-image problem that does not render in text (a
non-numeric garble, not a real option), so no answer is asserted rather
than guessing.

Run with:
    python -m app.scripts.backfill_qa_2020_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("How many 3-digit numbers are there, for which the product of their digits is more than 2 but less than 7?", "21", "The digit product must be 3, 4, 5, or 6. Listing the digit combinations that give each of these products (and all their orderings as a 3-digit number) adds up to 21 numbers."),
    ("If f (5 + x) = f (5 − x) for every real x and f (x) = 0 has four distinct real roots, then the sum of the roots is", "20", "f(5+x) = f(5−x) means the graph is symmetric about x = 5, so the roots pair up as 5±a and 5±b. Adding all four roots cancels the ±a and ±b parts, leaving 4 × 5 = 20."),
    ("Veeru invested Rs 10000 at 5% simple annual interest, and exactly after two years, Joy invested Rs 8000 at 10% simple annual interest. How many years after Veeru’s investment, will their balances be equal?", "12", "After t years, Veeru's balance is 10000 + 500t. Joy starts 2 years later, so after the same t years his balance is 8000 + 800(t−2). Setting the two equal and solving gives t = 12."),
    ("A train traveled at one-third of its usual speed, reaching the destination 30 minutes late. On its return journey, it traveled at usual speed for 5 minutes but stopped for 4 minutes. The percentage increase in speed needed to reach on time is nearest to:", "67", "At one-third speed the trip took 30 extra minutes, which pins down the usual time as 15 minutes. On the return leg, after travelling 5 minutes at normal speed, catching up to reach on time needs roughly a 67% higher speed for the rest of the journey."),
    ("A straight road connects points A and B. Car 1 travels from A to B and Car 2 travels from B to A, both leaving at the same time. After meeting each other, they take 45 minutes and 20 minutes, respectively, to complete their journeys. If Car 1 travels at the speed of 60 km/hr, then the speed of Car 2, in km/hr, is", "90", "After the cars cross, the time each one still needs to finish is inversely proportional to its speed. Car 1 (going 60 km/hr) needs 45 more minutes and Car 2 needs 20 more minutes, so Car 2's speed is 60 × 45/20 = 90 km/hr."),
    ("Let A, B, and C be three positive integers such that the sum of A and the mean of B and C is 5. In addition, the sum of B and the mean of A and C is 7. Then the sum of A and B is", "6", "The two conditions give 2A + B + C = 10 and 2B + A + C = 14. Subtracting shows B = A + 4, and since A, B, C must be positive integers, the only valid fit is A = 1, B = 5, C = 3 - so A + B = 6."),
    ("The mean of all 4-digit even natural numbers of the form ’aabb’, where a > 0, is", "5544", "Every such number equals 1100a + 11b = 11(100a + b), with a from 1-9 and b an even digit 0-8. Averaging over all valid (a, b) pairs gives a mean of 5544."),
    ("The number of distinct real roots of the equation (x + 1/x)2 − 3(x + 1/x) + 2 = 0 equals:", "1", "Substituting y = x + 1/x turns this into y² − 3y + 2 = 0, i.e. y = 1 or y = 2. y = 1 gives no real x, but y = 2 gives a repeated root x = 1 - so there is exactly one distinct real root."),
    ("A person spent Rs 50000 to purchase a desktop computer and a laptop computer. He sold the desktop at 20", "20000", "Let x be the desktop's cost; the laptop then costs 50000 − x. Selling the desktop at a 20% markup and the laptop at a 10% markdown, with total revenue equal to a 2% overall gain on 50000, gives x = 20000."),
    ("Among 100 students, x1 have birthdays in January, x2 have birthdays in February, and so on. If x0 = max(x1 , x2 , . . . , x12 ), then the smallest possible value of x0 is", "9", "To keep the largest monthly count as small as possible, spread 100 students as evenly as possible across 12 months. That caps the maximum at ⌈100/12⌉ = 9."),
    ("Among 100 students, x1 have birthdays in January, x2 have birthdays in February, and so on. If x0 = max(x1 , x2 , . . . , x12 ), then the smallest possible value of x0 is", "9", "Same setup as the previous question - spreading 100 students across 12 months as evenly as possible still caps the largest group at 9."),
    ("How many distinct positive integer-valued solutions exist to the equation (x2 − 7x + 11)2 − 13x + 42 = 1?", "6", "Rearranging gives (x² − 7x + 11)² = 13x − 41. Testing positive integer values of x for which both sides match as perfect squares turns up 6 valid solutions."),
    ("The area of the region satisfying the inequalities |x| − y ≤ 1, y ≥ 0, and y ≤ 1 is", "3", "The condition |x| − y ≤ 1 rearranges to y ≥ |x| − 1, so the region sits between y = |x| − 1 and y = 1, with y ≥ 0. Working out this bounded area over x from −1 to 1 gives 3 square units."),
    ("A solid right circular cone of height 27 cm is cut into 2 pieces along a plane parallel to its base at a height of 18 cm from the base. If the difference in the volume of the two pieces is 225 cc, the volume, in cc, of the original cone is", "243", "Cutting the cone at 18 cm creates a smaller similar cone (scaled by 18/27 = 2/3) on top and a frustum below. Using the given volume difference between the original cone and the smaller cone to solve for the base radius gives the original cone's volume as 243 cc."),
    ("A circle is inscribed in a rhombus with diagonals 12 cm and 16 cm. The ratio of the area of the circle to the area of the rhombus is", "6π", "The rhombus has area ½ × 12 × 16 = 96 cm² and side 10 cm (by Pythagoras on the half-diagonals), giving perimeter 40 cm. The inscribed circle's radius works out to 2.4 cm, so the circle's area is 5.76π cm² and the ratio to 96 simplifies to 6π/25."),
    ("Leaving home at the same time, Amal reaches office at 10:15 am if he travels at 8 kmph, and at 9:40 am if he travels at 15 kmph. Leaving home at 9:10 am, at what speed, in kmph, must he travel so as to reach office exactly at 10:00 am?", "12", "The 35-minute gap between the two arrival times at speeds 8 and 15 kmph pins the distance at 120 km. Leaving at 9:10 to arrive by 10:00 leaves 50 minutes, which requires a speed of 12 kmph."),
    ("If a, b, and c are positive integers such that ab = 432, bc = 96 and c < 9, then the smallest possible value of a + b + c is", "46", "From ab = 432 and bc = 96, a works out to 4.5c, so c must be even. Checking c = 2, 4, 6 (all under 9), the smallest total a + b + c = 46 happens at c = 6, giving a = 27, b = 16."),
    ("An alloy is prepared by mixing metals A, B, C in the proportion 3 : 4 : 7 by volume. Weights of the same volume of metals A, B, C are in the ratio 5 : 2 : 6. In 130 kg of the alloy, the weight, in kg, of the metal C is", "84", "By volume the metals are in ratio 3:4:7 and by weight 5:2:6; converting the volume ratio into actual weights and scaling so the total comes to 130 kg gives metal C's weight as 84 kg."),
    ("In 130 kg of the alloy, the weight, in kg, of the metal C is", "84", "Converting the 3:4:7 volume ratio into weights using the given per-unit-volume weight ratio 5:2:6, then scaling so the total alloy weighs 130 kg, gives metal C's share as 84 kg."),
    ("A solution, of volume 40 litres, has dye and water in the proportion 2 : 3. Water is added to the solution to change this proportion to 2 : 5. If one-fourth of this diluted solution is taken out, how many litres of dye must be added to the remaining solution to bring the proportion back to 2 : 3?", "8", "The solution starts with 16 L dye and 24 L water. After removing a quarter of the mixture and topping up with dye to restore the original 2:3 ratio in a smaller batch, the amount of dye added back out works out to 8 litres."),
    ("The number of real-valued solutions of the equation 2x + 22x = 2 − (x − 2)2 is", "0", "The left side grows without bound as x increases (exponential terms), while the right side is a downward parabola capped at 2. The two sides never meet, so there are no real solutions."),
    ("In a group of people, 28% of the members are young while the rest are old. If 65% of the members are literates, and 25% of the literates are young, then the percentage of old people among the illiterates is nearest to", "66", "Out of 100 people: 65 are literate, of which 25% (16.25) are young, leaving 48.75 literate and old. The illiterate group is the remaining 35 people; working out how many of those are old gives roughly 66% of illiterates being old."),
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
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} QA {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
