"""Generate a seed_cat_pyq_<year>_qa.py file from pyq_qa_parser.py JSON
output for each of a year's 3 slots. Mirrors generate_varc_seed.py /
generate_dilr_seed.py.

Questions flagged as "garbage" (embedded-math image content pdftotext
couldn't recover - a run of 3+ spaces where an equation used to be, or an
empty option) are skipped entirely, not fabricated. Reported on stderr.

Usage:
    python3 generate_qa_seed.py <year> <slot1.json> <slot2.json> <slot3.json> > seed_cat_pyq_<year>_qa.py
"""
import json
import sys


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
    out.append(f'"""Seed real CAT {year} QA questions, generated from the official')
    out.append("solutions PDFs via pdftotext + pyq_qa_parser.py (automated text-layer")
    out.append("extraction, not LLM transcription).")
    out.append("")
    out.append(
        "Roughly half of CAT QA questions embed their math as a rendered image "
        "pdftotext can't recover (shows up as a run of blank space where an "
    )
    out.append(
        "equation used to be, or an empty option) - those are intentionally "
        "omitted here, not fabricated. See stderr from the generation step for "
    )
    out.append("which question numbers were skipped per slot.")
    out.append("")
    out.append(
        "`correct_answer`/`explanation` are intentionally left blank for now - the "
        "answer key"
    )
    out.append("is loaded separately once transcribed from the solutions PDFs.")
    out.append("")
    out.append("Run with:")
    out.append(f"    python -m app.scripts.seed_cat_pyq_{year}_qa")
    out.append('"""')
    out.append("")
    out.append("from app.database.database import Base, SessionLocal, engine")
    out.append("from app.models.cat_question import CatQuestion")
    out.append("")
    out.append(f"SOURCE_YEAR = {year}")
    out.append("")
    out.append("")
    out.append("def q(slot, qtype, text, options=None):")
    out.append("    return {")
    out.append('        "section": "QA",')
    out.append('        "question_type": qtype,')
    out.append('        "topic": "Quantitative Aptitude",')
    out.append('        "difficulty": "hard",')
    out.append('        "source": "pyq",')
    out.append('        "source_year": SOURCE_YEAR,')
    out.append('        "source_slot": slot,')
    out.append('        "group_id": None,')
    out.append('        "passage_text": None,')
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
        flagged = data.get("flagged", [])
        if flagged:
            print(f"slot{slot_idx}: skipping garbage (unrecoverable-math) questions: {flagged}", file=sys.stderr)
        out.append("")
        out.append(f"# ============================================================ SLOT {slot_idx} ====")
        out.append(f'_slot = "slot{slot_idx}"')
        out.append("QUESTIONS += [")
        for item in data["questions"]:
            qtype = item["question_type"]
            text = py_str(item["question_text"])
            options = py_list(item["options"])
            out.append(f"    q(_slot, {py_str(qtype)}, {text}, options={options}),")
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
        '== "QA")'
    )
    out.append("            .count()")
    out.append("        )")
    out.append("        if existing > 0:")
    out.append(
        f'            print(f"CAT {{SOURCE_YEAR}} QA PYQs already seeded ({{existing}} '
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
        f'        print(f"Seeded {{len(QUESTIONS)}} CAT {{SOURCE_YEAR}} QA PYQ questions.")'
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
