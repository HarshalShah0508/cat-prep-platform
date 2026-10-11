"""Add the 4 CAT 2021 DILR Slot 3 questions missing from the DB (16/20
loaded) - an entire set ("employees and projects Gantt chart") that was
never loaded at all. The local solutions PDF's AI-generated reasoning for
this set was internally inconsistent (different numbers for the same data
across questions), so all four answers were verified via web search
cross-checks against multiple independent sources (including a %-correct
statistic confirming Q17).

Run with:
    python -m app.scripts.backfill_dilr_2021_slot3_missing_questions
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

PASSAGE = (
    "The figure shows the schedule of four employees - Abani, Bahni, Danni, and Tinni - whom "
    "Dhoni supervised in 2020. Altogether there were five projects which started and concluded "
    "in 2020 in which they were involved. For each of these projects and for each employee, the "
    "starting day was at the beginning of a month and the concluding day was the end of a month, "
    "indicated by the left and right endpoints of the corresponding horizontal bars. The number "
    "within each bar indicates the percentage of assigned work completed by the employee for "
    "that project, as assessed by Dhoni.\n\n"
    "For each employee, his/her total project-month (in 2020) is the sum of the number of months "
    "(s)he worked across the five projects, while his/her annual completion index is the "
    "weighted average of the completion percentages across the different projects, with the "
    "weights being the corresponding number of months (s)he worked. For each project, the total "
    "employee-month is the sum of the number of months the four employees worked on this "
    "project, while its completion index is the weighted average of the completion percentages "
    "for the employees who worked on it, with the weights being the number of months they worked."
)

ROWS = [
    dict(
        question_text="Which of the following statements is/are true? I: The total project-month was the same for the four employees. II: The total employee-month was the same for the five projects.",
        options=["Only II", "Both I and II", "Neither I nor II", "Only I"],
        correct_answer="Only I",
        explanation="Each of the four employees worked a total of 9 months across their projects (Statement I true), but the five projects had differing total employee-months (6, 5, 9, 10, 6 - Statement II false).",
    ),
    dict(
        question_text="Which employees did not work in multiple projects for any of the months in 2020?",
        options=["Only Abani, Bahni and Danni", "Only Abani and Bahni", "All four of them", "Only Tinni"],
        correct_answer="Only Abani, Bahni and Danni",
        explanation="Checking each employee's project timeline for month-level overlaps, only Tinni has two projects active in the same month (November) - Abani, Bahni, and Danni never work on more than one project in any given month.",
    ),
    dict(
        question_text="The project duration, measured in terms of the number of months, is the time during which at least one employee worked in the project. Which of the following pairs of the projects had the same duration?",
        options=["Project 1, Project 5", "Project 4, Project 5", "Project 3, Project 5", "Project 3, Project 4"],
        correct_answer="Project 3, Project 4",
        explanation="Computing the span of months during which any employee was active on each project gives durations of 3, 3, 5, 5, and 4 months for Projects 1-5 respectively - Projects 3 and 4 share the same 5-month duration.",
    ),
    dict(
        question_text="The list of employees in decreasing order of annual completion index is:",
        options=["Danni, Tinni, Abani, Bahni", "Tinni, Danni, Abani, Bahni", "Danni, Tinni, Bahni, Abani", "Abani, Bahni, Danni, Tinni"],
        correct_answer="Danni, Tinni, Abani, Bahni",
        explanation="Computing each employee's weighted-average completion percentage (weighted by months worked on each project) from the chart gives the ranking Danni > Tinni > Abani > Bahni.",
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
                    CatQuestion.section == "DILR",
                    CatQuestion.source_year == 2021,
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
                source_year=2021,
                source_slot="slot3",
                group_id="cat2021_dilr_slot3_set4",
                passage_text=PASSAGE,
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
        print(f"Inserted {inserted} CAT 2021 DILR Slot 3 questions.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
