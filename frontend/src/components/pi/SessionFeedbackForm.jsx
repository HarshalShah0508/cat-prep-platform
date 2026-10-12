import { useState } from 'react'

const STARS = [1, 2, 3, 4, 5]

export default function SessionFeedbackForm({ onSubmit, onSkip }) {
  const [rating, setRating] = useState(0)
  const [hoverRating, setHoverRating] = useState(0)
  const [feedbackText, setFeedbackText] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (rating === 0) {
      setError('Please select a rating.')
      return
    }

    setError('')
    setSubmitting(true)
    try {
      await onSubmit({ rating, feedback_text: feedbackText.trim() || null })
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to submit feedback. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="card pi-feedback-form" onSubmit={handleSubmit}>
      <h2>Rate your experience</h2>

      <div className="pi-star-rating">
        {STARS.map((value) => (
          <button
            key={value}
            type="button"
            className={`pi-star ${value <= (hoverRating || rating) ? 'pi-star--filled' : ''}`}
            onMouseEnter={() => setHoverRating(value)}
            onMouseLeave={() => setHoverRating(0)}
            onClick={() => setRating(value)}
            aria-label={`Rate ${value} out of 5`}
          >
            ★
          </button>
        ))}
      </div>

      <div className="form-group">
        <label>Anything you'd like to share? (optional)</label>
        <textarea
          rows={3}
          value={feedbackText}
          onChange={(e) => setFeedbackText(e.target.value)}
          placeholder="What worked well, what didn't, what you'd like to see..."
        />
      </div>

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
