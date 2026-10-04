"""Seed CAT 2023 DILR Slot 3 questions - generated from the official
solutions PDF via pdftotext + pyq_dilr_parser.py (automated text-layer
extraction, not LLM transcription).

This fills a genuine gap left by seed_cat_pyq_2023_dilr.py, whose own
docstring says Slots 2 and 3 were "written incrementally... checkpointed
after each slot while under extraction" - Slot 3 was simply never
finished (not a deliberate chart-dependency skip, unlike most of this
year/section's other gaps).

Set 2 (six police stations connected by streets "as shown below") is
chart/diagram-dependent - the connecting topology is never given in text,
so it's skipped here, not fabricated.

`correct_answer`/`explanation` are intentionally left blank for now - the
answer key is loaded separately once transcribed from the solutions PDFs.

Run with:
    python -m app.scripts.seed_cat_pyq_2023_dilr_slot3
"""

from app.database.database import Base, SessionLocal, engine
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2023
SOURCE_SLOT = "slot3"


def q(group_id, qtype, text, options=None, passage=None):
    return {
        "section": "DILR",
        "question_type": qtype,
        "topic": "Data Interpretation & Logical Reasoning",
        "difficulty": "hard",
        "source": "pyq",
        "source_year": SOURCE_YEAR,
        "source_slot": SOURCE_SLOT,
        "group_id": group_id,
        "passage_text": passage,
        "question_text": text,
        "options": options,
    }


_REG_PASSAGE = (
    "In a coaching class, some students register online, and some others register offline. "
    "No student registers both online and offline; hence the total registration number is the "
    "sum of online and offline registrations. The following facts and table pertain to these "
    "registration numbers for the five months - January to May of 2023. The table shows the "
    "minimum, maximum, median registration numbers of these five months, separately for "
    "online, offline and total number of registrations. The following additional facts are "
    "known. 1. In every month, both online and offline registration numbers were multiples of "
    "10. 2. In January, the number of offline registrations was twice that of online "
    "registrations. 3. In April, the number of online registrations was twice that of offline "
    "registrations. 4. The number of online registrations in March was the same as the number "
    "of offline registrations in February. 5. The number of online registrations was the "
    "largest in May.\n\n"
    "Minimum Maximum Median\n"
    "Online 40 100 80\n"
    "Offline 30 80 50\n"
    "Total 110 130 120"
)

_SCORES_PASSAGE = (
    "There are only three female students - Amala, Koli and Rini - and only three male "
    "students - Biman, Mathew and Shyamal - in a course. The course has two evaluation "
    "components, a project and a test. The aggregate score in the course is a weighted "
    "average of the two components, with the weights being positive and adding to 1. The "
    "projects are done in groups of two, with each group consisting of a female and a male "
    "student. Both the group members obtain the same score in the project. The following "
    "additional facts are known about the scores in the project and the test. "
    "1. The minimum, maximum and the average of both project and test scores were identical "
    "- 40, 80 and 60, respectively. 2. The test scores of the students were all multiples of "
    "10; four of them were distinct and the remaining two were equal to the average test "
    "scores. 3. Amala's score in the project was double that of Koli in the same, but Koli "
    "scored 20 more than Amala in the test. Yet Amala had the highest aggregate score. "
    "4. Shyamal scored the second highest in the test. He scored two more than Koli, but two "
    "less than Amala in the aggregate. 5. Biman scored the second lowest in the test and the "
    "lowest in the aggregate. 6. Mathew scored more than Rini in the project, but less than "
    "her in the test."
)

_AC_PASSAGE = (
    "An air conditioner (AC) company has four dealers - D1, D2, D3 and D4 in a city. It is "
    "evaluating sales performances of these dealers. The company sells two variants of ACs - "
    "Window and Split. Both these variants can be either Inverter type or Non-inverter type. "
    "It is known that of the total number of ACs sold in the city, 25% were of Window "
    "variant, while the rest were of Split variant. Among the Inverter ACs sold, 20% were of "
    "Window variant. The following information is also known: "
    "1. Every dealer sold at least two Window ACs. 2. D1 sold 13 Inverter ACs, while D3 sold "
    "5 Non-inverter ACs. 3. A total of six Window Non-inverter ACs and 36 Split Inverter ACs "
    "were sold in the city. 4. The number of Split ACs sold by D1 was twice the number of "
    "Window ACs sold by it. 5. D3 and D4 sold an equal number of Window ACs and this number "
    "was one-third of the number of similar ACs sold by D2. "
    "6. D2 and D3 were the only ones who sold Window Non-inverter ACs. The number of these "
    "ACs sold by D2 was twice the number of these ACs sold by D3. "
    "7. D3 and D4 sold an equal number of Split Inverter ACs. This number was half the number "
    "of similar ACs sold by D2."
)

QUESTIONS = [
    q(
        "cat2023_dilr_slot3_set1",
        "TITA",
        "What was the total number of registrations in April?",
        passage=_REG_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set1",
        "TITA",
        "What was the number of online registrations in January?",
        passage=_REG_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set1",
        "MCQ",
        "Which of the following statements can be true?\n"
        "I. The number of offline registrations was the smallest in May.\n"
        "II. The total number of registrations was the smallest in February.",
        options=["Only I", "Both I and II", "Neither I nor II", "Only II"],
        passage=_REG_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set1",
        "MCQ",
        "What best can be concluded about the number of offline registrations in February?",
        options=["80", "50", "50 or 80", "30 or 50 or 80"],
        passage=_REG_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set1",
        "MCQ",
        "Which pair of months definitely had the same total number of registrations?\n"
        "I. January and April\n"
        "II. February and May",
        options=["Only II", "Only I", "Both I and II", "Neither I nor II"],
        passage=_REG_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set3",
        "TITA",
        "What was Rini's score in the project?",
        passage=_SCORES_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set3",
        "MCQ",
        "What was the weight of the test component?",
        options=["0.60", "0.75", "0.40", "0.50"],
        passage=_SCORES_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set3",
        "MCQ",
        "What was the maximum aggregate score obtained by the students?",
        options=["62", "66", "80", "68"],
        passage=_SCORES_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set3",
        "TITA",
        "What was Mathew's score in the test?",
        passage=_SCORES_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set3",
        "MCQ",
        "Which of the following pairs of students were part of the same project team?\n"
        "(i) Amala and Biman\n"
        "(ii) Koli and Mathew",
        options=["Only (i)", "Only (ii)", "Both (i) and (ii)", "Neither (i) nor (ii)"],
        passage=_SCORES_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set4",
        "TITA",
        "How many Split Inverter ACs did D2 sell?",
        passage=_AC_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set4",
        "MCQ",
        "What percentage of ACs sold were of Non-inverter type?",
        options=["75%", "20%", "25%", "4.33%"],
        passage=_AC_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set4",
        "TITA",
        "What was the total number of ACs sold by D2 and D4?",
        passage=_AC_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set4",
        "MCQ",
        "Which of the following statements is necessarily false?",
        options=[
            "D1 and D3 sold an equal number of Split ACs.",
            "D2 sold the highest number of ACs.",
            "D1 and D3 together sold more ACs as compared to D2 and D4 together.",
            "D4 sold more Split ACs as compared to D3.",
        ],
        passage=_AC_PASSAGE,
    ),
    q(
        "cat2023_dilr_slot3_set4",
        "MCQ",
        "If D3 and D4 sold an equal number of ACs, then what was the number of Non-inverter "
        "ACs sold by D2?",
        options=["5", "7", "6", "4"],
        passage=_AC_PASSAGE,
    ),
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = (
            db.query(CatQuestion)
            .filter(
                CatQuestion.source_year == SOURCE_YEAR,
                CatQuestion.section == "DILR",
                CatQuestion.source_slot == SOURCE_SLOT,
            )
            .count()
        )
        if existing > 0:
            print(
                f"CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} PYQs already seeded "
                f"({existing} rows); skipping."
            )
            return

        for item in QUESTIONS:
            db.add(
                CatQuestion(
                    section=item["section"],
                    question_type=item["question_type"],
                    topic=item["topic"],
                    difficulty=item["difficulty"],
                    source=item["source"],
                    source_year=item["source_year"],
                    source_slot=item["source_slot"],
                    group_id=item["group_id"],
                    passage_text=item["passage_text"],
                    question_text=item["question_text"],
                    options=item["options"],
                    correct_answer=None,
                    explanation=None,
                    is_active=True,
                )
            )
        db.commit()
        print(f"Seeded {len(QUESTIONS)} CAT {SOURCE_YEAR} DILR {SOURCE_SLOT} PYQ questions.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
