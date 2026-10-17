"""Backfill missing correct_answer/explanation for CAT 2025 VARC Slot 3.

Source: pyq-source/2025/VARC_SLOT3_CAT_2025_SOLUTIONS.pdf, cross-checked
against pyq-source/2025/VARC_SLOT3_CAT_2025.pdf for sentence numbering used
by para-jumble/odd-one-out questions.

Matched by id directly. Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered,
and MCQ answers are verified to be one of the row's options before writing.

Run with:
    python -m app.scripts.backfill_varc_2025_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot3"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        389,
        "With fixed moral starting points and expanding computational resources, the argument forecasts convergence on one ethical system and treats contextual judgment as unnecessary once formal reasoning scales across domains and cultures.",
        "The passage's physics analogy predicts continuing divergence across "
        "ethical frameworks, not convergence on one; so claiming the argument "
        "forecasts a single unified system is the one inference NOT supported.",
    ),
    (
        390,
        "The passage weighs the appeal of an impersonal AI judge against doubts about moral grasp. It warns that codification can erode case-sensitive judgment, allow axiom-led reasoning at scale, and use a physics analogy to model structured plurality.",
        "This option captures the passage's balance between the appeal of an "
        "impersonal AI judge and doubts about its moral grasp, plus the "
        "codification-erodes-judgment warning and the physics analogy, without distortion.",
    ),
    (
        391,
        "There is a principled way to decide which ethical framework applies to which class of cases, so the system can select the relevant starting points before deriving a recommendation.",
        "For the ethics-physics analogy to guide practice, the system must be "
        "able to principled-ly pick which framework's fixed starting points apply "
        "to a given case before reasoning from them - this assumption is required for the comparison to work.",
    ),
    (
        392,
        "The council followed a priorititarian approach, assigning greater moral weight to improvements for the worst-off rather than to maximising total welfare across the affected population.",
        "Utilitarianism maximises total/aggregate welfare; prioritarianism "
        "instead weights gains to the worst-off more heavily, making it the "
        "closest opposite among the options.",
    ),
    (
        393,
        "The 1982 draft forest act replicated colonial measures of control and regulation of forest resources.",
        "The controversy grew larger because the 1982 draft act was seen as "
        "replicating the same colonial-era control-and-regulation measures that "
        "had long been resented, escalating the original dispute.",
    ),
    (
        394,
        "Involving local people in cultivating forests.",
        "The passage indicates that meaningfully involving local communities in "
        "forest cultivation remains an unmet reform in India's forest policy, "
        "unlike the other listed items which have already been addressed.",
    ),
    (
        395,
        "Both resulted in large scale deforestation.",
        "The passage does not claim both the 1878 Act and the 1982 draft act "
        "directly caused large-scale deforestation; the shared traits it "
        "describes are the state's monopoly claim, the controversy they sparked, "
        "and their colonial mindset, not a deforestation outcome.",
    ),
    (
        396,
        "Nineteenth century German forestry experts were infamous for violating the rights of indigenous communities that lived in forest regions.",
        "This statement, if true, would actually reinforce the passage's "
        "narrative about colonial-style forestry violating indigenous rights, "
        "rather than weaken it - making it the EXCEPT answer among the "
        "otherwise narrative-undermining options.",
    ),
    (
        397,
        "Option 3",
        "The genetic-location sentence belongs right after the paragraph "
        "describes the affected males' undesirable behaviours and right before "
        "the sentence identifying the specific point mutation, placing it at blank 3.",
    ),
    (
        398,
        "1",
        "Sentences 2, 4, 5 and 3 (universality, ubiquity, cognitive demand, "
        "identity) form a coherent chain about music; sentence 1, which pivots to "
        "emotional-impact research, is the odd one out.",
    ),
    (
        399,
        "4312",
        "Sentence 4 introduces activists coining 'Latinx'; sentence 3 objects "
        "('They have done this...') that grammatical gender isn't sociological; "
        "sentence 1 gives Cherie Moraga's personal resistance; sentence 2 closes "
        "with usage statistics - giving the order 4-3-1-2.",
    ),
    (
        400,
        "Option 3",
        "The sentence about productivity gains now enriching wealth-holders "
        "bridges the 'erosion of mechanisms' idea just before it and the 'capital "
        "income boosted by design' line just after it, fitting at blank 3.",
    ),
    (
        401,
        "The mindful Indian shopper is shifting away from convenience and uniformity of clothing, and waste in fashion, to customisation and less exorbitantly priced clothing.",
        "This option captures all three elements the passage lists - the shift "
        "from fast-fashion homogeneity, the move away from fashion waste, and "
        "the pull toward affordable customisation - without the overreach of the other options.",
    ),
    (
        402,
        "1",
        "Sentences 2, 4, 5, 3 build a chain about music's universality, cognitive "
        "demand, and tie to identity; sentence 1, about emotional impact "
        "inspiring research, introduces an unrelated strand and is the odd one out.",
    ),
    (
        403,
        "2143",
        "Sentence 2 introduces candidates using portraits and promises analysis; "
        "sentence 1 explains the immediate personal-link effect; sentence 4 widens "
        "to the political/systemic effect; sentence 3 closes with the deepest "
        "conceptual claim - giving the order 2-1-4-3.",
    ),
    (
        404,
        "The drive to control nature is evident not only in mega-infrastructures like the Hoover and Aswan dams, but in smaller dams as well.",
        "The passage contrasts the charismatic Hoover and Aswan dams with the "
        "tens of thousands of smaller, unnoticed dams to show the same "
        "nature-control impulse runs through both scales.",
    ),
    (
        405,
        "Exemplification and manifestation",
        "In context, 'instantiation' describes dams as the physical embodiment "
        "of an abstract drive to control nature - exactly what 'exemplification "
        "and manifestation' convey.",
    ),
    (
        406,
        "Smaller, though not inconsequential, dams are safer than large dam projects.",
        "The passage never compares the safety of small versus large dams; it "
        "only notes smaller dams are 'not inconsequential' in their impact, "
        "making this safety claim the unsupported EXCEPT answer.",
    ),
    (
        407,
        "Mega-infrastructure - Sacrifice zone - Worshipping modernity - Water impoundment",
        "These four terms trace the passage's spine in order - what dams are "
        "(mega-infrastructure), what they cost (sacrifice zone), how they're "
        "justified (worshipping modernity), and the overall trend (water impoundment).",
    ),
    (
        408,
        "accommodate existential fluidity.",
        "The passage attributes non-human emotion in tribal narratives to a "
        "'fusion between various planes of existence' - a dissolving of "
        "boundaries between human and non-human that the option labels 'existential fluidity.'",
    ),
    (
        409,
        "Imagination helps humans make sense of space while memory helps them understand time.",
        "The passage repeatedly organizes its contrast between imagination and "
        "memory along the space-versus-time axis, including the tribal example "
        "of turning to memory/time once territorial/space domination wasn't available.",
    ),
    (
        410,
        "Tribal stories depict the natural world in accordance with rational scientific knowledge.",
        "The passage describes tribal narratives as dreamlike, hallucinatory and "
        "non-rational (oceans flying, mountains swimming), directly contradicting "
        "any claim that they follow rational scientific knowledge - making this the EXCEPT answer.",
    ),
    (
        411,
        "For tribals, conversing with the dead becomes a way of seeking control over time.",
        "Having lost territorial/spatial domination, tribal communities turned "
        "to mastering time instead, and ancestor-worship/conversing with the "
        "dead is presented as the ritual expression of that pursuit of control over time.",
    ),
    (
        412,
        "That which we call \"knowledge of the past\" is logically independent of the past, since the act of remembering which forms memory-beliefs happens in the present, and does not need to be based in real past occurrences, or even need a past at all.",
        "This option captures the passage's full thesis - memory-beliefs are "
        "present occurrences logically independent of any real past - rather "
        "than just the illustrative five-minutes-ago example that the other options lean on.",
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
