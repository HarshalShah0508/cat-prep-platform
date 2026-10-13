import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getPiSessionResults, submitPiSessionFeedback } from '../api/catPiApi'
import SessionFeedbackForm from '../components/pi/SessionFeedbackForm'
import PageHeader from '../components/ui/PageHeader'
import Pill from '../components/ui/Pill'

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
        <div className="ui-card">
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
      <PageHeader
        eyebrow="PI results"
        title="PI practice complete"
        stats={[
          { value: `${results.average_score}/10`, label: 'Average score', accent: true },
          { value: results.questions_attempted, label: 'Questions attempted' },
        ]}
      />

      <div className="ui-card">
        <div className="ui-eyebrow">Strong topics</div>
        <div className="pi-topic-pills">
          {results.strong_topics.length === 0 ? (
            <span className="text-muted">None yet</span>
          ) : (
            results.strong_topics.map((topic) => <Pill key={topic} tone="positive">{topic}</Pill>)
          )}
        </div>
      </div>

      <div className="ui-card">
        <div className="ui-eyebrow">Weak topics</div>
        <div className="pi-topic-pills">
          {results.weak_topics.length === 0 ? (
            <span className="text-muted">None yet</span>
          ) : (
            results.weak_topics.map((topic) => <Pill key={topic} tone="critical">{topic}</Pill>)
          )}
        </div>
      </div>

      <div className="ui-card">
        <div className="ui-eyebrow">Skipped questions</div>
        <div className="pi-topic-pills">
          {results.skipped_questions.length === 0 ? (
            <span className="text-muted">No questions were skipped.</span>
          ) : (
            results.skipped_questions.map((skipped) => (
              <Pill key={skipped.question_number} tone="warning">
                Question {skipped.question_number} — {skipped.topic}
              </Pill>
            ))
          )}
        </div>
      </div>

      {results.user_rating ? (
        <div className="ui-card">
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
