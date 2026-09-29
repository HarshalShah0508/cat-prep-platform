import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { updateCatProfile } from '../api/catProfileApi'

const COMMON_IIMS = [
  'Ahmedabad',
  'Bangalore',
  'Calcutta',
  'Lucknow',
  'Kozhikode',
  'Indore',
  'Other',
]

export default function CatOnboardingPage() {
  const navigate = useNavigate()
  const [academicBackground, setAcademicBackground] = useState('engineering')
  const [selectedIims, setSelectedIims] = useState([])
  const [targetPercentile, setTargetPercentile] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  function toggleIim(iim) {
    setSelectedIims((prev) =>
      prev.includes(iim) ? prev.filter((item) => item !== iim) : [...prev, iim],
    )
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (selectedIims.length === 0) {
      setError('Please select at least one target IIM.')
      return
    }
    const percentileNum = Number(targetPercentile)
    if (!targetPercentile || Number.isNaN(percentileNum) || percentileNum <= 0 || percentileNum > 100) {
      setError('Please enter a valid target percentile between 0 and 100.')
      return
    }

    setSubmitting(true)
    try {
      await updateCatProfile({
        cat_academic_background: academicBackground,
        cat_target_iims: selectedIims,
        cat_target_percentile: percentileNum,
      })
      navigate('/dashboard')
    } catch (err) {
      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Could not save your profile. Please try again.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page-container">
      <div className="card onboarding-card">
        <h1>Tell us about your CAT prep</h1>
        <p className="text-muted">
          This helps us tailor mock tests, PI practice, and weak-concept tracking to you.
        </p>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <label htmlFor="academicBackground">Academic background</label>
            <select
              id="academicBackground"
              value={academicBackground}
              onChange={(e) => setAcademicBackground(e.target.value)}
            >
              <option value="engineering">Engineering</option>
              <option value="commerce">Commerce</option>
              <option value="humanities">Humanities</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div className="form-group">
            <label>Target IIMs</label>
            <div className="checkbox-grid">
              {COMMON_IIMS.map((iim) => (
                <label key={iim} className="checkbox-item">
                  <input
                    type="checkbox"
                    checked={selectedIims.includes(iim)}
                    onChange={() => toggleIim(iim)}
                  />
                  <span>IIM {iim}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="targetPercentile">Target percentile</label>
            <input
              id="targetPercentile"
              type="number"
              min="0"
              max="100"
              step="0.1"
              value={targetPercentile}
              onChange={(e) => setTargetPercentile(e.target.value)}
              placeholder="e.g. 99.5"
            />
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Saving...' : 'Save and continue'}
          </button>
        </form>
      </div>
    </div>
  )
}
