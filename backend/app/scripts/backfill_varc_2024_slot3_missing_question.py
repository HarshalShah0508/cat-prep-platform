"""Add the missing CAT 2024 VARC Slot 3 Paragraph Summary question (Q.6 in
the source paper - pyq-source/2024/VARC_SLOT3_CAT_2024.pdf). Slot 3 only had
2 of the usual 3 Paragraph Summary questions loaded; this was the gap.
Solved from the source PDF's text directly - the solutions PDF skips this
particular question, so there's no official key to copy from.

Run with:
    python -m app.scripts.backfill_varc_2024_slot3_missing_question
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

QUESTION_TEXT = (
    "The passage given below is followed by four alternate summaries. Choose the option that "
    "best captures the essence of the passage. Lyric poetry is a genre of private meditation "
    "rather than public commitment. The impulse in Marxism toward changing a society deemed "
    "unacceptable in its basic design would seem to place demands on lyric poetry that such "
    "poetry, with its tendency toward the personal, the small scale, and the idiosyncratic, "
    "could never answer. There is within Marxism, however, also a strand of thought that would "
    "locate in lyric poetry alternative modes of perception and description that call forth a "
    "vision of worlds at odds with a repressive reality or that draw attention to the workings "
    "of ideology within the hegemonic culture. The poetic imagination may indeed deflect larger "
    "social concerns, but it may also be implicitly critical and utopian."
)

OPTIONS = [
    "Marxism has internal contradictions due to which one strand of Marxism sees no merit in lyric poetry while another appreciates the alternative modes of perception in poetry.",
    "The focus of lyric poetry as personal may not seem compatible with Marxism. However, it is possible to envisage lyric poetry as a symbol of resistance against an oppressive culture.",
    "Marxism makes unreasonable demands on lyric poetry. However, lyric poetry has its own merits that are largely ignored by Marxism due to its personal nature.",
    "The focus of lyric poetry is largely personal while that of Marxism is bringing change in society. Unless the difference is resolved, poetry will remain largely utopian.",
]

CORRECT_ANSWER = OPTIONS[1]

EXPLANATION = (
    "The passage sets up an apparent mismatch - lyric poetry's personal, small-scale nature "
    "seems unable to meet Marxism's demand for social change - then pivots with \"however\" to "
    "a strand within Marxism that instead sees lyric poetry as a critical, utopian vision "
    "against repressive reality. Option 2 is the only one that preserves both halves accurately: "
    "the seeming incompatibility, and poetry's recast role as resistance. Option 1 invents an "
    "\"internal contradiction\" and a strand that \"sees no merit\" - neither is stated. Option 3 "
    "claims poetry's merits are \"largely ignored\", when the passage says the opposite - a "
    "strand recognises them. Option 4 invents a resolution condition (\"unless the difference is "
    "resolved\") the passage never poses."
)


def backfill() -> None:
    db = SessionLocal()
    try:
        existing = (
            db.query(CatQuestion)
            .filter(
                CatQuestion.section == "VARC",
                CatQuestion.source_year == 2024,
                CatQuestion.source_slot == "slot3",
                CatQuestion.question_text == QUESTION_TEXT,
            )
            .first()
        )
        if existing is not None:
            print(f"Already present as id={existing.id}, skipping.")
            return

        row = CatQuestion(
            section="VARC",
            question_type="MCQ",
            topic="Paragraph Summary",
            difficulty="hard",
            source="pyq",
            source_year=2024,
            source_slot="slot3",
            question_text=QUESTION_TEXT,
            options=OPTIONS,
            correct_answer=CORRECT_ANSWER,
            explanation=EXPLANATION,
        )
        db.add(row)
        db.commit()
        print(f"Added missing CAT 2024 VARC Slot 3 Paragraph Summary question as id={row.id}.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
