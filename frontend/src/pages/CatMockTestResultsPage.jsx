import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getMockTestResults } from '../api/catMockTestApi'

const SECTION_ORDER = ['VARC', 'DILR', 'QA']

function SectionBar({ correct, wrong, skipped }) {
  const total = correct + wrong + skipped || 1
  return (
    <div className="score-bar">
      <div className="score-bar-segment score-bar-correct" style={{ width: `${(correct / total) * 100}%` }} />
      <div className="score-bar-segment score-bar-wrong" style={{ width: `${(wrong / total) * 100}%` }} />
      <div className="score-bar-segment score-bar-skipped" style={{ width: `${(skipped / total) * 100}%` }} />
    </div>
  )
}

function QuestionReview({ question }) {
  const [expanded, setExpanded] = useState(false)
  const isCorrect = question.is_correct

  return (
    <div className={`card question-review ${isCorrect ? 'question-correct' : 'question-incorrect'}`}>
      <button type="button" className="question-review-toggle" onClick={() => setExpanded((e) => !e)}>
        <span className={`badge ${isCorrect ? 'badge-success' : 'badge-error'}`}>
          {isCorrect ? 'Correct' : 'Incorrect'}
        </span>
        <span className="question-review-text">{question.question_text}</span>
        <span className="expand-icon">{expanded ? '−' : '+'}</span>
      </button>

      {expanded && (
        <div className="question-review-body">
          {Array.isArray(question.options) && question.options.length > 0 && (
            <ul className="options-list-static">
              {question.options.map((option, idx) => {
                const isUserAnswer = option === question.selected_answer
                const isCorrectAnswer = option === question.correct_answer
                let cls = ''
                if (isCorrectAnswer) cls = 'option-correct'
                else if (isUserAnswer) cls = 'option-wrong'
                return (
                  <li key={idx} className={cls}>
                    {option}
                    {isCorrectAnswer && <span className="tag"> Correct answer</span>}
                    {isUserAnswer && !isCorrectAnswer && <span className="tag"> Your answer</span>}
                  </li>
                )
              })}
            </ul>
          )}
          {(!question.options || question.options.length === 0) && (
            <p>
              <strong>Your answer:</strong> {question.selected_answer || '—'}
              <br />
              <strong>Correct answer:</strong> {question.correct_answer}
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

  const sectionKeys = SECTION_ORDER.filter((s) => results.sections?.[s])

  return (
    <div className="page-container">
      <h1>Your results</h1>

      <div className="results-summary card">
        <div>
          <div className="stat-value">{results.raw_score}</div>
          <div className="stat-label">Raw score</div>
        </div>
        <div>
          <div className="stat-value">{results.percentile_estimate}</div>
          <div className="stat-label">Percentile estimate</div>
        </div>
      </div>

      {sectionKeys.map((section) => {
        const sectionResult = results.sections[section]
        return (
          <div key={section} className="card section-result">
            <h2>{section}</h2>
            <div className="section-result-stats">
              <span className="tag tag-correct">{sectionResult.correct} correct</span>
              <span className="tag tag-wrong">{sectionResult.wrong} wrong</span>
              <span className="tag tag-skipped">{sectionResult.skipped} skipped</span>
            </div>
            <SectionBar
              correct={sectionResult.correct}
              wrong={sectionResult.wrong}
              skipped={sectionResult.skipped}
            />

            <div className="question-review-list">
              {sectionResult.questions?.map((q) => (
                <QuestionReview key={q.id} question={q} />
              ))}
            </div>
          </div>
        )
      })}
    </div>
  )
}
