"""Backfill missing correct_answer/explanation for CAT 2025 VARC Slot 1.

Source: pyq-source/2025/VARC_2025_SLOT1_CAT_SOLUTIONS.pdf (note the
year/slot order in this filename is swapped relative to the other VARC
solution files). Cross-checked against pyq-source/2025/VARC_SLOT1_CAT_2025.pdf
for the raw passage/sentence numbering used by para-jumble/odd-one-out
questions.

Matched by id directly. Every update is still guarded by
correct_answer.is_(None) so an already-populated row can never be clobbered,
and MCQ answers are verified to be one of the row's options before writing.

Run with:
    python -m app.scripts.backfill_varc_2025_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2025
SOURCE_SLOT = "slot1"

# (id, correct_answer, explanation)
ANSWERS = [
    (
        341,
        "1",
        "Sentences 2-3-4-5 form a coherent paragraph about freedom over death "
        "and its link to assisted dying; sentence 1 ('Developments both "
        "technological and sociocultural...') is the odd one out.",
    ),
    (
        342,
        "defend electronic music from certain common charges.",
        "The author spends the passage responding to common objections "
        "(unfamiliarity, lack of traditional musical language) raised against "
        "electronic music, so the goal is to defend it from those charges.",
    ),
    (
        343,
        "Unfamiliar forms and terms might get in the way of our seeing electronic music as music, but this can be overcome.",
        "The 'communication problem' - unfamiliar forms and novel terms - is "
        "presented as an obstacle to recognizing electronic music as music, but "
        "one that can be overcome, directly tying back to the author's opening questions.",
    ),
    (
        344,
        "help us determine which sounds are musical and which are not.",
        "Stravinsky's description is used to complicate and expand our notion of "
        "music and to argue electronic music qualifies as music, not to give a "
        "rule for sorting musical from non-musical sounds - making that the EXCEPT answer.",
    ),
    (
        345,
        "Particular",
        "In context, 'sui generis' (literally 'of its own kind') is used to mean "
        "particular/unique, not generic, unaesthetic, or indescribable.",
    ),
    (
        346,
        "3142",
        "Sentence 3 introduces the panoptic mechanism as a way of making power "
        "function through functions; sentence 1 elaborates how it integrates into "
        "any function; sentence 4 summarises how power is subtly embedded; "
        "sentence 2 closes with the 'easy once you've thought of it' remark - giving the order 3-1-4-2.",
    ),
    (
        347,
        "Option 1",
        "Ava's general quote about 'old-world, traditional techniques' echoes the "
        "preceding general statement about embracing the great-grandfather's "
        "ways, so it fits right after it at gap 1, before the paragraph moves into "
        "the specific guitarron example.",
    ),
    (
        348,
        "Option 3",
        "The sentence about silver's historical role in 'show' needs to follow the "
        "discussion of why the market stayed buoyant despite domestic/economic "
        "changes and before the point about American museum collecting, placing it at gap 3.",
    ),
    (
        349,
        "the text attributes the COVID-19 pandemic rebound in financial markets solely to displaced sports bettors and treats their entry as the overriding cause of the rapid recovery across assets and time horizons.",
        "The passage hedges the sports-bettor point with words like 'potentially' "
        "and 'might', never claiming it is the sole or overriding cause - so this "
        "option overstates the text and is the unsupported EXCEPT answer.",
    ),
    (
        350,
        "The passage explains how noise can create order, then shows why complex systems with contagion are vulnerable to heavy-tailed cascades. It also explains why early shocks change rules through nonstationarity with a market illustration during the COVID-19 disruption.",
        "This option covers all four movements of the passage - noise creating "
        "order, heavy-tailed vulnerability in contagion systems, second-order tail "
        "events, and nonstationarity illustrated via the COVID-19 market episode - without distortion.",
    ),
    (
        351,
        "After a major equity crash, researchers find dense clusters of large daily moves for several weeks, with extreme days occurring far more often than in normal circumstances for assets with customarily low volatility profiles.",
        "This is the only option showing extreme events clustering after an "
        "initial shock (serial dependence), which directly strengthens the claim "
        "that a first-order tail event raises the probability of further tail events.",
    ),
    (
        352,
        "Individuals base movement choices partly on observed infections and on the behaviour of others. So, local responses interact, which turns many small adjustments into large scale patterns that can frustrate the intended aim of risk reduction.",
        "For contact-tracing apps to inadvertently raise risky interactions, "
        "individual behavioural choices must feed into each other so that small "
        "local adjustments aggregate into large-scale, counterproductive patterns - exactly this assumption.",
    ),
    (
        353,
        "3241",
        "Sentence 3 introduces women's socialized restraint on aggression; "
        "sentence 2 follows with what happens once that taboo breaks; sentence 4 "
        "develops the struggle with aggressive feelings; sentence 1 closes with the "
        "broad concluding contrast about everyone - giving order 3-2-4-1.",
    ),
    (
        354,
        "Aging leads to less effective apoptosis, and therefore zombie cells start to accumulate in the body, causing inflammation, which accelerates aging and leads to chronic diseases.",
        "This option preserves the passage's full causal chain: aging reduces "
        "apoptosis efficiency, which lets senescent cells accumulate, which causes "
        "inflammation, which in turn accelerates aging and chronic disease.",
    ),
    (
        355,
        "The borders of criminal responsibility.",
        "The last paragraph's list of middle-class, white, professional men "
        "(physicians and lawyers) are bound by their shared engagement with "
        "deciding the borders of criminal responsibility in court.",
    ),
    (
        356,
        "Physicians who specialised in the study of madness and the care of the insane in the nineteenth century.",
        "The passage directly defines alienists as physicians who specialised in "
        "the study of madness and the care of the insane in the nineteenth century.",
    ),
    (
        357,
        "Judgement, Insanity, Punishment, Responsibility.",
        "These four concepts - judgement of mental state, insanity as the "
        "medical-legal question, responsibility as liability, and punishment as "
        "the stake - are all central load-bearing ideas of the passage, unlike the "
        "other option sets which each include a peripheral term.",
    ),
    (
        358,
        "Referring to the practice of 'confession' in some faiths, here it is a metaphor for the religion of the defendant.",
        "In the list 'disease, gender, confession, or race', confession sits "
        "alongside other identity categories, so it is used as a metaphor for the "
        "defendant's religion, grouped with those other markers of difference.",
    ),
    (
        359,
        "1",
        "Sentences 2-3-4-5 build a coherent argument about how the Bayeux "
        "tapestry was displayed and experienced; sentence 1 ('The Bayeux tapestry "
        "was, therefore, an obvious way...') is the odd one out.",
    ),
    (
        360,
        "The passage outlines investment, incentive, and governance channels through which income inequality may support economic growth and reports short-term gains while noting long-term drawbacks.",
        "This option names the three specific channels (investment, incentive, "
        "governance) by which inequality may support growth and captures the "
        "passage's balanced short-term-gain-versus-long-term-drawback verdict.",
    ),
    (
        361,
        "After the emergency decree, the regime shifted toward authoritarianism as suffrage narrowed and opposition parties were deregistered.",
        "Democratization means widening political participation; narrowing "
        "suffrage and banning opposition parties is a textbook reversal of that "
        "process, making this the genuine opposite (the other options mislabel "
        "actually pro-democratic changes).",
    ),
    (
        362,
        "inequality can aid short-term growth in settings with high sunk costs, incentive alignment, and concentrated ownership.",
        "This option bundles all three arguments (investment indivisibilities, "
        "incentives, governance) and keeps the passage's conditional, short-run "
        "framing, matching exactly what the three-part case is built to show.",
    ),
    (
        363,
        "Pay rewards on verifiable performance for highly productive workers.",
        "The incentive/moral-hazard argument says tying pay to measurable output "
        "motivates effort and justifies the resulting inequality, which is "
        "exactly what this design describes.",
    ),
    (
        364,
        "Artists in a globalised world must navigate between drawing inspiration from diverse cultures respectfully and cultural appropriation that involves borrowing without proper acknowledgement which has broader societal impacts including perpetuating power imbalances.",
        "This option captures both paragraphs in proportion: the central tension "
        "between respectful inspiration and appropriation, plus the second "
        "paragraph's point that appropriation's harm extends to broader societal power imbalances.",
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
