import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { startMockTest } from '../api/catMockTestApi'
import { useCatMockTest } from '../context/CatMockTestContext'

const ALL_SECTIONS = ['VARC', 'DILR', 'QA']

export default function CatMockTestSetupPage() {
  const navigate = useNavigate()
  const { trackSession } = useCatMockTest()
  const [testType, setTestType] = useState('full_mock')
  const [sections, setSections] = useState(ALL_SECTIONS)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  function toggleSection(section) {
    setSections((prev) =>
      prev.includes(section) ? prev.filter((s) => s !== section) : [...prev, section],
    )
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    const chosenSections = testType === 'full_mock' ? ALL_SECTIONS : sections
    if (chosenSections.length === 0) {
      setError('Please select at least one section.')
      return
    }

    setSubmitting(true)
    try {
      const data = await startMockTest({ test_type: testType, sections: chosenSections })
      trackSession(data.session_id, data.status)
      navigate(`/mock-tests/${data.session_id}`)
    } catch (err) {
      const message =
        err?.response?.data?.detail || 'Could not start the mock test. Please try again.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="page-container">
      <div className="card">
        <h1>Start a mock test</h1>
        <p className="text-muted">Choose the format that matches what you want to practice.</p>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <label>Test type</label>
            <div className="radio-group">
              <label className="radio-item">
                <input
                  type="radio"
                  name="testType"
                  value="full_mock"
                  checked={testType === 'full_mock'}
                  onChange={() => setTestType('full_mock')}
                />
                <span>Full mock (all sections)</span>
              </label>
              <label className="radio-item">
                <input
                  type="radio"
                  name="testType"
                  value="sectional"
                  checked={testType === 'sectional'}
                  onChange={() => setTestType('sectional')}
                />
                <span>Sectional test</span>
              </label>
              <label className="radio-item">
                <input
                  type="radio"
                  name="testType"
                  value="topic_drill"
                  checked={testType === 'topic_drill'}
                  onChange={() => setTestType('topic_drill')}
                />
                <span>Topic drill</span>
              </label>
            </div>
          </div>

          {testType !== 'full_mock' && (
            <div className="form-group">
              <label>Sections</label>
              <div className="checkbox-grid">
                {ALL_SECTIONS.map((section) => (
                  <label key={section} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={sections.includes(section)}
                      onChange={() => toggleSection(section)}
                    />
                    <span>{section}</span>
                  </label>
                ))}
              </div>
            </div>
          )}

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Starting...' : 'Start test'}
          </button>
        </form>
      </div>
    </div>
  )
}
