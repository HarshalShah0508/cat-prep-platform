"""Generate a seed_cat_pyq_<year>_dilr.py file from pyq_dilr_parser.py JSON
output for each of a year's 3 slots. Mirrors generate_varc_seed.py.

Questions belonging to a "flagged" (chart/diagram-dependent, text-
unrecoverable) set are skipped entirely - not fabricated, not loaded with
a broken passage. They're reported on stderr so they can be filled in
later once real chart images are supplied.

Usage:
    python3 generate_dilr_seed.py <year> <slot1.json> <slot2.json> <slot3.json> > seed_cat_pyq_<year>_dilr.py
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
    out.append(f'"""Seed real CAT {year} DILR questions, generated from the official')
    out.append("solutions PDFs via pdftotext + pyq_dilr_parser.py (automated")
    out.append("text-layer extraction, not LLM transcription).")
    out.append("")
    out.append(
        "Sets that are chart/diagram-dependent (the passage text only refers to "
        '"the figure above" etc. with no recoverable data) are intentionally '
    )
    out.append(
        "omitted here, not fabricated - see stderr output from the generation "
        "step for which sets were skipped."
    )
    out.append("")
    out.append(
        "`correct_answer`/`explanation` are intentionally left blank for now - the "
        "answer key"
    )
    out.append("is loaded separately once transcribed from the solutions PDFs.")
    out.append("")
    out.append("Run with:")
    out.append(f"    python -m app.scripts.seed_cat_pyq_{year}_dilr")
    out.append('"""')
    out.append("")
    out.append("from app.database.database import Base, SessionLocal, engine")
    out.append("from app.models.cat_question import CatQuestion")
    out.append("")
    out.append(f"SOURCE_YEAR = {year}")
    out.append("")
    out.append("")
    out.append("def q(group_id, slot, qtype, text, options=None, passage=None):")
    out.append("    return {")
    out.append('        "section": "DILR",')
    out.append('        "question_type": qtype,')
    out.append('        "topic": "Data Interpretation & Logical Reasoning",')
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
        flagged = set(data.get("flagged_sets", []))
        if flagged:
            print(f"slot{slot_idx}: skipping flagged (chart-dependent) sets: {sorted(flagged)}", file=sys.stderr)
        out.append("")
        out.append(f"# ============================================================ SLOT {slot_idx} ====")
        out.append(f'_slot = "slot{slot_idx}"')
        out.append("QUESTIONS += [")
        for item in data["questions"]:
            # pyq_dilr_parser.py flags by plain set number ("set_main");
            # pyq_dilr_parser_legacy.py flags by the group_id string itself.
            if item.get("set_main") in flagged or item.get("group_id") in flagged:
                continue
            qtype = item["question_type"]
            text = py_str(item["question_text"])
            options = py_list(item["options"])
            group_id = py_str(item["group_id"]) if item["group_id"] else "None"
            passage = py_str(item["passage_text"]) if item["passage_text"] else "None"
            out.append(
                f"    q({group_id}, _slot, {py_str(qtype)}, {text}, "
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
        '== "DILR")'
    )
    out.append("            .count()")
    out.append("        )")
    out.append("        if existing > 0:")
    out.append(
        f'            print(f"CAT {{SOURCE_YEAR}} DILR PYQs already seeded ({{existing}} '
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
        f'        print(f"Seeded {{len(QUESTIONS)}} CAT {{SOURCE_YEAR}} DILR PYQ questions.")'
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
