"""Backfill explanation for CAT 2021 VARC Slot 2 (correct_answer was already
resolved correctly by pyq_varc_parser_legacy.py at load time - this only adds
the explanation field, rewritten in plain language from the solutions PDF,
not copied verbatim). Matched against already-loaded rows by (source_year,
source_slot, section, question_text).

Q24 is skipped - its printed answer value did not resolve to anything usable.

Run with:
    python -m app.scripts.backfill_varc_2021_slot2_answers
"""

from app.database.database import SessionLocal
from app.models.cat_question import CatQuestion

SOURCE_YEAR = 2021
SOURCE_SLOT = "slot2"

ANSWERS = [
    ("The central theme of the passage is about the choice between:", "attaining social cohesion and propagating objective truth.", "The passage centers on the tension between sticking to objective truth and using unifying fiction to hold societies together - the central choice it explores."),
    ("Regarding which one of the following quotes could we argue that the author overempha- sises the importance of fiction?", "”Hence sticking with the truth is the best strategy for gaining power. Unfortunately, this is just a comforting myth.”", "By calling the idea that \"truth is the best strategy for gaining power\" a mere \"comforting myth,\" the author signals a strong lean toward fiction's power over truth - supporting the claim that fiction is overemphasized."),
    ("The author would support none of the following statements about political power EXCEPT that:", "there are definite advantages to promoting fiction, but there needs to be some limit to a pervasive belief in myths.", "The passage does see real advantages in promoting unifying fiction, but it doesn't suggest that belief in myths should go unchecked - there has to be some limit."),
    ("The author implies that, like scholars, successful leaders:", "know how to balance truth and social unity.", "Just as scholars must weigh serving the truth against preserving social harmony, the author implies successful leaders also need to strike that same balance."),
    ("From the passage, we can infer that the author is in favour of:", "greater multilingualism.", "The author contrasts multilingualism's benefits against the risks of cultural homogenization, favoring a more linguistically connected, multilingual world."),
    ("The author mentions the Welsh language to show that:", "languages can revive even after their speakers have gone through a ”language shift”.", "Welsh's revival after being stigmatized shows that a language can bounce back even after its speakers had shifted away from it."),
    ("The author lists all of the following as reasons for the decline or disappearance of a lan- guage EXCEPT:", "the focus on only a few languages as a result of widespread internet use.", "The passage attributes language decline to things like government policy, catastrophic events, and people switching languages for work or study - but never blames the internet for narrowing language use."),
    ("We can infer all of the following about indigenous languages from the passage EXCEPT that:", "their vocabulary and grammatical constructs have been challenging to document.", "The passage treats indigenous languages as fragile repositories of cultural knowledge worth documenting, but never claims their vocabulary and grammar have been especially hard to document."),
    ("Which one of the following explains the ”contradictory pulls” on Indian nationalism?", "Despite its fight against colonial domination, Indian nationalism had to borrow from the coloniser in the material sphere.", "Indian nationalism fought colonial rule politically while still having to adopt the coloniser's material/organizational techniques - that tension is the \"contradictory pull.\""),
    ("Which one of the following best describes the liberal perception of Indian nationalism?", "Indian nationalist discourses reaffirmed traditional gender roles for Indian women.", "Liberals read Indian nationalism's conservatism as reinforcing traditional gender roles for women, rather than seeing it as a selective, strategic borrowing from the West."),
    ("Which one of the following, if true, would weaken the author’s claims in the passage?", "The colonial period saw the hybridisation of Indian culture in all realms as it came in contact with British/European culture.", "If Indian culture had actually hybridized completely with British/European culture across every sphere during the colonial period, that would undercut the author's claim that nationalism selectively preserved its own spiritual core."),
    ("On the basis of the information in the passage, all of the following are true about the spiritual/material dichotomy of Indian nationalism EXCEPT that it:", "was not as ideologically powerful as the inner/outer dichotomy.", "The passage treats the spiritual/material dichotomy as every bit as ideologically powerful as the inner/outer split, tightly linked to it - not weaker."),
    ("”. . . we cannot catch a glimpse of things-in-themselves around the corner of our own eyes; we cannot form an idea of reality that floats above the processes of our conceiving it . . .” Which one of the following statements best reflects the argument being made in this sentence?", "If the reality of things is independent of our perception, logically we cannot perceive that reality.", "The line implies that if reality truly exists independent of how we perceive it, we have no way to directly access or verify that reality at all."),
    ("The author of the passage is most likely to support which one of the following statements?", "The scandal of philosophy is that we might not know anything at all about reality if we think of reality as independent of our perceptions, ideas or descriptions.", "The author's \"scandal of philosophy\" is precisely the worry that if reality is independent of our perceptions and ideas, we can't be sure we know anything real about it."),
    ("According to the last paragraph of the passage, ”We hold our beliefs and presumptive knowledges more or less confidently, usually depending on” something. Which one of the following most broadly captures what we depend on?", "All of the options listed here.", "The passage lists multiple factors shaping how confidently we hold a belief (how we got it, what's at stake, what resources back it up) - all of which apply together, not just one."),
    ("The author discusses all of the following arguments in the passage, EXCEPT:", "if we cannot distinguish knowledge from opinion or delusion, we will not be able to justify our actions.", "The passage covers the sceptical \"scandal\" of knowledge and the general public's dismissal of epistemic worries, but doesn't argue that failing to separate knowledge from opinion would stop us from justifying our actions."),
    ("Four sentences that are a part of the paragraph are given below; the sentences may or may not be in the right order; create the sequence that forms a coherent paragraph.", "1, 2, 4, 3", "1, 2, 4, 3 - starting with the US's position on the Northwest Passage as an international strait, then the historical context of Canada's territorial claim, followed by the next stage of the dispute, and closing with its resolution."),
    ("Four sentences that are a part of the paragraph are given below; the sentences may or may not be in the right order; create the sequence that forms a coherent paragraph.", "4, 2, 1, 3", "4, 2, 1, 3 - opening with the historical vision behind development that's since been overshadowed, then describing the present moment, followed by elaboration, and closing with the broader implication."),
    ("Directions for Summary: A paragraph is followed by four options which have summa- rized the passage in their own way. Pick the option that best summarizes the passage:\n\nThe unlikely alliance of the incumbent industrialist and the distressed unemployed worker is especially powerful amid the debris of corporate bankruptcies and layoffs. In an economic downturn, the capitalist is more likely to focus on costs of the competition emanating from free markets than on the opportunities they create. And the unemployed worker will find many others in a similar condition and with anxieties similar to his, which will make it easier for them to organize together. Using the cover and the political organization provided by the distressed, the capitalist captures the political agenda.", "In an economic downturn, the capitalists use the anxieties of the unemployed and their political organisation to set the political agenda to suit their economic interests.", "The passage's core idea is that in an economic downturn, capitalists exploit the unemployed's anxieties and political organization to shape the political agenda in their own economic favor."),
    ("Directions for sentence exclusion: Five sentences are given below; out of these, four come together to form a coherent paragraph, but one sentence does not fit into the sequence. Choose the sentence that does not fit into the sequence.", "The care with which philosophers examine arguments for and against forms of biotech- nology makes this an excellent primer on formulating and assessing moral arguments.", "The sentence praising the book as \"an excellent primer\" for examining biotech arguments reads as an outside evaluative comment, not a sentence that belongs inside the flowing argument of the other four."),
    ("Directions for Summary: A paragraph is followed by four options which have summa- rized the passage in their own way. Pick the option that best summarizes the passage:\n\nCreativity is now viewed as the engine of economic progress. Various organizations are devoted to its study and promotion; there are encyclopedias and handbooks surveying creativ- ity research. But this proliferating success has tended to erode creativity’s stable identity: it has become so invested with value that it has become impossible to police its meaning and the practices that supposedly identify and encourage it. Many people and organizations commit- ted to producing original thoughts now feel that undue obsession with the idea of creativity gets in the way of real creativity.", "The value assigned to creativity today has assumed such proportions that the concept itself has lost its real meaning and this is hampering the engendering of real creativity.", "The passage's point is that creativity has been so inflated in value that the word has lost real meaning - ironically making it harder to nurture genuine creativity."),
    ("Directions for Summary: A paragraph is followed by four options which have summa- rized the passage in their own way. Pick the option that best summarizes the passage:\n\nBiologists who publish their research directly to the Web have been labelled as ”rogue”, but physicists have been routinely publishing research digitally (”preprints”), prior to submitting in a peer-reviewed journal. Advocates of preprints argue that quick and open dissemination\n\nof research speeds up scientific progress and allows for wider access to knowledge. But some journals still don’t accept research previously published as a preprint. Even if the idea of preprints is gaining ground, one of the biggest barriers for biologists is how they would be viewed by members of their conservative research community.", "Compared to biologists, physicists are less conservative in their acceptance of digital pre- publication of research papers, which allows for faster dissemination of knowledge.", "The passage contrasts how readily physicists embrace pre-publication of research (speeding up how fast knowledge spreads) against biologists' more cautious, conservative stance."),
    ("Directions for sentence exclusion: Five sentences are given below; out of these, four come together to form a coherent paragraph, but one sentence does not fit into the sequence. Choose the sentence that does not fit into the sequence:", "It has taken on a warm, fuzzy glow in the advertising world, where its potential is being widely discussed, and it is being claimed as the undeniable wave of the future.", "The sentence describing neuromarketing's \"warm, fuzzy glow\" in advertising stands apart from the other sentences, which take a more skeptical, scientific tone toward the topic."),
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
