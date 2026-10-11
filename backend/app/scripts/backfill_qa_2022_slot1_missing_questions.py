"""Add the 7 CAT 2022 QA Slot 1 questions missing from the DB (15/22 loaded).
Found by diffing against pyq-source/2022/QUANT_SLOT1_CAT_2022.pdf (an
official digialm response sheet showing the correct option / possible
answer for every question). Every answer below was solved independently
and cross-checked against that key.

Run with:
    python -m app.scripts.backfill_qa_2022_slot1_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        question_type="TITA",
        question_text="Let A be the largest positive integer that divides all the numbers of the form 3^k+4^k+5^k, and B be the largest positive integer that divides all the numbers of the form 4^k+3(4^k)+4^(k+2), where k is any positive integer. Then (A+B) equals",
        correct_answer="82",
        explanation="3^k+4^k+5^k is always even (odd+even+odd), and gcd of the k=1,2 values (12,50) is 2, so A=2. The second form simplifies to 5·4^(k+1), whose values for k=1,2,... are all multiples of the k=1 value 80, so B=80. A+B=82.",
    ),
    dict(
        question_type="MCQ",
        question_text="All the vertices of a rectangle lie on a circle of radius R. If the perimeter of the rectangle is P, then the area of the rectangle is",
        options=["P²/16 − R²", "P²/8 − 2R²", "P²/2 − 2PR", "P²/8 − R²/2"],
        correct_answer="P²/8 − 2R²",
        explanation="The rectangle's diagonal equals the circle's diameter, so a²+b²=4R², while a+b=P/2. Then ab = [(a+b)²-(a²+b²)]/2 = [(P/2)²-4R²]/2 = P²/8 − 2R².",
    ),
    dict(
        question_type="MCQ",
        question_text="Let a, b, c be non-zero real numbers such that b² < 4ac, and f(x) = ax² + bx + c. If the set S consists of all integers m such that f(m) < 0, then the set S must necessarily be",
        options=["either the empty set or the set of all integers", "the set of all integers", "the set of all positive integers", "the empty set"],
        correct_answer="either the empty set or the set of all integers",
        explanation="b²<4ac means the quadratic has no real roots, so f keeps a constant sign everywhere - always positive if a>0 (giving S=∅) or always negative if a<0 (giving S=all integers).",
    ),
    dict(
        question_type="MCQ",
        question_text="Let a and b be natural numbers. If a² + ab + a = 14 and b² + ab + b = 28, then (2a + b) equals",
        options=["8", "9", "7", "10"],
        correct_answer="8",
        explanation="Factoring, a(a+b+1)=14 and b(a+b+1)=28, so b=2a. Substituting s=a+b+1=3a+1 into a·s=14 gives 3a²+a-14=0, whose positive root is a=2, so b=4 and 2a+b=8.",
    ),
    dict(
        question_type="MCQ",
        question_text="Let 0 ≤ a ≤ x ≤ 100 and f(x) = |x − a| + |x − 100| + |x − a − 50|. Then the maximum value of f(x) becomes 100 when a is equal to",
        options=["0", "25", "100", "50"],
        correct_answer="50",
        explanation="For a≤x≤100, f(x) = (100-a) + |x-a-50|, maximised over x in [a,100] at x=a (where |x-a-50|=50, the larger of the two endpoint distances). So the maximum is 150-a, which equals 100 when a=50.",
    ),
    dict(
        question_type="TITA",
        question_text="For any real number x, let [x] be the largest integer less than or equal to x. If the sum from n=1 to N of [1/5 + n/25] = 25 then N is",
        correct_answer="44",
        explanation="[1/5+n/25] = [(n+5)/25], which is 0 for n=1..19 and 1 for n=20..44. The running sum first reaches 25 (19 zeros plus 25 ones) exactly at N=44.",
    ),
    dict(
        question_type="MCQ",
        question_text="For any natural number n, suppose the sum of the first n terms of an arithmetic progression is (n + 2n²). If the nth term of the progression is divisible by 9, then the smallest possible value of n is",
        options=["8", "7", "4", "9"],
        correct_answer="7",
        explanation="The nth term is S(n)-S(n-1) = (n+2n²)-((n-1)+2(n-1)²) = 4n-1. Needing 4n≡1 (mod 9), and since 4·7=28≡1, the smallest n is 7.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        inserted = 0
        for row in ROWS:
            existing = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.section == "QA",
                    CatQuestion.source_year == 2022,
                    CatQuestion.source_slot == "slot1",
                    CatQuestion.question_text == row["question_text"],
                )
                .first()
            )
            if existing is not None:
                print(f"Already present as id={existing.id}, skipping: {row['question_text'][:50]!r}")
                continue

            q = CatQuestion(
                section="QA",
                question_type=row["question_type"],
                topic="Quantitative Aptitude",
                difficulty="hard",
                source="pyq",
                source_year=2022,
                source_slot="slot1",
                question_text=row["question_text"],
                options=row.get("options"),
                correct_answer=row["correct_answer"],
                explanation=row["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted id={q.id}: {row['question_text'][:50]!r}")
            inserted += 1
        db.commit()
        print(f"Inserted {inserted} CAT 2022 QA Slot 1 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
