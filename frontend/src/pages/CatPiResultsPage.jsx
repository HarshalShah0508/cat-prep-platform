import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getPiSessionResults, submitPiSurvey } from '../api/catPiApi'
import PageHeader from '../components/ui/PageHeader'
import Pill from '../components/ui/Pill'
import SurveyForm from '../components/feedback/SurveyForm'

const PI_SURVEY_QUESTIONS = [
  {
    key: 'realism_rating',
    type: 'rating',
    label: 'How realistic did this feel compared to a real IIM panel interview?',
    required: true,
  },
  {
    key: 'relevance_rating',
    type: 'rating',
    label: 'How relevant were the questions to your background/profile?',
    required: true,
  },
  {
    key: 'issues_text',
    type: 'text',
    label: 'Any issues with voice input, camera, or delivery coaching?',
    required: false,
  },
  { key: 'nps_rating', type: 'rating', label: 'How likely are you to recommend CATPrep to a friend?', required: true },
]

export default function CatPiResultsPage() {
  const { sessionId } = useParams()

  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [surveySkipped, setSurveySkipped] = useState(false)

  useEffect(() => {
    getPiSessionResults(sessionId)
      .then(setResults)
      .catch((err) => setError(err?.response?.data?.detail || 'Could not load session results.'))
      .finally(() => setLoading(false))
  }, [sessionId])

  async function handleSurveySubmit(payload) {
    const saved = await submitPiSurvey(sessionId, payload)
    setResults((prev) => ({ ...prev, survey: saved }))
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

      {results.survey ? (
        <div className="ui-card">
          <p className="text-muted">Thanks for your feedback!</p>
        </div>
      ) : (
        !surveySkipped && (
          <SurveyForm
            title="Quick feedback"
            questions={PI_SURVEY_QUESTIONS}
            onSubmit={handleSurveySubmit}
            onSkip={() => setSurveySkipped(true)}
          />
        )
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
