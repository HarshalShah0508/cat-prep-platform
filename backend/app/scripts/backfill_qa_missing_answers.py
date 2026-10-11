"""Backfill correct_answer + explanation for the 11 QA rows that were loaded
with both fields null (ids 781, 793, 794, 801, 266, 285, 291, 314, 177, 180,
196). Several of these also had corrupted question_text/options from the
original OCR/scrape - math-heavy PDFs (2020 slot1/slot2 scans, a 2024 slot2
listing with completely fabricated numbers) lost or mangled exponents,
radicals and option text. Those are repaired here too, cross-checked against
the raw source PDFs (pyq-source/2020, 2024, 2025) and, where the local scrape
itself was wrong (266, 285), the official CAT answer-key / response-sheet
sources found via web search.

Run with:
    python -m app.scripts.backfill_qa_missing_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    781: {
        "question_text": "If x = (4096)^(7+4√3), then which of the following equals 64?",
        "options": [
            "(x^(7/2))/(x^(4/√3))",
            "(x^7)/(x^(4√3))",
            "(x^(7/2))/(x^(2√3))",
            "(x^7)/(x^(2√3))",
        ],
        "correct_answer": "(x^(7/2))/(x^(2√3))",
        "explanation": "4096=2^12, so x=2^(12(7+4√3))=2^(84+48√3). For x^(7/2)/x^(2√3)=x^(7/2-2√3), the exponent (7/2-2√3)(84+48√3) expands to 294+168√3-168√3-288=6, giving 2^6=64. Matches the source's official key (Q7: C).",
    },
    793: {
        "question_text": "If y is a negative number such that 2^(y²·log₃5) = 5^(log₂3), then y equals",
        "options": ["log2(1/3)", "log2(1/5)", "-log2(1/3)", "-log2(1/5)"],
        "correct_answer": "log2(1/3)",
        "explanation": "Taking log base 2 of both sides: y²·log₃5 = log₂3·log₂5. Using log₃5 = log₂5/log₂3, this reduces to y² = (log₂3)², so y = ±log₂3. Since y is negative, y = -log₂3 = log₂(1/3). Matches the source's official key (Q19: A).",
    },
    794: {
        "question_type": "TITA",
        "options": None,
        "correct_answer": "3√π(5 + 12/π)",
        "explanation": "The circle's diameter equals the rectangle's shorter side W, so area = πW²/4. Unpainted = (2/3)·painted gives 135 = (5/3)(πW²/4), so W² = 324/π, W = 18/√π. Length L = 135/W = (15/2)√π. Perimeter = 2(L+W) = 15√π + 36/√π = 3√π(5 + 12/π). Matches the source's official key (Q20).",
    },
    801: {
        "question_type": "TITA",
        "options": None,
        "correct_answer": "s²/√3",
        "explanation": "By Viviani's theorem, the sum of perpendicular distances from any interior point of an equilateral triangle to its three sides equals the triangle's altitude h, so h = s. Side a = 2h/√3 = 2s/√3, and area = (√3/4)a² = (√3/4)(4s²/3) = s²/√3. Matches the source's official key (Q2).",
    },
    266: {
        "question_text": "The sum of all real values of k for which (1/8)^k × (1/32768)^(1/3) = 1/8 × (1/32768)^(1/k) is",
        "correct_answer": "-2/3",
        "explanation": "32768=8^5, so with base 1/8 the equation becomes k + 5/3 = 1 + 5/k. Multiplying through by k and rearranging gives 3k²+2k-15=0. The sum of roots is -2/3 (by -b/a), and the discriminant is positive so both roots are real.",
    },
    285: {
        "question_text": "A bus starts at 9 am and follows a fixed route every day. One day, it traveled at a constant speed of 60 km per hour and reached its destination 3.5 hours later than its scheduled arrival time. Next day, it traveled two-thirds of its route in one-third of its total scheduled travel time, and the remaining part of the route at 40 km per hour to reach just on time. The scheduled arrival time of the bus is",
        "options": ["7:30 pm", "7:00 pm", "10:30 pm", "9:00 pm"],
        "correct_answer": "7:30 pm",
        "explanation": "Let T be the scheduled travel time and D the distance. Day 1: D/60 = T+3.5. Day 2: T/3 + (D/3)/40 = T, so D = 80T. Combining: 80T = 60T+210, giving T=10.5 hours. Scheduled arrival = 9 am + 10.5 h = 7:30 pm.",
    },
    291: {
        "question_text": "The sum of the infinite series (1/5)(1/5 − 1/7) + (1/5)²((1/5)² − (1/7)²) + (1/5)³((1/5)³ − (1/7)³) + … is equal to",
        "correct_answer": "5/408",
        "explanation": "The nth term is (1/5)^n[(1/5)^n-(1/7)^n] = (1/25)^n - (1/35)^n. Summing each geometric series separately: Σ(1/25)^n = 1/24 and Σ(1/35)^n = 1/34. The total is 1/24 - 1/34 = 10/816 = 5/408.",
    },
    314: {
        "correct_answer": "2 log10 2",
        "explanation": "Let t=10^x. The equation t+4/t=81/2 becomes 2t²-81t+8=0. The product of roots is 8/2=4, so 10^x1 · 10^x2 = 4, giving x1+x2 = log10(4) = 2 log10 2. The discriminant (6497) is positive and both roots are positive, so both are valid.",
    },
    177: {
        "options": ["1", "2", "0", "infinite"],
        "correct_answer": "0",
        "explanation": "Since base 1/4 < 1, log(1/4)(n²-7n+11) > 0 requires 0 < n²-7n+11 < 1. The upper bound n²-7n+11<1 simplifies to (n-2)(n-5)<0, i.e. 2<n<5, so n could only be 3 or 4 - but both give n²-7n+11=-1, which fails the n²-7n+11>0 requirement. No integer satisfies both conditions.",
    },
    180: {
        "correct_answer": "20(3 + √14)",
        "explanation": "Triangle PQC is isosceles (CP=CQ=radius) with ∠PQC=45°, so ∠QPC=45° and the central angle PCQ=90°. Distance from C to PQ = r·cos45° = 6, and half-chord = r·sin45° = 6, so PQ=12. With the distance ratio 3:2, SR is at distance 4, giving half-chord √(72-16)=2√14, so SR=4√14. The chords lie on opposite sides of the diameter, so the trapezoid's height is 6+4=10. Area = (1/2)(12+4√14)(10) = 20(3+√14).",
    },
    196: {
        "question_text": "If log₆₄(x²) + log₈(√y) + 3·log₅₁₂(√y · z) = 4, where x, y and z are positive real numbers, then the minimum possible value of (x + y + z) is",
        "correct_answer": "48",
        "explanation": "Converting all terms to base 2: log₂x/3 + log₂y/6 + [log₂y/6 + log₂z/3] = 4 simplifies to (log₂x+log₂y+log₂z)/3 = 4, so xyz = 2^12 = 4096. By AM-GM, x+y+z is minimized when x=y=z=4096^(1/3)=16, giving a minimum sum of 48.",
    },
}


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, fix in FIXES.items():
            row = db.query(CatQuestion).filter(CatQuestion.id == question_id).first()
            if row is None:
                print(f"NO MATCH: id={question_id}")
                continue
            if "question_text" in fix:
                row.question_text = fix["question_text"]
            if "question_type" in fix:
                row.question_type = fix["question_type"]
            if "options" in fix:
                row.options = fix["options"]
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} QA answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
