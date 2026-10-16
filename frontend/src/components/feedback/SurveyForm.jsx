import { useState } from 'react'

const STARS = [1, 2, 3, 4, 5]

function RatingQuestion({ question, value, hoverValue, onHover, onPick }) {
  return (
    <div className="form-group">
      <label>{question.label}</label>
      <div className="pi-star-rating">
        {STARS.map((star) => (
          <button
            key={star}
            type="button"
            className={`pi-star ${star <= (hoverValue || value || 0) ? 'pi-star--filled' : ''}`}
            onMouseEnter={() => onHover(star)}
            onMouseLeave={() => onHover(0)}
            onClick={() => onPick(star)}
            aria-label={`Rate ${star} out of 5`}
          >
            ★
          </button>
        ))}
      </div>
    </div>
  )
}

function RadioQuestion({ question, value, onPick }) {
  return (
    <div className="form-group">
      <label>{question.label}</label>
      <div className="radio-group">
        {question.options.map((opt) => (
          <label key={opt.value} className="radio-item">
            <input
              type="radio"
              name={question.key}
              value={opt.value}
              checked={value === opt.value}
              onChange={() => onPick(opt.value)}
            />
            <span>{opt.label}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

function TextQuestion({ question, value, onChange }) {
  return (
    <div className="form-group">
      <label>
        {question.label} {!question.required && <span className="text-muted">(optional)</span>}
      </label>
      <textarea rows={3} value={value || ''} onChange={(e) => onChange(e.target.value)} />
    </div>
  )
}

export default function SurveyForm({ title, questions, onSubmit, onSkip }) {
  const [answers, setAnswers] = useState({})
  const [hovers, setHovers] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  function setAnswer(key, value) {
    setAnswers((prev) => ({ ...prev, [key]: value }))
  }

  function setHover(key, value) {
    setHovers((prev) => ({ ...prev, [key]: value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    const missing = questions.find((q) => q.required && !answers[q.key])
    if (missing) {
      setError('Please answer all required questions.')
      return
    }

    setError('')
    setSubmitting(true)
    try {
      const payload = {}
      questions.forEach((q) => {
        payload[q.key] = q.type === 'text' ? (answers[q.key]?.trim() || null) : answers[q.key]
      })
      await onSubmit(payload)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not submit feedback. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="card pi-feedback-form" onSubmit={handleSubmit}>
      <h2>{title}</h2>

      {questions.map((q) => {
        if (q.type === 'rating') {
          return (
            <RatingQuestion
              key={q.key}
              question={q}
              value={answers[q.key]}
              hoverValue={hovers[q.key] || 0}
              onHover={(v) => setHover(q.key, v)}
              onPick={(v) => setAnswer(q.key, v)}
            />
          )
        }
        if (q.type === 'radio') {
          return (
            <RadioQuestion key={q.key} question={q} value={answers[q.key]} onPick={(v) => setAnswer(q.key, v)} />
          )
        }
        return (
          <TextQuestion key={q.key} question={q} value={answers[q.key]} onChange={(v) => setAnswer(q.key, v)} />
        )
      })}

      {error && <div className="alert alert-error">{error}</div>}

      <div className="pi-modal-actions">
        <button type="submit" className="btn btn-primary" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit feedback'}
        </button>
        {onSkip && (
          <button type="button" className="btn btn-secondary" onClick={onSkip} disabled={submitting}>
            Skip
          </button>
        )}
      </div>
    </form>
  )
}
