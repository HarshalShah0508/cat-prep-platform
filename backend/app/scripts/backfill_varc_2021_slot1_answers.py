"""Backfill explanation for CAT 2021 VARC Slot 1 (correct_answer was already
resolved correctly by pyq_varc_parser_legacy.py at load time - this only adds
the explanation field, rewritten in plain language from the solutions PDF,
not copied verbatim). Matched against already-loaded rows by (source_year,
source_slot, section, question_text).

Run with:
    python -m app.scripts.backfill_varc_2021_slot1_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot1"

ANSWERS = [
    ("The author of this book review is LEAST likely to support the view that:", "tea became the leading drink in Britain in the nineteenth century.", "The author frames tea's history around social, moral, and marketing narratives rather than treating its popularity as a straightforward historical fact - so claiming tea simply \"became the leading drink\" misses the book's real emphasis."),
    ("This book review argues that, according to Rappaport, tea is unlike other “morality” products because it:", "appealed to a universal group and not just to a niche section of people.", "Rappaport highlights that tea's marketing uniquely reached across the whole of society rather than targeting one narrow group, unlike other \"morality\" products aimed at niche audiences."),
    ("Today, “conflat[ing] consumption with virtue” can be seen in the marketing of:", "sustainably farmed foods.", "Modern \"sustainably farmed foods\" marketing mirrors tea's old trick of tying consumption to a sense of virtue or moral good."),
    ("According to this book review, A Thirst for Empire says that, in addition to “profit-motivated marketers,” tea drinking was promoted in Britain by all of the following EXCEPT:", "tea drinkers lobbying for product diversity.", "The passage lists manufacturers, factories, and the anti-alcohol lobby as groups promoting tea - but never credits tea drinkers themselves with lobbying for more product variety."),
    ("Which one of the following best explains the “additional complexity” that the example of the incense burner illustrates regarding personhood for the Classic Maya?", "The example adds a new layer to the nonbinary understanding of personhood by bringing in a third category that shares a similar relation with the previous two.", "The incense burner example adds a third category of personhood beyond the simple human/nonhuman divide, showing a relationship similar to the other two categories already discussed."),
    ("Which one of the following, if true about the Classic Maya, would invalidate the purpose of the iPhone example in the passage?", "The personhood of the incense burner and the stone chopper was a function of their usefulness to humans.", "The iPhone comparison only works if personhood can come from a thing's relationship with humans - if the incense burner's \"personhood\" instead just reflected its usefulness to people, the comparison would fall apart."),
    ("On the basis of the passage, which one of the following worldviews can be inferred to be closest to that of the Classic Maya?", "A tribe that perceives plants as person-plants because they form an ecosystem and are marked by needs of nutrition.", "The Maya worldview treats plants and other nonhumans as persons when they're bound up in relationships (like ecosystems and nutritional needs) - closest to a tribe seeing plants as persons through their ecological ties."),
    ("Which one of the following, if true, would not undermine the democratising potential of the Classic Maya worldview?", "They depicted their human healers with physical attributes of local medicinal plants.", "Depicting human healers with plant-like attributes reinforces (rather than undermines) the Maya's nonbinary, boundary-crossing idea of personhood."),
    ("All of the following statements can be inferred from the passage EXCEPT that:", "Utopian and dystopian societies are twins, the progeny of the same parents.", "The passage treats utopia and dystopia as closely related, not as each other's opposite \"twins from the same parents\" - this framing goes further than what the passage actually argues."),
    ("Following from the passage, which one of the following may be seen as a characteristic of a utopian society?", "Institutional surveillance of every individual to ensure his/her security and welfare.", "A utopian society's drive for order and security, as the passage describes it, tends to come with surveillance of its members to maintain that security and welfare."),
    ("All of the following arguments are made in the passage EXCEPT that:", "In More’s time, there was plenty and security, so people did not need restraints that could appear unreasonable.", "The passage never argues that More's era had enough plenty and security to make strict rules feel unreasonable - every other listed point IS something the passage actually argues."),
    ("Which sequence of words below best captures the narrative of the passage?", "Utopia – Security – Homogeneity – Intentional community.", "The passage's narrative arc moves from utopia's promise, through its reliance on security, into enforced homogeneity, and finally into exclusive intentional communities."),
    ("All of the following constitute a point of difference between the “original” and “modified” versions of the marshmallow test EXCEPT that:", "The former correlated self-control and future success, while the latter correlated self-control and survival advantages.", "The original marshmallow test linked self-control to later life success, while the cuttlefish version linked it instead to survival-related advantages - that's the real point of difference, not any of the other listed options."),
    ("Which one of the following cannot be inferred from Alexandra Schnell’s experiment?", "Intelligence in a species is impossible without sociability.", "Schnell's cuttlefish experiment shows self-control in a solitary, non-social species, which directly undercuts the idea that intelligence requires sociability - so that claim cannot be inferred from the experiment."),
    ("In which one of the following scenarios would the cuttlefish’s behaviour demonstrate self-control?", "Asian shore crabs and raw prawns are simultaneously released while a live grass shrimp drawer labelled with a triangle is placed in front of the cuttlefish, to be opened after one minute.", "Self-control shows up precisely when the cuttlefish has to resist two immediately available foods to wait for its preferred one - the scenario with both shrimp and prawns on offer simultaneously, delayed only for the preferred option."),
    ("Which one of the following, if true, would best complement the passage’s findings?", "Cuttlefish live in big groups that exhibit sociability.", "If cuttlefish turned out to be more social than thought, that would support (not undercut) the passage's suggestion that self-control is linked to sociability."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage. McGurk and MacDonald (1976) reported a powerful multisensory illusion occurring with audio-visual speech. They recorded a voice articulating a consonant ‘ba-ba-ba’ and dubbed it with a face articulating another consonant ‘ga-ga-ga’. Even though the acoustic speech signal was well recognized alone, it was heard as another consonant after dubbing with incongruent visual speech i.e., ‘da-da-da’. The illusion, termed as the McGurk effect, has been replicated many times, and it has sparked an abundance of research. The reason for the great impact is that this is a striking demonstration of multisensory integration, where that auditory and visual information is merged into a unified, integrated percept.", "Visual speech mismatched with auditory speech can result in the perception of an entirely different message: this illusion is known as the McGurk effect.", "The passage's core point is that mismatched visual and auditory speech can trick the brain into perceiving an entirely different message - the McGurk effect."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage. Foreign peacekeepers often exist in a bubble in the poor countries in which they are deployed; they live in posh compounds, drive fancy vehicles, and distance themselves from locals. This may be partially justified as they are outsiders, living in constant fear, performing a job that is emotionally draining. But they are often despised by the locals, and many would like them to leave. A better solution would be bottom-up peacebuilding, which would involve their spending more time working with communities, understanding their grievances and earning their trust, rather than only meeting government officials.", "Peacekeeping forces in foreign countries have tended to be aloof for valid reasons but would be more effective if they worked more closely with local communities.", "The passage argues peacekeepers' isolation is understandable but ultimately counterproductive - they'd do better engaging more closely with the communities they serve."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage. Developing countries are becoming hotbeds of business innovation in much the same way as Japan did from the 1950s onwards. They are reinventing systems of production and distribution, and experimenting with entirely new business models. Why are countries that were until recently associated with cheap hands now becoming leaders in innovation? Driven by a mixture of ambition and fear they are relentlessly climbing up the value chain. Emerging-market champions have not only proved highly competitive in their own backyards, they are also going global themselves.", "Competition has driven emerging economies, once suppliers of cheap labour, to become innovators of business models that have enabled them to move up the value chain and go global.", "Developing economies have moved beyond just offering cheap labor, using competitive pressure to become genuine innovators that climb the value chain globally."),
    ("Five jumbled up sentences, related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd one out and key in the number of the sentence as your answer.", "Critics say the US is conferring rights that it has no authority to confer; Russia in particular has condemned this, citing the US’ disrespect for international law.", "The odd sentence breaks from the passage's focus on ambiguous legal frameworks for space commerce by instead making a specific claim about US-Russia diplomatic friction."),
    ("The four sentences (labelled 1, 2, 3, 4) below, when properly sequenced, would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "(2, 3, 4, 1)", "2, 3, 4, 1 - starting with the discovery of rapid neuron regeneration in zebrafish (2), narrowing to the specific cells studied (3), explaining how the regeneration depends on injury location (4), and closing with a broader comparison to other species (1)."),
    ("The four sentences (labelled 1, 2, 3, 4) below, when properly sequenced, would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "(2, 4, 3, 1)", "2, 4, 3, 1 - opening with the certainty of worsening global warming (2), linking that to trees' carbon-absorbing role (4), noting the problem of burning trees releasing that carbon (3), and closing with the popular call to plant more trees (1)."),
    ("The four sentences (labelled 1, 2, 3, 4) below, when properly sequenced, would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "(1, 2, 3, 4)", "1, 2, 3, 4 - the sentences build in their original logical order, from the text needing a reader to come alive, through the convergence of text and reader, to the work sitting between the two, and finally the two poles of artistic creation and aesthetic realization."),
    ("Five jumbled up sentences, related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd one out and key in the number of the sentence as your answer:", "In look and feel thus, they are exactly like any reputed journal.", "The odd sentence out praises predatory journals for looking just like legitimate ones - breaking from the other four sentences, which instead describe the actual problems with predatory academic publishing."),
]


def backfill() -> None:
    db = SessionLocal()
    try:
        updated = 0
        for question_text, correct_answer, explanation in ANSWERS:
            row = (
                db.query(CatQuestion)
                .filter(
                    CatQuestion.source_year == SOURCE_YEAR,
                    CatQuestion.source_slot == SOURCE_SLOT,
                    CatQuestion.section == "VARC",
                    CatQuestion.question_text == question_text,
                    CatQuestion.correct_answer.is_(None),
                )
                .first()
            )
            if row is None:
                print(f"NO MATCH: {question_text[:60]!r}")
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
