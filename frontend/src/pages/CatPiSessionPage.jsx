import { useEffect, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { startPiSession, getPiSession, answerPiQuestion, finishPiSession } from '../api/catPiApi'

export default function CatPiSessionPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()

  const [id, setId] = useState(sessionId || null)
  const [currentQuestion, setCurrentQuestion] = useState(null)
  const [currentQuestionId, setCurrentQuestionId] = useState(null)
  const [answerText, setAnswerText] = useState('')
  const [lastEvaluation, setLastEvaluation] = useState(null)
  const [finished, setFinished] = useState(false)
  const [finalResult, setFinalResult] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const startedRef = useRef(false)

  // No sessionId in the URL: start a brand-new PI session, then adopt its id.
  useEffect(() => {
    if (sessionId) {
      setLoading(true)
      getPiSession(sessionId)
        .then((data) => {
          setId(data.id)
          const answered = data.questions.filter((q) => q.answer)
          const unanswered = data.questions.find((q) => !q.answer)
          if (unanswered) {
            setCurrentQuestion({ id: unanswered.id, question_text: unanswered.question_text })
            setCurrentQuestionId(unanswered.id)
          } else if (answered.length > 0) {
            const last = answered[answered.length - 1]
            setLastEvaluation(last.answer)
            setCurrentQuestion(null)
          }
          if (data.status === 'completed' || data.status === 'finished') {
            setFinished(true)
          }
        })
        .catch((err) => {
          setError(err?.response?.data?.detail || 'Could not load this PI session.')
        })
        .finally(() => setLoading(false))
      return
    }

    if (startedRef.current) return
    startedRef.current = true

    setLoading(true)
    startPiSession()
      .then((data) => {
        setId(data.session_id)
        setCurrentQuestion(data.question)
        setCurrentQuestionId(data.question.id)
        navigate(`/pi/${data.session_id}`, { replace: true })
      })
      .catch((err) => {
        setError(err?.response?.data?.detail || 'Could not start a PI session.')
      })
      .finally(() => setLoading(false))
  }, [sessionId, navigate])

  async function handleSubmitAnswer(e) {
    e.preventDefault()
    if (!answerText.trim() || !id || !currentQuestionId) return

    setSubmitting(true)
    setError('')
    try {
      const data = await answerPiQuestion(id, {
        pi_session_question_id: currentQuestionId,
        answer_text: answerText,
      })
      setLastEvaluation(data.evaluation)
      setAnswerText('')
      if (data.next_question) {
        setCurrentQuestion(data.next_question)
        setCurrentQuestionId(data.next_question.id)
      } else {
        setCurrentQuestion(null)
        setCurrentQuestionId(null)
      }
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not submit your answer.')
    } finally {
      setSubmitting(false)
    }
  }

  async function handleFinish() {
    if (!id) return
    setSubmitting(true)
    setError('')
    try {
      const data = await finishPiSession(id)
      setFinalResult(data)
      setFinished(true)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not finish the session.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="page-loading">Loading PI practice...</div>

  if (error && !currentQuestion && !finished) {
    return (
      <div className="page-container">
        <div className="alert alert-error">{error}</div>
      </div>
    )
  }

  if (finished) {
    return (
      <div className="page-container">
        <div className="card">
          <h1>PI practice complete</h1>
          {finalResult ? (
            <>
              <div className="stat-value">{finalResult.overall_score}</div>
              <div className="stat-label">Overall score</div>
              <p className="feedback-text">{finalResult.feedback_text}</p>
            </>
          ) : (
            <p className="text-muted">This session has already been completed.</p>
          )}
        </div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <h1>AI Personal Interview Practice</h1>

      {error && <div className="alert alert-error">{error}</div>}

      {lastEvaluation && (
        <div className="card evaluation-card">
          <h2>Feedback on your last answer</h2>
          <div className="stat-value">{lastEvaluation.score}</div>
          <div className="stat-label">Score</div>
          <p>{lastEvaluation.feedback}</p>
          {Array.isArray(lastEvaluation.strengths) && lastEvaluation.strengths.length > 0 && (
            <div>
              <strong>Strengths</strong>
              <ul>
                {lastEvaluation.strengths.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
          {Array.isArray(lastEvaluation.improvements) && lastEvaluation.improvements.length > 0 && (
            <div>
              <strong>Areas to improve</strong>
              <ul>
                {lastEvaluation.improvements.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {currentQuestion ? (
        <div className="card">
          <h2>Question</h2>
          <p className="question-text">{currentQuestion.question_text}</p>
          <form onSubmit={handleSubmitAnswer}>
            <div className="form-group">
              <textarea
                rows={6}
                value={answerText}
                onChange={(e) => setAnswerText(e.target.value)}
                placeholder="Type your answer..."
              />
            </div>
            <button type="submit" className="btn btn-primary" disabled={submitting || !answerText.trim()}>
              {submitting ? 'Submitting...' : 'Submit answer'}
            </button>
          </form>
        </div>
      ) : (
        <div className="card">
          <p>No more questions queued.</p>
          <button type="button" className="btn btn-primary" onClick={handleFinish} disabled={submitting}>
            {submitting ? 'Finishing...' : 'Finish session'}
          </button>
        </div>
      )}
    </div>
  )
}
