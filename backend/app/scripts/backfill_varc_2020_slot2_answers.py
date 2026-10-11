"""Backfill correct_answer + explanation for CAT 2020 VARC Slot 2 (all 26 rows
were loaded with both fields null). Solved from the stored passage/question/
options text directly, not copied from any official key. Matched by id.

Run with:
    python -m app.scripts.backfill_varc_2020_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot2"

ANSWERS = [
    (529, "Phenomena supplemental to the evidence.", "Author contrasts images as \"evidence for explanation\" against epiphenomena - phenomena that merely accompany the real evidence rather than being the evidence itself."),
    (530, "studying visual culture requires institutional structures without which the structures of perception cannot be analysed.", "Passage never claims institutional structures are a precondition for analysing perception; institutions appear in a different context (configuring agents/practices), so this overreaches."),
    (531, "Social analytical accounts of people like Michelangelo or Leonardo cannot explain their genius.", "The passage says social analysis can illuminate reception/meaning but can't account for their unique creative genius itself."),
    (532, "Sight becomes a meaningful visual experience because of covenants of meaningfulness that we establish with the images we see.", "Restates that seeing becomes meaningful only through shared conventions (\"covenants\") with images."),
    (533, "Imagery, Visual Practices, Lifeworlds, Structures of Perception.", "These map directly onto the passage's four stated concerns of visual-culture scholarship."),
    (534, "Lehr does not assign adequate blame to empire builders for their past deeds.", "By sticking to \"disorganised small fry\" and skipping large organised colonial powers, Lehr avoids holding empire-builders to the same piracy standard."),
    (535, "if we eliminate poverty and income disparities in affected regions.", "Passage ties piracy's root cause to poverty/need, and notes welfare investment (not warships) stopped Malaysian piracy long-term."),
    (536, "ironic, about the reasons why so many took to piracy in medieval times.", "The rhetorical comparison of a peasant's toil to a pirate's easy riches is an ironic observation on motive, not literal indignation or analysis."),
    (537, "colonialism’s disruption of historic ties among countries.", "Passage credits colonialism with weakening internal power balances (creating opportunists), not disrupting \"ties among countries\" - the other three causes are explicitly stated."),
    (538, "The example of agricultural finance helps us to see how to concentrate corporate activity in the renewable energy sector.", "Passage uses the agricultural finance analogy only to describe how concentrated control generates profit, not as a how-to guide for concentrating activity."),
    (539, "Renewable energy systems have little or no environmental impact.", "If this claim is false (i.e. renewables do have real environmental impact), it reinforces the passage's warning against treating renewables as impact-free."),
    (540, "The author has reservations about the consequences of renewable energy systems.", "The first paragraph flags both environmental/social costs and profitability limits of renewables specifically, not non-renewables."),
    (541, "The development of the renewable energy sector is a double-edged sword.", "The last paragraph shows renewables can democratise energy access but need concentrated financial control to be profitable - a genuine trade-off."),
    (542, "More stringent global policies and regulations to ensure a more just system of toxic waste disposal.", "Directly follows the passage's critique that toxic-waste disposal perpetuates social injustice."),
    (543, "In certain kinds of aggression, inflicting pain is not the objective, and is no more than a utilitarian means to achieve another end.", "This is the definition of instrumental aggression given just before the torture example."),
    (544, "acommon theory of aggression is that it is the result of an abnormally low neural regulation of testosterone.", "Passage separately discusses low neural inhibition of aggressive impulses and testosterone's hormonal effect; it never merges them into one \"neural regulation of testosterone\" theory."),
    (545, "Aggressor — Circumstances of aggression — Victim.", "These are explicitly named as the three key variables: the aggressor, the social situation, and the target."),
    (546, "aggression in most societies is kept under control through moderating the death instinct identified by Freud.", "The passage never discusses societal control of aggression via moderating the death instinct; it only describes causes of aggression."),
    (547, "B, A, C, D", "Opens by naming nuclear fission as the most dangerous change (B), notes the layman's attention goes to the atom bomb instead (A), pivots with \"however\" to the greater danger of \"peaceful\" uses (C), and closes with the resulting ionizing radiation as the real threat (D)."),
    (548, "D, A, C, B", "Opens with the everyday observation of unnoticed big shifts (D), explains the brain can't process everything (A), continues \"it cannot be aware of every single thing\" (C), and names the phenomenon \"change blindness\" (B)."),
    (549, "Thomas Hobbes theorized the emergence of sovereign states based on a transactional relationship between people and sovereign state that was necessitated by a sense of insecurity of the people.", "Matches the passage's people-surrender-rights-for-security bargain."),
    (550, "Decisions based on intuition and information result in differential soeed and ability to provide a rationale.", "Captures both contrasted dimensions (speed and explainability) the passage draws between intuitive and informational decisions."),
    (551, "With the diversity of urban landscapes, measurable criteria for defining urban areas may need to be supplemented with human judgement.", "Matches the passage's conclusion that a richer criteria set needs human judgment given diverse urban forms."),
    (552, "There is, alongside the world of monopolised information and surveillance, a different dynamic growing up: information as a social good, incapable of being owned or exploited or priced.", "The other four sentences chain via explicit referents (\"this\", \"Yet\") into one argument about monopolising vs. replicable data; this sentence stands apart without that connective link."),
    (553, "As more and more stories of sexual assault have been made public in the last two years, the genre of their telling has exploded --- crimes have a tendency to become not just stories but genres.", "The other four sentences build one argument about victims' narratives being skewed toward the past; this one shifts to the unrelated point about the growing volume/genre of assault stories."),
    (554, "B, A, D, C", "Introduces the VLT's four main telescopes (B), adds its four auxiliary telescopes (A), explains combining them produces interferometry (D), and closes with the resulting capability to resolve an astronaut on the Moon (C)."),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_id, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.id == question_id,
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "VARC",
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: id={question_id}")
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
