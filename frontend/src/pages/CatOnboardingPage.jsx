import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { updateCatProfile } from '../api/catProfileApi'

const EXPERIENCE_BANDS = [
  { value: 'fresher', label: 'Fresher (no work experience)' },
  { value: '0_to_1', label: '0-1 years' },
  { value: '1_to_3', label: '1-3 years' },
  { value: '3_to_5', label: '3-5 years' },
  { value: '5_plus', label: '5+ years' },
]

const PERCENTILE_BANDS = [
  { value: 'below_90', label: 'Below 90', min: 0, max: 90 },
  { value: '90_to_95', label: '90-95', min: 90, max: 95 },
  { value: '95_to_99', label: '95-99', min: 95, max: 99 },
  { value: '99_plus', label: '99+', min: 99, max: 100 },
]

export default function CatOnboardingPage() {
  const navigate = useNavigate()
  const [academicBackground, setAcademicBackground] = useState('engineering')
  const [experienceBand, setExperienceBand] = useState('fresher')
  const [currentCompany, setCurrentCompany] = useState('')
  const [notWorking, setNotWorking] = useState(false)
  const [percentileBand, setPercentileBand] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  function handleNotWorkingChange(checked) {
    setNotWorking(checked)
    if (checked) setCurrentCompany('')
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    const band = PERCENTILE_BANDS.find((b) => b.value === percentileBand)
    if (!band) {
      setError('Please select a target percentile range.')
      return
    }

    setSubmitting(true)
    try {
      await updateCatProfile({
        cat_academic_background: academicBackground,
        cat_years_experience_band: experienceBand,
        cat_current_company: notWorking ? '' : currentCompany,
        cat_target_percentile_min: band.min,
        cat_target_percentile_max: band.max,
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
      <div className="ui-card onboarding-card">
        <div className="ui-eyebrow">Getting started</div>
        <h1>Tell us about your CAT prep</h1>
        <p className="text-muted">
          This helps us tailor mock tests, PI practice, and weak-concept tracking to you.
        </p>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <label htmlFor="academicBackground">
              <span className="ui-step-index">01</span>Academic background
            </label>
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
            <label htmlFor="experienceBand">
              <span className="ui-step-index">02</span>Years of experience
            </label>
            <select
              id="experienceBand"
              value={experienceBand}
              onChange={(e) => setExperienceBand(e.target.value)}
            >
              {EXPERIENCE_BANDS.map((band) => (
                <option key={band.value} value={band.value}>
                  {band.label}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="currentCompany">
              <span className="ui-step-index">03</span>Current company
            </label>
            <input
              id="currentCompany"
              type="text"
              value={currentCompany}
              onChange={(e) => setCurrentCompany(e.target.value)}
              disabled={notWorking}
              placeholder="e.g. TCS"
            />
            <label className="checkbox-item" style={{ marginTop: '0.5rem' }}>
              <input
                type="checkbox"
                checked={notWorking}
                onChange={(e) => handleNotWorkingChange(e.target.checked)}
              />
              <span>I'm a student / not currently working</span>
            </label>
          </div>

          <div className="form-group">
            <label>
              <span className="ui-step-index">04</span>Target percentile range
            </label>
            <div className="radio-group">
              {PERCENTILE_BANDS.map((band) => (
                <label key={band.value} className="radio-item">
                  <input
                    type="radio"
                    name="percentileBand"
                    value={band.value}
                    checked={percentileBand === band.value}
                    onChange={() => setPercentileBand(band.value)}
                  />
                  <span>{band.label}</span>
                </label>
              ))}
            </div>
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Saving...' : 'Save and continue'}
          </button>
        </form>
      </div>
    </div>
  )
}
