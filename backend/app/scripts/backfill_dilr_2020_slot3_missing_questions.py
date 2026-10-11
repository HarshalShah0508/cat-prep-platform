"""Add the 7 CAT 2020 DILR Slot 3 questions missing from the DB: 1 question
from the existing 16-patients/8-vials blood-testing set, and an entire
6-question set ("farmer's 205 trees across 12 plots") that was never loaded
at all. The local source PDF for this slot turned out to be a mislabeled
duplicate of Slot 2's paper, so this was reconstructed via web search
cross-checks against multiple independent sources (cracku, bodheeprep),
with the vial-testing answer independently re-verified.

Run with:
    python -m app.scripts.backfill_dilr_2020_slot3_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

VIAL_PASSAGE = (
    "Sixteen patients in a hospital must undergo a blood test for a disease. It is known that exactly "
    "one of them has the disease. The hospital has only eight testing kits and has decided to pool blood "
    "samples of patients into eight vials for the tests. The patients are numbered 1 through 16, and the "
    "vials are labelled A, B, C, D, E, F, G, and H. The following table shows the vials into which each "
    "patient's blood sample is distributed.\n\n"
    "Vial A: 9,10,11,12,13,14,15,16. Vial B: 1,2,3,4,5,6,7,8. Vial C: 5,6,7,8,13,14,15,16. "
    "Vial D: 1,2,3,4,9,10,11,12. Vial E: 3,4,7,8,11,12,15,16. Vial F: 1,2,5,6,9,10,13,14. "
    "Vial G: 2,4,6,8,10,12,14,16. Vial H: 1,3,5,7,9,11,13,15.\n\n"
    "- If a patient has the disease, then each vial containing his/her blood sample will test positive.\n"
    "- If a vial tests positive, then one of the patients whose blood samples were mixed in the vial has "
    "the disease.\n"
    "- If a vial tests negative, then none of the patients whose blood samples were mixed in the vial has "
    "the disease."
)

TREES_PASSAGE = (
    "A farmer had a rectangular land containing 205 trees. He distributed that land among his four "
    "daughters - Abha, Bina, Chitra and Dipti - by dividing the land into twelve plots arranged along "
    "three rows (X, Y, Z) and four columns (1, 2, 3, 4). The plots in rows X, Y, and Z contained Mango, "
    "Teak, and Pine trees, respectively. Each plot had a non-zero multiple of 3 or 4 trees, and no two "
    "plots had the same number of trees.\n\n"
    "The following additional facts are known:\n"
    "1. Abha got 20 trees more than Chitra but 6 trees less than Dipti.\n"
    "2. The largest number of trees in a plot was 32, but it was not with Abha.\n"
    "3. The number of teak trees in Column 3 was double of that in Column 2 but was half of that in "
    "Column 4.\n"
    "4. Both Abha and Bina got a higher number of plots than Dipti.\n"
    "5. Only Bina, Chitra and Dipti got corner plots.\n"
    "6. Dipti got two adjoining plots in the same row.\n"
    "7. Bina was the only one who got a plot in each row and each column.\n"
    "8. Chitra and Dipti did not get plots which were adjacent to each other.\n"
    "9. The number of mango trees was double the number of teak trees."
)

VIAL_QUESTION = dict(
    group_id="cat2020_dilr_slot3_set5",
    question_type="MCQ",
    passage_text=VIAL_PASSAGE,
    question_text="Which of the following combinations of test results is NOT possible?",
    options=[
        "Vials A and E positive, vials C and D negative",
        "Vial B positive, vials C, F and H negative",
        "Vials A and G positive, vials D and E negative",
        "Vials B and D positive, vials F and H negative",
    ],
    correct_answer="Vials A and E positive, vials C and D negative",
    explanation="Vials C and D together cover all 16 patients (C={5-8,13-16}, D={1-4,9-12}), so both testing negative would mean no patient could have the disease - contradicting the given fact that exactly one patient is sick. This combination is therefore impossible regardless of A and E.",
)

TREE_QUESTIONS = [
    dict(
        question_text="How many mango trees were there in total?",
        options=["84", "98", "49", "126"],
        correct_answer="98",
        explanation="Row X (Mango) trees sum to 98 once the full grid is solved from the nine clues - consistent with mango trees being double the teak-tree total (clue 9).",
    ),
    dict(
        question_text="Which of the following is the correct sequence of trees received by Abha, Bina, Chitra and Dipti, respectively?",
        options=["50, 69, 30, 56", "54, 57, 34, 60", "44, 87, 24, 50", "60, 39, 40, 66"],
        correct_answer="50, 69, 30, 56",
        explanation="Solving the full plot-ownership grid against all nine clues (including Abha=Chitra+20=Dipti-6) gives Abha=50, Bina=69, Chitra=30, Dipti=56 trees - and indeed 50=30+20 and 50=56-6, matching clue 1.",
    ),
    dict(
        question_text="How many pine trees did Chitra receive?",
        options=["21", "30", "18", "15"],
        correct_answer="18",
        explanation="From the solved grid, Chitra's plots in row Z (Pine) total 18 trees.",
    ),
    dict(
        question_text="Who got the plot with the smallest number of trees, and how many trees did that plot have?",
        options=["Dipti, 6", "Bina, 4", "Abha, 4", "Bina, 3"],
        correct_answer="Bina, 3",
        explanation="Among all 12 distinct plot values (non-zero multiples of 3 or 4), the smallest is 3 trees, held by Bina.",
    ),
    dict(
        question_text="Which of the following statements is NOT true?",
        options=["Chitra got 12 mango trees", "Bina got 32 pine trees", "Abha got 41 teak trees", "Dipti got 56 mango trees"],
        correct_answer="Bina got 32 pine trees",
        explanation="In the solved grid, Bina's pine-tree total does not equal 32 (the single largest plot of 32 trees belongs to a different owner, per clue 2 which only rules out Abha) - making this the false statement.",
    ),
    dict(
        question_text="Which column had the highest number of trees?",
        options=["4", "3", "Cannot be determined", "2"],
        correct_answer="4",
        explanation="The four columns total 36, 52, 49, and 68 trees respectively (summing to the full 205), so Column 4 has the most.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        inserted = 0

        existing = (
            db.query(CatQuestion)
            .filter(
                CatQuestion.section == "DILR",
                CatQuestion.source_year == 2020,
                CatQuestion.source_slot == "slot3",
                CatQuestion.question_text == VIAL_QUESTION["question_text"],
            )
            .first()
        )
        if existing is None:
            q = CatQuestion(
                section="DILR",
                question_type=VIAL_QUESTION["question_type"],
                topic="Logical Reasoning",
                difficulty="hard",
                source="pyq",
                source_year=2020,
                source_slot="slot3",
                group_id=VIAL_QUESTION["group_id"],
                passage_text=VIAL_QUESTION["passage_text"],
                question_text=VIAL_QUESTION["question_text"],
                options=VIAL_QUESTION["options"],
                correct_answer=VIAL_QUESTION["correct_answer"],
                explanation=VIAL_QUESTION["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted vial question id={q.id}")
            inserted += 1
        else:
            print(f"Vial question already present as id={existing.id}, skipping.")

        for row in TREE_QUESTIONS:
            existing = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.section == "DILR",
                    CatQuestion.source_year == 2020,
                    CatQuestion.source_slot == "slot3",
                    CatQuestion.question_text == row["question_text"],
                )
                .first()
            )
            if existing is not None:
                print(f"Already present as id={existing.id}, skipping: {row['question_text'][:50]!r}")
                continue
            q = CatQuestion(
                section="DILR",
                question_type="MCQ",
                topic="Logical Reasoning",
                difficulty="hard",
                source="pyq",
                source_year=2020,
                source_slot="slot3",
                group_id="cat2020_dilr_slot3_set1",
                passage_text=TREES_PASSAGE,
                question_text=row["question_text"],
                options=row["options"],
                correct_answer=row["correct_answer"],
                explanation=row["explanation"],
            )
            db.add(q)
            db.flush()
            print(f"Inserted id={q.id}: {row['question_text'][:50]!r}")
            inserted += 1

        db.commit()
        print(f"Inserted {inserted} CAT 2020 DILR Slot 3 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
