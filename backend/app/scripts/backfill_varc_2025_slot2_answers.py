"""Backfill missing correct_answer/explanation for CAT 2025 VARC Slot 2.

Source: pyq-source/2025/VARC_SLOT2_CAT_2025_SOLUTIONS.pdf, cross-checked
against pyq-source/2025/VARC_SLOT2_CAT_2025.pdf for sentence numbering used
by para-jumble/odd-one-out questions.

Matched by id directly. Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered,
and MCQ answers are verified to be one of the row's options before writing.

Run with:
    python -m app.scripts.backfill_varc_2025_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot2"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        365,
        "Contrary to the idea that humans always hurt nature and that it thrives in their absence, a lot of human action across history has been equally likely to increase biodiversity than reduce it, often creating varied ecological landscapes that support a vast array of species.",
        "This option captures the passage's central corrective claim - that human "
        "land use has often increased rather than only reduced biodiversity - "
        "without the overreach or narrower scope of the other summaries.",
    ),
    (
        366,
        "A comprehensive understanding of the human condition can best be achieved by combining the findings of disciplines from the arts and the sciences.",
        "The quoted statement praises bridging arts and sciences for producing "
        "valuable knowledge about the human condition, so the valid conclusion is "
        "that combining both disciplines best achieves that understanding.",
    ),
    (
        367,
        "Humans do not interact with places in subjective, emotional ways because places are only physical topography.",
        "The passage's core argument is that humans experience places subjectively "
        "and emotionally, not merely as physical topography, so denying this (as "
        "this option does) would directly contradict the passage if false - making "
        "it the only statement that, if false, would NOT contradict the argument.",
    ),
    (
        368,
        "Literature can convey how different people experience the same place differently.",
        "The literary description example is used to show how the same place can "
        "be experienced differently by different people, illustrating literature's "
        "capacity to convey subjective, varied experience.",
    ),
    (
        369,
        "The emotional and spiritual experience of a place can replace a surveyor's map.",
        "The second paragraph argues the emotional/spiritual experience is as real "
        "as the physical one, not that it replaces physical surveying altogether - "
        "making this overstated claim the one that is NOT true of the argument.",
    ),
    (
        370,
        "The neutrality of AI is conducive to critical thinking.",
        "The author argues AI's veneer of neutrality lulls users into absorbing "
        "biased responses without critical engagement - the opposite of this "
        "claim - so the author is least likely to agree with it.",
    ),
    (
        371,
        "\"When I queried ChatGPT about its rhetoric, it responded: 'The way I communicate is designed to foster trust and confidence in my responses, which can be both helpful and potentially misleading.'\"",
        "The other three examples are instances of AI bias in action (gendered "
        "images, Americanizing English, favoring Altman), while this example is "
        "AI commenting on its own rhetoric - serving a different illustrative "
        "purpose, making it the odd one out.",
    ),
    (
        372,
        "\"I'm not aware of research on whether ChatGPT tends to favor big tech, OpenAI or Altman, and I can only guess why it seemed that way in our conversation.\"",
        "This is the author's own hedge/disclaimer rather than a statement "
        "affirming the gap between tech companies' claims and what AI actually "
        "does, making it the EXCEPT answer.",
    ),
    (
        373,
        "AI tends to blame its training data when scrutinized for its biases.",
        "The 'beige office building' comparison is about AI's generalized, bland, "
        "falsely collegial tone meant to build trust - not about AI deflecting "
        "blame onto its training data, making this the EXCEPT answer.",
    ),
    (
        374,
        "But when these cells get too big, they can burst, which is why we often see chronic inflammation in humans and other animals that have stored a lot of fat in their tissues.",
        "This statement is a general biological fact about fat cells bursting and "
        "causing inflammation in humans/animals broadly, not specifically "
        "describing adaptation in Mexican tetra cavefish, making it the EXCEPT answer.",
    ),
    (
        375,
        "To control inflammation from the bursting of fat cells.",
        "Carotenoids are most likely functioning to control the inflammation "
        "caused by bursting overfilled fat cells in the cavefish, per the passage's discussion.",
    ),
    (
        376,
        "Only eyeless offspring had yellow fat.",
        "Riddle's actual inference from the cross was that carotenoid "
        "accumulation is NOT linked to eyelessness (some eyeless fish had white "
        "fat). A result showing a clean, perfect correlation - only eyeless "
        "offspring having yellow fat - would revive the eye-link hypothesis and "
        "thus invalidate that no-link inference.",
    ),
    (
        377,
        "Mexican tetra cavefish are similar to non-cave-dwelling variants in their early stages of development.",
        "Because cavefish embryos develop similarly to sighted surface fish before "
        "eye loss sets in, the resulting inefficiency of growing and then losing "
        "eye structures is biologically unavoidable given that shared early developmental pathway.",
    ),
    (
        378,
        "Option 1",
        "The disbelief sentence about Western customers follows the 'woven air' "
        "mystique set up at the very start of the passage and is resolved by the "
        "next sentence explaining the human, painstaking process - placing it at blank 1.",
    ),
    (
        379,
        "Milestone",
        "The passage frames instruments as either receptive (observing/detecting) "
        "or interventional (cutting/manipulating) tools; a milestone is neither - "
        "it simply marks distance/progress - making it the least applicable instrument.",
    ),
    (
        383,
        "2143",
        "Sentence 2 opens as the general topic sentence; sentence 1 responds with "
        "the contrasting 'dual citizenship' idea; sentence 4 follows by naming 1's "
        "'dual citizenship' point; sentence 3 closes by explaining that legacy - giving the order 2-1-4-3.",
    ),
    (
        384,
        "Option 4",
        "The sentence about taste's link to pleasure and embodiment, distinct from "
        "judgment, fits after the passage's broader discussion of the shift in "
        "meaning of 'taste', placed at blank 4 just before the closing point about neglected thinkers.",
    ),
    (
        385,
        "Celebrated icons of the gaming industry, Charles Darrow and Parker Brothers, snatched the feminist icon Elizabeth Magie's original design and transformed Monopoly into a worldwide phenomenon, while barely acknowledging her.",
        "This option keeps the two non-negotiable beats of the passage - the "
        "game's worldwide success and Magie's erased authorship/pittance payment "
        "- without distorting the facts the way the other three options do.",
    ),
    (
        386,
        "1",
        "Sentences 2-3-4-5 form a coherent paragraph about new Pfas research "
        "findings and their implications; sentence 1 ('Pfas are a class of about "
        "15,000 compounds...') is a general background fact and is the odd one out.",
    ),
    (
        387,
        "2413",
        "Sentence 2 is the topic sentence naming the familiar old-book scent; "
        "sentence 4 explains that it's chemistry, not dust; sentence 1 details the "
        "cellulose/lignin breakdown; sentence 3 names the specific compounds - giving the order 2-4-1-3.",
    ),
    (
        388,
        "4",
        "Sentences 1, 2, 3, and 5 paint Torres's persona and comedic content "
        "through colour-themed wordplay; sentence 4, which is dry production "
        "logistics about the camera and screen setup, is the odd one out.",
    ),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for qid, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == qid,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "VARC",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH for id={qid}")
                continue
            if row.options and correct_answer not in row.options:
                print(f"WARNING: answer not in options for id={qid}: {correct_answer!r} not in {row.options!r}")
                continue
            row.correct_answer = correct_answer
            row.explanation = explanation
            db.flush()
            updated += 1
        db.commit()
        print(f"Backfilled {updated} CAT {SOURCE_YEAR} VARC {SOURCE_SLOT} answers/explanations.")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()
