import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { startMockTest } from '../api/catMockTestApi'
import { getAvailablePyqPapers } from '../api/catPyqApi'
import { useCatMockTest } from '../context/CatMockTestContext'

const ALL_SECTIONS = ['VARC', 'DILR', 'QA']
const SLOT_LABELS = { slot1: 'Slot 1', slot2: 'Slot 2', slot3: 'Slot 3' }

export default function CatMockTestSetupPage() {
  const navigate = useNavigate()
  const { trackSession } = useCatMockTest()
  const [testType, setTestType] = useState('full_mock')
  const [sections, setSections] = useState(ALL_SECTIONS)
  const [questionSource, setQuestionSource] = useState('mixed')
  const [papers, setPapers] = useState([])
  const [pyqYear, setPyqYear] = useState('any')
  const [pyqSlot, setPyqSlot] = useState('any')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    getAvailablePyqPapers()
      .then(setPapers)
      .catch(() => {
        // Non-fatal: the year/slot picker just won't have options to offer.
      })
  }, [])

  const years = useMemo(
    () => [...new Set(papers.map((p) => p.source_year))].sort((a, b) => b - a),
    [papers],
  )
  const slotsForYear = useMemo(
    () =>
      pyqYear === 'any'
        ? []
        : [...new Set(papers.filter((p) => p.source_year === Number(pyqYear)).map((p) => p.source_slot))].sort(),
    [papers, pyqYear],
  )

  const showPyqFilter = questionSource === 'pyq_only'

  function toggleSection(section) {
    setSections((prev) =>
      prev.includes(section) ? prev.filter((s) => s !== section) : [...prev, section],
    )
  }

  function handleYearChange(value) {
    setPyqYear(value)
    setPyqSlot('any')
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
      const data = await startMockTest({
        test_type: testType,
        sections: chosenSections,
        question_source: questionSource,
        pyq_source_year: showPyqFilter && pyqYear !== 'any' ? Number(pyqYear) : undefined,
        pyq_source_slot: showPyqFilter && pyqSlot !== 'any' ? pyqSlot : undefined,
      })
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

          <div className="form-group">
            <label>Question source</label>
            <div className="radio-group">
              <label className="radio-item">
                <input
                  type="radio"
                  name="questionSource"
                  value="mixed"
                  checked={questionSource === 'mixed'}
                  onChange={() => setQuestionSource('mixed')}
                />
                <span>Mixed - PYQs + new AI-generated (Recommended)</span>
              </label>
              <label className="radio-item">
                <input
                  type="radio"
                  name="questionSource"
                  value="pyq_only"
                  checked={questionSource === 'pyq_only'}
                  onChange={() => setQuestionSource('pyq_only')}
                />
                <span>PYQs only</span>
              </label>
              <label className="radio-item">
                <input
                  type="radio"
                  name="questionSource"
                  value="ai_only"
                  checked={questionSource === 'ai_only'}
                  onChange={() => setQuestionSource('ai_only')}
                />
                <span>New questions only (AI-generated)</span>
              </label>
            </div>
            <p className="text-muted">
              Want a specific past paper instead of a shuffled mix? Try{' '}
              <Link to="/pyq-tests">PYQ Practice</Link>.
            </p>
          </div>

          {showPyqFilter && (
            <div className="form-group">
              <label>PYQ year &amp; slot (optional)</label>
              <div className="form-row">
                <select
                  value={pyqYear}
                  onChange={(e) => handleYearChange(e.target.value)}
                  className="select-input"
                >
                  <option value="any">Any year</option>
                  {years.map((year) => (
                    <option key={year} value={year}>
                      {year}
                    </option>
                  ))}
                </select>
                <select
                  value={pyqSlot}
                  onChange={(e) => setPyqSlot(e.target.value)}
                  disabled={pyqYear === 'any'}
                  className="select-input"
                >
                  <option value="any">Any slot</option>
                  {slotsForYear.map((slot) => (
                    <option key={slot} value={slot}>
                      {SLOT_LABELS[slot] || slot}
                    </option>
                  ))}
                </select>
              </div>
              <p className="text-muted">
                Narrows the PYQ portion of this test to one real paper instead of
                sampling across every year. Leave on "Any" to pull from the whole bank.
              </p>
            </div>
          )}

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
