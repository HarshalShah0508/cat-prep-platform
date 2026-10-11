"""Backfill correct_answer + explanation for the remaining CAT VARC rows that
were loaded with both fields null: id 700 (2021 slot2), 722 (2021 slot3),
380 (2022 slot1), 453 (2023 slot1), 136/137/138 (2025 slot2).

A few of these rows also had corrupted `options`/`question_text` from the
original parse (a leaked answer key concatenated onto an option, several
options merged into one string, or truncated question text missing
sentences 2-4) - those are repaired here too, id 380's missing sentences
sourced from pyq-source/2022/VARC_SLOT1_CAT_2022.pdf which carries the
official "Possible Answer: 3214" key directly.

Run with:
    python -m app.scripts.backfill_varc_remaining_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

FIXES = {
    700: {
        "options": [
            "Look forward a few decades to an invention which can end the energy crisis, change the global economy and curb climate change at a stroke: commercial fusion power.",
            "To gain meaningful insights, logic has to be accompanied by asking probing questions of nature through controlled tests, precise observations and clever analysis.",
            "The greatest of all inventions is the über-invention that has provided the insights on which others depend: the modern scientific method.",
            "This invention is inconceivable without the scientific method; it will rest on the application of a diverse range of scientific insights, such as the process transforming hydrogen into helium to release huge amounts of energy.",
        ],
        "correct_answer": "3, 2, 1, 4",
        "explanation": "Starts with the scientific method as the foundation (3), moves to gaining insight via controlled experimentation (2), shifts to the world-changing invention this enables - fusion power (1), and closes by tying that invention back to the scientific method it depends on (4).",
    },
    722: {
        "options": [
            "A typical example is Wikipedia, where the overwhelming majority of contributors are male and so the available content is skewed to reflect their interests.",
            "Without diversity of thought and representation, society is left with a distorted picture of future options, which are likely to result in augmenting existing inequalities.",
            "Gross gender inequality in the technology sector is problematic, not only for the industry-wide marginalisation of women, but because technology designs embody the values of their makers.",
            "While redressing unequal representation in the workplace is a step in the right direction, broader social change is needed to address the structural inequalities embedded within the current organisation of work and employment.",
            "If technology merely reflects the perspectives of the male stereotype, then new technologies are unlikely to accommodate the diverse social contexts within which they operate.",
        ],
        "correct_answer": "While redressing unequal representation in the workplace is a step in the right direction, broader social change is needed to address the structural inequalities embedded within the current organisation of work and employment.",
        "explanation": "The other four sentences chain into one argument - tech design embodies its (male) makers' values (3), Wikipedia as the example (1), so new tech won't fit diverse contexts (5), leaving a distorted, unequal picture of the future (2). This sentence instead pivots to workplace representation as a policy fix, breaking that chain.",
    },
    380: {
        "question_text": (
            "The four sentences (labelled 1, 2, 3 and 4) below, when properly sequenced, would "
            "yield a coherent paragraph. Decide on the proper sequencing of the order of the "
            "sentences and key in the sequence of the four numbers as your answer: "
            "1. The creative element in product design has become of paramount importance as it "
            "is one of the few ways a firm or industry can sustain a competitive advantage over "
            "its rivals. "
            "2. In fact, the creative element in the value of world industry would be larger "
            "still, if we added the contribution of the creative element in other industries, "
            "such as the design of tech accessories. "
            "3. The creative industry is receiving a lot of attention today as its growth rate is "
            "faster than that of the world economy as a whole. "
            "4. It is for this reason that today's trade issues are increasingly involving "
            "intellectual property, as Western countries have an interest in protecting their "
            "revenues along with freeing trade in non-tangibles."
        ),
        "correct_answer": "3, 2, 1, 4",
        "explanation": "Official key (CAT 2022 Slot 1 source PDF: \"Possible Answer: 3214\"). Opens with the creative industry's fast growth (3), adds that its value would be even larger counting other industries (2), narrows to why the creative element matters commercially - competitive advantage (1), and closes with the resulting trade/IP tension (4).",
    },
    453: {
        "options": [
            "Colonialism surged in the 16th century due to advancements in navigation, enabling British settlements abroad and global dominance.",
            "As a result of developments in navigation technology, European colonialism, led to the displacement of indigenous populations and global political changes in the 16th century.",
            "Colonialism, conceptualized in the 16th century, allowed colonizers to expand their territories, establish settlements, and exercise political power.",
            "Technological advancements in navigation in the 16th century, transformed colonialism, enabling Europeans to establish settlements and exert political dominance over distant regions.",
        ],
        "correct_answer": "As a result of developments in navigation technology, European colonialism, led to the displacement of indigenous populations and global political changes in the 16th century.",
        "explanation": "Only this option keeps the passage's two key emphases together - navigation technology as the 16th-century trigger, and \"violent dispossession\" (displacement) alongside political change; the others drop the dispossession angle or narrow it to Britain alone.",
    },
    136: {
        "correct_answer": "In both astronomy and microbiology, progress has been the consequence of improvements in the instruments they use.",
        "explanation": "A direct restatement of the quoted claim - both disciplines described in the passage are shown to depend on ongoing instrumental improvement for progress.",
    },
    137: {
        "correct_answer": "Because of the relatively recent entry of computational machinery in mathematics, the field is only now beginning to develop a scientific culture.",
        "explanation": "The passage treats mathematics as already having its own science culture, just slow to become instrumentally embodied - claiming it is \"only now beginning to develop a scientific culture\" contradicts that framing, unlike the other options which stay consistent with the passage.",
    },
    138: {
        "correct_answer": "The author distinguishes between the receptive and interventionist uses of instruments in the sciences by comparing astronomy and biology, respectively.",
        "explanation": "This matches the passage directly (astronomy as \"largely a receptive science\", biology as \"far more interventional\"). The other options misattribute details - new astronomy began with radio astronomy, not Newton's reflecting telescopes, and Galileo (not Newton) observed Venus's phases and Jupiter's satellites.",
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
            if "options" in fix:
                row.options = fix["options"]
            if "question_text" in fix:
                row.question_text = fix["question_text"]
            row.correct_answer = fix["correct_answer"]
            row.explanation = fix["explanation"]
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} remaining CAT VARC answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
