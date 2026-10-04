"""Backfill explanation for CAT 2020 VARC Slot 3 (correct_answer was already
resolved correctly by pyq_varc_parser_flat.py at load time - this only adds
the explanation field, rewritten in plain language from the solutions PDF,
not copied verbatim). Matched against already-loaded rows by (source_year,
source_slot, section, question_text).

Run with:
    python -m app.scripts.backfill_varc_2020_slot3_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2020
SOURCE_SLOT = "slot3"

ANSWERS = [
    ("From the passage, we can infer that feminist scholars’ understanding of the experiences of Victorian women travellers is influenced by all of the following EXCEPT scholars’:", "knowledge of class tensions in Victorian society.", "Feminist scholars' understanding of Victorian women travellers draws on how identity forms, the researchers' own perspective, and gender awareness - but the passage doesn't tie it to class-tension knowledge specifically."),
    ("From the passage, we can infer that travel writing is most similar to:", "autobiographical writing.", "Travel writing closely resembles autobiographical writing, since both center on the writer's personal journey and self-discovery."),
    ("From the passage, it can be inferred that scholars argue that Victorian women experienced self-development through their travels because:", "their identity was redefined when they were away from home.", "Victorian women experienced self-development through travel because their sense of identity got reshaped once they were away from home."),
    ("American travel literature of the 1920s:", "celebrated the freedom that travel gives.", "1920s American travel literature centered on celebrating the sense of freedom that travel brings."),
    ("According to the passage, Said’s book, ”Orientalism”:", "demonstrated how cultural imperialism was used to justify colonial domination.", "Said's \"Orientalism\" showed how travel-writing depictions of other cultures fed into and justified colonial domination through cultural imperialism."),
    ("The author has differing views from Bregman regarding:", "a civilised society being coercive and unjust.", "The author pushes back on Bregman's claim that civilised society is inherently coercive and unjust."),
    ("According to the passage, the ”collapse of civilisations” is viewed by Bregman as:", "a time that enables changes in societies and cultures.", "Bregman sees the collapse of civilisations not as decline but as an opening that lets societies and cultures change and renew themselves."),
    ("None of the following views is expressed in the passage EXCEPT that:", "most people agree with Hobbes’ pessimistic view of human nature as being intrinsically untrustworthy and selfish.", "The passage states that most people do agree with Hobbes' bleak view of human nature as selfish and untrustworthy - every other option contradicts what the passage actually says."),
    ("According to the author, the main reason why Bregman contrasts life in pre-agricultural societies with agricultural societies is to:", "bolster his argument that people are basically decent, but progress as we know it can make them selfish.", "Bregman contrasts pre-agricultural and agricultural societies to argue that people are naturally decent, but that the kind of progress agriculture brought can make people selfish."),
    ("Which of the following statements about the negative effects of screen time is the author least likely to endorse?", "It increases human contact as it fills an isolation void.", "The author would be unlikely to agree that screen time increases human contact - the passage argues the opposite, that it fills an isolation void rather than real human connection."),
    ("The statement ”The richer you are, the more you spend to be off-screen” is supported by which other line from the passage?", "”How comfortable someone is with human engagement could be a new class marker.”", "The line about human engagement becoming \"a new class marker\" directly supports the idea that wealthier people pay more to stay off-screen."),
    ("The author is least likely to agree with the view that the increase in screen-time is fuelled by the fact that:", "with falling costs, people are streaming more content on their devices.", "The author would be least likely to attribute rising screen time simply to falling costs letting people stream more content - the passage frames the rise in screen time around isolation and surveillance, not economics."),
    ("The author claims that Silicon Valley tech companies have tried to ”confuse the public” by:", "promoting screen time in public schools while opting for a screen-free education for their own children.", "Tech companies pushed screen-based learning in public schools while choosing screen-free education for their own kids - a contradiction the author calls out as confusing the public."),
    ("Which one of the following, if false, could be seen as supporting the author’s claims?", "The economic crisis was not a failure of collective action to rectify economic problems.", "If it turned out the economic crisis wasn't actually a failure of collective action, that would undercut the author's own argument - so its falseness would actually support the author's claims."),
    ("Which one of the following, if true, would be an accurate inference from the first sentence of the passage?", "The author’s preoccupation with the economic crisis is not less than two years old.", "Since the passage opens by saying the author has followed the crisis for \"more than two years,\" it's fair to infer this preoccupation is at least two years old."),
    ("Which one of the following best captures the main argument of the last paragraph of the passage?", "The ideology of individualism must be set aside in order to deal with the crisis.", "The passage's closing argument is that the ideology of individualism needs to be set aside so society can respond collectively to the crisis."),
    ("All of the following, if true, could be seen as supporting the arguments in the passage, EXCEPT:", "The failure of economic systems does not necessarily mean the failure of their ideologies.", "The passage links the crisis to failures in prevailing economic ideologies - so the claim that an economic system's failure doesn't imply its ideology failed runs counter to the passage's argument."),
    ("According to the passage, the author is likely to be supportive of which one of the following programmes?", "An educational curriculum that promotes developing financial literacy in the masses.", "The author would likely support a programme aimed at improving financial literacy among ordinary people, since the passage laments how little the public understands about finance."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage. Brown et al. (2001) suggest that ’metabolic theory may provide a conceptual foundation for much of ecology just as genetic theory provides a foundation for much of evolutionary biology’. One of the successes of genetic theory is the diversity of theoretical approaches and models that have been developed and applied. A Web of Science (v. 5.9. Thomson Reuters) search on genetic + theor + evol identifies more than 12000 publications between 2005 and 2012. Considering only the 10 most-cited papers within this 12000 publication set, genetic theory can be seen to focus on genome dynamics, phylogenetic inference, game theory and the regulation of gene expression. There is no one fundamental genetic equation,\n\nbut rather a wide array of genetic models, ranging from simple to complex, with differing inputs and outputs, and divergent areas of application, loosely connected to each other through the shared conceptual foundation of heritable variation.", "Genetic theory has a wide range of theoretical approaches and applications and is foundational to evolutionary biology and Metabolic theory has the potential to do the same for ecology.", "Genetic theory has broad models and applications and underpins evolutionary biology, and the passage argues Metabolic theory could do something similar for ecology."),
    ("The four sentences (labelled A, B, C, D) below, when properly sequenced would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "DABC", "D, A, B, C - starting with the Chicago-school consumer welfare standard (D), explaining its conservative, markets-trusting approach (A), noting how big tech grew unchecked under it (B), and ending with the case for new rules against today's tech giants (C)."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage. Aesthetic political representation urges us to realize that ’the representative has autonomy with regard to the people represented’ but autonomy then is not an excuse to abandon one’s responsibility. Aesthetic autonomy requires cultivation of ’disinterestedness’ on the part of actors which is not indifference. To have disinterestedness, that is, to have comportment towards the beautiful that is devoid of all ulterior references to use - requires a kind of aesthetic commitment; it is the liberation of ourselves for the release of what has proper worth only in itself.", "Aesthetic political representation advocates autonomy for the representatives drawing from disinterestedness, which itself is different from indifference.", "Aesthetic political representation gives representatives autonomy rooted in disinterestedness - which is a meaningful, engaged stance, not mere indifference."),
    ("The four sentences (labelled A, B, C, D) below, when properly sequenced would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "CADB", "C, A, D, B - introducing the seven Shichi Fukujin deities (C), noting each personifies a different kind of fortune (A), pointing out only two are originally Japanese (D), and closing with the rest being borrowed from other traditions (B)."),
    ("Five jumbled up sentences, related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd one out and key in the number of the sentence as your answer:", "The makeover-centric media sets out subtly and not-so-subtly, ’good’ and ’bad’ ways to be a woman, layering these over inequalities of race and class.", "The media sets out implicit and explicit rules for how a woman should look and behave, layering those judgments on top of existing race and class inequalities."),
    ("The passage given below is followed by four alternate summaries. Choose the option that best captures the essence of the passage.\n\nThe dominant hypotheses in modern science believe that language evolved to allow humans to exchange factual information about the physical world. But an alternative view is that language evolved, in modern humans at least, to facilitate social bonding. It increased our ancestors’ chances of survival by enabling them to hunt more successfully or to cooperate more extensively. Language meant that things could be explained and that plans and past experiences could be shared efficiently.", "Most believe that language originated from a need to articulate facts, but others think it emerged from the need to promote social cohesion and cooperation, thus enabling human survival.", "Most believe language began as a way to state facts, but some now think it arose instead to build social cohesion and help humans survive together."),
    ("The four sentences (labelled A, B, C, D) below, when properly sequenced would yield a coherent paragraph. Decide on the proper sequencing of the order of the sentences and key in the sequence of the four numbers as your answer:", "BCDA", "B, C, D, A - opening with echolocation in bats as an example of exaptation (B), explaining the Russian-doll structural view of organisms (C), applying it to the central nervous system (D), and giving a concrete CNS example (A)."),
    ("Five jumbled up sentences, related to a topic, are given below. Four of them can be put together to form a coherent paragraph. Identify the odd one out and key in the number of the sentence as your answer:", "The current automatic detection models miss out on something vital: context.", "The odd one out is the sentence about automatic detection models missing \"something vital: context\" - it's a general critique, while the rest describe specific ways machine-learning hate-speech detection goes wrong."),
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
