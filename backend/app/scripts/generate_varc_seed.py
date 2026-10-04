"""Generate a seed_cat_pyq_<year>_varc.py file from pyq_varc_parser.py JSON
output for each of a year's 3 slots. This is the automation half of the
token-saving VARC pipeline: pdftotext -> pyq_varc_parser.py -> (this script)
-> ready-to-run seed script, with no LLM transcription involved for the
clean-text majority of content.

Usage:
    python3 generate_varc_seed.py <year> <slot1.json> <slot2.json> <slot3.json> > seed_cat_pyq_<year>_varc.py
"""
import json
import sys


def infer_topic(q):
    if q["group_id"]:
        return "Reading Comprehension"
    text = q["question_text"].lower()
    if "odd" in text and ("sentence" in text or "jumbled" in text):
        return "Odd Sentence Out"
    if "properly sequenced" in text or "four sentences" in text or "coherent paragraph" in text:
        return "Para-jumble"
    if "missing in the paragraph" in text or "best fit" in text or "would best fit" in text:
        return "Sentence Insertion"
    if "summary" in text:
        return "Paragraph Summary"
    return "Verbal Ability"


def py_str(s):
    return json.dumps(s, ensure_ascii=False)


def py_list(items):
    if items is None:
        return "None"
    return "[" + ", ".join(py_str(i) for i in items) + "]"


def main():
    year = sys.argv[1]
    slot_files = sys.argv[2:5]

    out = []
    out.append(f'"""Seed real CAT {year} VARC questions, all 3 slots, generated from the')
    out.append("official solutions PDFs via pdftotext + pyq_varc_parser.py (automated")
    out.append("text-layer extraction, not LLM transcription - see that script's")
    out.append("docstring for the parsing approach and its known limitations).")
    out.append("")
    out.append(
        "`correct_answer`/`explanation` are intentionally left blank for now - the "
        "answer key"
    )
    out.append("is loaded separately once transcribed from the solutions PDFs.")
    out.append("")
    out.append("Run with:")
    out.append(f"    python -m app.scripts.seed_cat_pyq_{year}_varc")
    out.append('"""')
    out.append("")
    out.append("from app.database.database import Base, SessionLocal, engine")
    out.append("from app.models.cat_question import CatQuestion")
    out.append("")
    out.append(f"SOURCE_YEAR = {year}")
    out.append("")
    out.append("")
    out.append("def q(group_id, slot, topic, qtype, text, options=None, passage=None):")
    out.append("    return {")
    out.append('        "section": "VARC",')
    out.append('        "question_type": qtype,')
    out.append('        "topic": topic,')
    out.append('        "difficulty": "hard",')
    out.append('        "source": "pyq",')
    out.append('        "source_year": SOURCE_YEAR,')
    out.append('        "source_slot": slot,')
    out.append('        "group_id": group_id,')
    out.append('        "passage_text": passage,')
    out.append('        "question_text": text,')
    out.append('        "options": options,')
    out.append("    }")
    out.append("")
    out.append("")
    out.append("QUESTIONS = []")

    total = 0
    for slot_idx, jf in enumerate(slot_files, start=1):
        with open(jf, "r", encoding="utf-8") as f:
            data = json.load(f)
        out.append("")
        out.append(f"# ============================================================ SLOT {slot_idx} ====")
        out.append(f'_slot = "slot{slot_idx}"')
        out.append("QUESTIONS += [")
        for item in data:
            qtype = item["question_type"]
            text = py_str(item["question_text"])
            options = py_list(item["options"])
            group_id = py_str(item["group_id"]) if item["group_id"] else "None"
            passage = py_str(item["passage_text"]) if item["passage_text"] else "None"
            topic = py_str(infer_topic(item))
            out.append(
                f"    q({group_id}, _slot, {topic}, {py_str(qtype)}, {text}, "
                f"options={options}, passage={passage}),"
            )
            total += 1
        out.append("]")

    out.append("")
    out.append("")
    out.append("def seed() -> None:")
    out.append("    Base.metadata.create_all(bind=engine)")
    out.append("    db = SessionLocal()")
    out.append("    try:")
    out.append("        existing = (")
    out.append("            db.query(CatQuestion)")
    out.append(
        "            .filter(CatQuestion.source_year == SOURCE_YEAR, CatQuestion.section "
        '== "VARC")'
    )
    out.append("            .count()")
    out.append("        )")
    out.append("        if existing > 0:")
    out.append(
        f'            print(f"CAT {{SOURCE_YEAR}} VARC PYQs already seeded ({{existing}} '
        'rows); skipping.")'
    )
    out.append("            return")
    out.append("")
    out.append("        for item in QUESTIONS:")
    out.append("            db.add(")
    out.append("                CatQuestion(")
    out.append('                    section=item["section"],')
    out.append('                    question_type=item["question_type"],')
    out.append('                    topic=item["topic"],')
    out.append('                    difficulty=item["difficulty"],')
    out.append('                    source=item["source"],')
    out.append('                    source_year=item["source_year"],')
    out.append('                    source_slot=item["source_slot"],')
    out.append('                    group_id=item["group_id"],')
    out.append('                    passage_text=item["passage_text"],')
    out.append('                    question_text=item["question_text"],')
    out.append('                    options=item["options"],')
    out.append("                    correct_answer=None,")
    out.append("                    explanation=None,")
    out.append("                    is_active=True,")
    out.append("                )")
    out.append("            )")
    out.append("        db.commit()")
    out.append(
        f'        print(f"Seeded {{len(QUESTIONS)}} CAT {{SOURCE_YEAR}} VARC PYQ questions.")'
    )
    out.append("    finally:")
    out.append("        db.close()")
    out.append("")
    out.append("")
    out.append('if __name__ == "__main__":')
    out.append("    seed()")

    print("\n".join(out))
    print(f"# total questions: {total}", file=sys.stderr)


if __name__ == "__main__":
    main()
