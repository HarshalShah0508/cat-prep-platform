import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getPiSessionResults, submitPiSessionFeedback } from '../api/catPiApi'
import SessionFeedbackForm from '../components/pi/SessionFeedbackForm'

export default function CatPiResultsPage() {
  const { sessionId } = useParams()

  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getPiSessionResults(sessionId)
      .then(setResults)
      .catch((err) => setError(err?.response?.data?.detail || 'Could not load session results.'))
      .finally(() => setLoading(false))
  }, [sessionId])

  async function handleFeedbackSubmit(payload) {
    await submitPiSessionFeedback(sessionId, payload)
    setResults((prev) => ({ ...prev, user_rating: payload.rating, user_feedback_text: payload.feedback_text }))
  }

  if (loading) return <div className="page-loading">Loading results...</div>

  if (error) {
    return (
      <div className="page-container">
        <div className="alert alert-error">{error}</div>
      </div>
    )
  }

  if (!results.is_finished) {
    return (
      <div className="page-container">
        <div className="card">
          <h2>Interview not finished yet</h2>
          <p className="text-muted">
            You haven't finished this PI session yet. Finish the remaining questions to see your results.
          </p>
          <div className="pi-modal-actions">
            <Link className="btn btn-secondary" to="/dashboard">
              Back to dashboard
            </Link>
            <Link className="btn btn-primary" to={`/pi/${sessionId}`}>
              Continue session
            </Link>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <h1>PI practice complete</h1>

      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-value">{results.average_score}/10</div>
          <div className="stat-label">Average score</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{results.questions_attempted}</div>
          <div className="stat-label">Questions attempted</div>
        </div>
      </div>

      <div className="card">
        <h2>Strong topics</h2>
        <div className="pi-topic-pills">
          {results.strong_topics.length === 0 ? (
            <span className="text-muted">None yet</span>
          ) : (
            results.strong_topics.map((topic) => (
              <span key={topic} className="tag tag-correct">
                {topic}
              </span>
            ))
          )}
        </div>
      </div>

      <div className="card">
        <h2>Weak topics</h2>
        <div className="pi-topic-pills">
          {results.weak_topics.length === 0 ? (
            <span className="text-muted">None yet</span>
          ) : (
            results.weak_topics.map((topic) => (
              <span key={topic} className="tag tag-wrong">
                {topic}
              </span>
            ))
          )}
        </div>
      </div>

      <div className="card">
        <h2>Skipped questions</h2>
        <div className="pi-topic-pills">
          {results.skipped_questions.length === 0 ? (
            <span className="text-muted">No questions were skipped.</span>
          ) : (
            results.skipped_questions.map((skipped) => (
              <span key={skipped.question_number} className="tag tag-skipped">
                Question {skipped.question_number} — {skipped.topic}
              </span>
            ))
          )}
        </div>
      </div>

      {results.user_rating ? (
        <div className="card">
          <p className="text-muted">Thanks for your feedback!</p>
        </div>
      ) : (
        <SessionFeedbackForm onSubmit={handleFeedbackSubmit} />
      )}

      <div className="pi-modal-actions">
        <Link className="btn btn-secondary" to="/dashboard">
          Back to dashboard
        </Link>
        <Link className="btn btn-primary" to="/pi/new">
          Start a new interview
        </Link>
      </div>
    </div>
  )
}
