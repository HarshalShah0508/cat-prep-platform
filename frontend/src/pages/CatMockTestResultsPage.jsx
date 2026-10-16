import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getMockTestResults, submitMockTestFeedback } from '../api/catMockTestApi'
import PageHeader from '../components/ui/PageHeader'
import Pill from '../components/ui/Pill'
import ListRow from '../components/ui/ListRow'
import SurveyForm from '../components/feedback/SurveyForm'

const MOCK_TEST_SURVEY_QUESTIONS = [
  {
    key: 'difficulty',
    type: 'radio',
    label: 'How did the difficulty feel compared to the real CAT exam?',
    required: true,
    options: [
      { value: 'too_easy', label: 'Too easy' },
      { value: 'about_right', label: 'About right' },
      { value: 'too_hard', label: 'Too hard' },
    ],
  },
  { key: 'usefulness_rating', type: 'rating', label: 'How useful was this test for your prep?', required: true },
  { key: 'issues_text', type: 'text', label: 'Any bugs or friction during the test?', required: false },
  { key: 'nps_rating', type: 'rating', label: 'How likely are you to recommend CATPrep to a friend?', required: true },
]

const SECTION_ORDER = ['VARC', 'DILR', 'QA']
const SLOT_LABELS = { slot1: 'Slot 1', slot2: 'Slot 2', slot3: 'Slot 3' }

function SectionBar({ correct, wrong, skipped, ungraded = 0 }) {
  const total = correct + wrong + skipped + ungraded || 1
  return (
    <div className="score-bar">
      <div className="score-bar-segment score-bar-correct" style={{ width: `${(correct / total) * 100}%` }} />
      <div className="score-bar-segment score-bar-wrong" style={{ width: `${(wrong / total) * 100}%` }} />
      <div className="score-bar-segment score-bar-skipped" style={{ width: `${(skipped / total) * 100}%` }} />
      <div className="score-bar-segment score-bar-ungraded" style={{ width: `${(ungraded / total) * 100}%` }} />
    </div>
  )
}

function QuestionReview({ question }) {
  const [expanded, setExpanded] = useState(false)
  // is_correct comes back null in two different cases that need different
  // labels: PYQs loaded before their answer key was transcribed (no
  // correct_answer at all), vs. a question with a real answer key that the
  // user simply never attempted (correct_answer exists, selected_answer
  // doesn't).
  const noAnswerKey = !question.correct_answer
  const notAttempted = !noAnswerKey && question.is_correct === null
  const ungraded = noAnswerKey || notAttempted
  const isCorrect = question.is_correct
  const pillTone = ungraded ? 'neutral' : isCorrect ? 'positive' : 'critical'
  const badgeText = noAnswerKey
    ? 'Answer key pending'
    : notAttempted
      ? 'Not attempted'
      : isCorrect
        ? 'Correct'
        : 'Incorrect'
  const cardClass = ungraded ? '' : isCorrect ? 'question-correct' : 'question-incorrect'

  return (
    <div className={`ui-card question-review ${cardClass}`}>
      <button type="button" className="question-review-toggle" onClick={() => setExpanded((e) => !e)}>
        <Pill tone={pillTone}>{badgeText}</Pill>
        <span className="question-review-text">{question.question_text}</span>
        <span className="expand-icon">{expanded ? '−' : '+'}</span>
      </button>

      {expanded && (
        <div className="question-review-body">
          {Array.isArray(question.options) && question.options.length > 0 && (
            <ul className="options-list-static">
              {question.options.map((option, idx) => {
                const isUserAnswer = option === question.selected_answer
                const isCorrectAnswer = !noAnswerKey && option === question.correct_answer
                let cls = ''
                if (isCorrectAnswer) cls = 'option-correct'
                else if (isUserAnswer) cls = 'option-wrong'
                return (
                  <li key={idx} className={cls}>
                    {option}
                    {isCorrectAnswer && <Pill tone="positive">Correct answer</Pill>}
                    {isUserAnswer && !isCorrectAnswer && <Pill tone="critical">Your answer</Pill>}
                  </li>
                )
              })}
            </ul>
          )}
          {(!question.options || question.options.length === 0) && (
            <p>
              <strong>Your answer:</strong> {question.selected_answer || '—'}
              <br />
              <strong>Correct answer:</strong> {noAnswerKey ? 'Pending' : question.correct_answer}
            </p>
          )}
          {question.explanation && (
            <p className="explanation">
              <strong>Explanation:</strong> {question.explanation}
            </p>
          )}
        </div>
      )}
    </div>
  )
}

export default function CatMockTestResultsPage() {
  const { sessionId } = useParams()
  const [results, setResults] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [surveySkipped, setSurveySkipped] = useState(false)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const data = await getMockTestResults(sessionId)
        if (!cancelled) setResults(data)
      } catch (err) {
        if (!cancelled) {
          setError(err?.response?.data?.detail || 'Could not load results.')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [sessionId])

  if (loading) return <div className="page-loading">Loading results...</div>
  if (error) {
    return (
      <div className="page-container">
        <div className="alert alert-error">{error}</div>
      </div>
    )
  }
  if (!results) return null

  // Backend returns section_breakdown (array of counts) and a flat questions
  // list (each carrying its own section) rather than a nested sections dict.
  const questionsBySection = {}
  for (const q of results.questions ?? []) {
    const key = q.section || 'UNKNOWN'
    if (!questionsBySection[key]) questionsBySection[key] = []
    questionsBySection[key].push(q)
  }

  const breakdownBySection = {}
  for (const b of results.section_breakdown ?? []) {
    breakdownBySection[b.section] = b
  }

  const sectionKeys = SECTION_ORDER.filter((s) => breakdownBySection[s])

  async function handleFeedbackSubmit(payload) {
    const saved = await submitMockTestFeedback(sessionId, payload)
    setResults((prev) => ({ ...prev, feedback: saved }))
  }

  return (
    <div className="page-container">
      <PageHeader
        eyebrow="Results"
        title="Your results"
        subtitle={
          results.test_type === 'pyq_paper'
            ? `CAT ${results.pyq_source_year} · ${SLOT_LABELS[results.pyq_source_slot] || results.pyq_source_slot}`
            : undefined
        }
        stats={[
          { value: results.raw_score, label: 'Raw score' },
          { value: results.percentile_estimate, label: 'Percentile estimate', accent: true },
        ]}
      />

      <div className="ui-card">
        <div className="ui-eyebrow">Topics to work on</div>
        {results.weak_topics && results.weak_topics.length > 0 ? (
          results.weak_topics.map((wt) => (
            <ListRow
              key={`${wt.section}-${wt.topic}`}
              title={wt.topic}
              meta={
                <>
                  <Pill tone="warning">{wt.section}</Pill>
                  <span>{wt.wrong_count} wrong this test</span>
                </>
              }
              actions={
                <Link className="btn btn-secondary btn-sm" to="/weak-concepts">
                  View &amp; practice
                </Link>
              }
            />
          ))
        ) : (
          <p className="text-muted">No major weak topics flagged from this test — nice work.</p>
        )}
      </div>

      {sectionKeys.map((section) => {
        const sectionResult = breakdownBySection[section]
        const sectionQuestions = questionsBySection[section] ?? []
        return (
          <div key={section} className="ui-card section-result">
            <h2>{section}</h2>
            <div className="section-result-stats">
              <Pill tone="positive">{sectionResult.correct} correct</Pill>
              <Pill tone="critical">{sectionResult.wrong} wrong</Pill>
              <Pill tone="warning">{sectionResult.skipped} skipped</Pill>
              {sectionResult.ungraded > 0 && (
                <Pill tone="neutral">{sectionResult.ungraded} answer key pending</Pill>
              )}
            </div>
            <SectionBar
              correct={sectionResult.correct}
              wrong={sectionResult.wrong}
              skipped={sectionResult.skipped}
              ungraded={sectionResult.ungraded}
            />

            <div className="question-review-list">
              {sectionQuestions.map((q) => (
                <QuestionReview key={q.id} question={q} />
              ))}
            </div>
          </div>
        )
      })}

      {results.feedback ? (
        <div className="ui-card">
          <p className="text-muted">Thanks for your feedback!</p>
        </div>
      ) : (
        !surveySkipped && (
          <SurveyForm
            title="Quick feedback"
            questions={MOCK_TEST_SURVEY_QUESTIONS}
            onSubmit={handleFeedbackSubmit}
            onSkip={() => setSurveySkipped(true)}
          />
        )
      )}

      <div className="pi-modal-actions">
        <Link className="btn btn-secondary" to="/dashboard">
          Back to dashboard
        </Link>
        <Link className="btn btn-primary" to="/mock-tests/new">
          Start a new mock test
        </Link>
      </div>
    </div>
  )
}
