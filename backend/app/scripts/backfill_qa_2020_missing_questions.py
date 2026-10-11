"""Add the 9 CAT 2020 QA questions missing from slot1 (1), slot2 (3) and
slot3 (5) - each slot was short of the expected 26 questions. Found by
diffing the DB against the source PDFs (pyq-source/2020/QUANT_SLOT*_CAT_2020.pdf,
which carry the official answer key inline as "N: answer") and solved
independently; every answer below was cross-checked against that inline key
(and, for slot3 Q11, against a web search after the OCR "14a=36b=84c" turned
out to actually be "14^a=36^b=84^c" - exponents, not coefficients).

Run with:
    python -m app.scripts.backfill_qa_2020_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

ROWS = [
    dict(
        source_slot="slot1",
        question_type="TITA",
        question_text="If log₄5 = (log₄y)(log₆√5), then y equals",
        correct_answer="36",
        explanation="log₆√5 = (1/2)log₆5. So log₄(y) = 2·log₄5/log₆5 = 2·log₄5·(log5/log6)/(log5/log4)... using change of base, log₄(y) = 2log₄6 = log₄36, so y=36.",
    ),
    dict(
        source_slot="slot2",
        question_type="MCQ",
        question_text="The value of log_b(b/a) + log_a(a/b), for 1 < a ≤ b, cannot be equal to",
        options=["-0.5", "1", "0", "-1"],
        correct_answer="1",
        explanation="Let t=log_a(b)≥1. The expression simplifies to (1-1/t)+(1-t) = 2-t-1/t, which is 0 at t=1 and strictly decreasing for t>1, so it only ever takes values in (-∞, 0]. It can never equal a positive value like 1.",
    ),
    dict(
        source_slot="slot2",
        question_type="TITA",
        question_text="If x and y are positive real numbers satisfying x + y = 102, then the minimum possible value of 2601(1 + 1/x)(1 + 1/y) is",
        correct_answer="2704",
        explanation="(1+1/x)(1+1/y) = 1 + (x+y)/(xy) + 1/(xy) = 1 + 103/(xy). Since x+y=102 is fixed, xy is maximised (at x=y=51, giving xy=2601) when the bracket - and hence the whole expression - is minimised: 2601·(1+103/2601) = 2601+103 = 2704.",
    ),
    dict(
        source_slot="slot2",
        question_type="TITA",
        question_text="For real x, the maximum possible value of x/√(1+x⁴) is",
        correct_answer="1/√2",
        explanation="Squaring, x²/(1+x⁴) = u/(1+u²) where u=x²≥0, which is maximised at u=1 with value 1/2. So the maximum of x/√(1+x⁴) is √(1/2) = 1/√2, attained at x=1.",
    ),
    dict(
        source_slot="slot3",
        question_type="MCQ",
        question_text="Let log_a(30) = A, log_a(3/5) = B, and log₂(a) = 1/3, then log₃(a) equals",
        options=["2/(A+B-3)", "(A+B-3)/2", "[(A+B)/2] - 3", "[2/(A+B)] - 3"],
        correct_answer="2/(A+B-3)",
        explanation="log₂(a)=1/3 means log_a(2)=3. Writing p=log_a3, q=log_a5: A=log_a30=log_a2+p+q=3+p+q, and B=log_a(3/5)=p-q. Adding: A+B=3+2p, so p=(A+B-3)/2, and log₃(a)=1/p=2/(A+B-3).",
    ),
    dict(
        source_slot="slot3",
        question_type="TITA",
        question_text="(2×4×8×16)/[(log₂4)²(log₄8)³(log₈16)⁴] equals to:",
        correct_answer="24",
        explanation="2×4×8×16=2^10=1024. log₂4=2, log₄8=3/2, log₈16=4/3, so the denominator is 2²·(3/2)³·(4/3)⁴ = 4·(27/8)·(256/81) = 128/3. 1024÷(128/3)=24.",
    ),
    dict(
        source_slot="slot3",
        question_type="TITA",
        question_text="If a, b, c are non-zero and 14^a = 36^b = 84^c, then 6b(1/c - 1/a) equals to:",
        correct_answer="3",
        explanation="Let k=14^a=36^b=84^c. Then 1/a=log_k(14), b=log₃₆(k), 1/c=log_k(84). 1/c-1/a=log_k(84/14)=log_k(6). So 6b(1/c-1/a)=6·log_k(6)/log₃₆(k)... equivalently 6·ln6/ln36 = 6·ln6/(2ln6) = 3.",
    ),
    dict(
        source_slot="slot3",
        question_type="MCQ",
        question_text="Let m and n be natural numbers such that n is even and 0.2 < m/20, n/m, n/11 < 0.5. Then m - 2n equals",
        options=["4", "2", "1", "3"],
        correct_answer="1",
        explanation="0.2<m/20<0.5 gives m∈{5,...,9}. 0.2<n/11<0.5 gives n∈{3,4,5}, and n even forces n=4. 0.2<n/m<0.5 with n=4 needs 8<m<20, which combined with m∈{5,...,9} forces m=9. So m-2n=9-8=1.",
    ),
    dict(
        source_slot="slot3",
        question_type="MCQ",
        question_text="Let m and n be positive integers. If x² + mx + 2n = 0 and x² + 2nx + m = 0 have real roots, then the smallest possible value of m + n is",
        options=["8", "6", "5", "7"],
        correct_answer="6",
        explanation="Real roots require m²≥8n (first equation) and n²≥m (second). Testing n=1 gives no valid m; n=2 requires m≥4 and m≤4, so m=4 works, giving m+n=6. n=3 already needs m≥5, giving a larger sum. So the minimum is 6.",
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
                    CatQuestion.source_year == 2020,
                    CatQuestion.source_slot == row["source_slot"],
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
                source_year=2020,
                source_slot=row["source_slot"],
                question_text=row["question_text"],
                options=row.get("options"),
                correct_answer=row["correct_answer"],
                explanation=row["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted id={q.id} ({row['source_slot']}): {row['question_text'][:50]!r}")
            inserted += 1
        db.commit()
        print(f"Inserted {inserted} CAT 2020 QA questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
