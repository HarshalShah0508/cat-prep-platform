import { useEffect, useMemo, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { startMockTest, getTopicOptions } from '../api/catMockTestApi'
import { getAvailablePyqPapers } from '../api/catPyqApi'
import { useCatMockTest } from '../context/CatMockTestContext'
import PageHeader from '../components/ui/PageHeader'

const ALL_SECTIONS = ['VARC', 'DILR', 'QA']
const SLOT_LABELS = { slot1: 'Slot 1', slot2: 'Slot 2', slot3: 'Slot 3' }
const QUESTION_COUNT_OPTIONS = [10, 16, 22]
const DRILL_SECTIONS = ['QA', 'VARC', 'DILR']

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

  const [drillSection, setDrillSection] = useState('QA')
  const [topicGroups, setTopicGroups] = useState({})
  const [topicMode, setTopicMode] = useState('topic_wise')
  const [expandedCategories, setExpandedCategories] = useState([])
  const [selectedTopicsByCategory, setSelectedTopicsByCategory] = useState({})
  const [questionStyle, setQuestionStyle] = useState('challenging')
  const [questionCount, setQuestionCount] = useState(22)

  useEffect(() => {
    getAvailablePyqPapers()
      .then(setPapers)
      .catch(() => {
        // Non-fatal: the year/slot picker just won't have options to offer.
      })
  }, [])

  useEffect(() => {
    if (testType !== 'topic_drill') return
    getTopicOptions(drillSection)
      .then(setTopicGroups)
      .catch(() => {
        // Non-fatal: the topic picker just won't have options to offer.
      })
    // Switching section invalidates any topics picked for the previous section.
    setExpandedCategories([])
    setSelectedTopicsByCategory({})
  }, [testType, drillSection])

  function toggleCategory(category) {
    setExpandedCategories((prev) =>
      prev.includes(category) ? prev.filter((c) => c !== category) : [...prev, category],
    )
  }

  function toggleTopicInCategory(category, topic) {
    setSelectedTopicsByCategory((prev) => {
      const current = prev[category] || []
      const next = current.includes(topic)
        ? current.filter((t) => t !== topic)
        : [...current, topic]
      return { ...prev, [category]: next }
    })
  }

  const allTopicsFlat = useMemo(() => Object.values(topicGroups).flat(), [topicGroups])
  const selectedTopics =
    topicMode === 'full_syllabus'
      ? allTopicsFlat
      : Object.values(selectedTopicsByCategory).flat()

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

  const isTopicDrill = testType === 'topic_drill'

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (isTopicDrill) {
      if (selectedTopics.length === 0) {
        setError('Please select at least one topic.')
        return
      }
      setSubmitting(true)
      try {
        const data = await startMockTest({
          test_type: testType,
          sections: [drillSection],
          question_source: 'ai_only',
          topics: selectedTopics,
          question_style: questionStyle,
          question_count: questionCount,
        })
        trackSession(data.session_id, data.status)
        navigate(`/mock-tests/${data.session_id}`)
      } catch (err) {
        const message =
          err?.response?.data?.detail || 'Could not start the practice test. Please try again.'
        setError(message)
      } finally {
        setSubmitting(false)
      }
      return
    }

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
      <PageHeader
        eyebrow="Mock test"
        title="Start a mock test"
        subtitle="Choose the format that matches what you want to practice."
      />
      <div className="ui-card">
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
              <p className="option-hint">VARC, DILR, and QA back to back, 40 minutes each - the real exam sequence.</p>
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
              <p className="option-hint">Just one or two sections, for focused practice without a full 2-hour sitting.</p>
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
              <p className="option-hint">A short, freshly AI-generated set on one section/topic - fastest way to drill a weak spot.</p>
            </div>
          </div>

          {isTopicDrill ? (
            <>
              <div className="form-row-group">
                <div className="form-group">
                  <label>Section</label>
                  <select
                    value={drillSection}
                    onChange={(e) => setDrillSection(e.target.value)}
                    className="select-input"
                  >
                    {DRILL_SECTIONS.map((section) => (
                      <option key={section} value={section}>
                        {section}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="form-group">
                  <label>Coverage</label>
                  <select
                    value={topicMode}
                    onChange={(e) => setTopicMode(e.target.value)}
                    className="select-input"
                  >
                    <option value="topic_wise">Topic-wise (pick specific topics)</option>
                    <option value="full_syllabus">Full syllabus</option>
                  </select>
                </div>
              </div>
              <p className="option-hint" style={{ marginLeft: 0 }}>
                Questions are freshly generated for you each time, never reused from a previous practice test.
              </p>

              {topicMode === 'topic_wise' && (
                <div className="form-group">
                  <label>Topics</label>
                  {Object.entries(topicGroups).map(([category, topics]) => (
                    <div key={category} className="topic-category">
                      <label className="checkbox-item">
                        <input
                          type="checkbox"
                          checked={expandedCategories.includes(category)}
                          onChange={() => toggleCategory(category)}
                        />
                        <span>
                          <strong>{category}</strong>
                        </span>
                      </label>
                      {expandedCategories.includes(category) && (
                        <div className="checkbox-grid" style={{ marginLeft: '1.5rem' }}>
                          {topics.map((topic) => (
                            <label key={topic} className="checkbox-item">
                              <input
                                type="checkbox"
                                checked={(selectedTopicsByCategory[category] || []).includes(topic)}
                                onChange={() => toggleTopicInCategory(category, topic)}
                              />
                              <span>{topic}</span>
                            </label>
                          ))}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              <div className="form-row-group">
                <div className="form-group">
                  <label>Difficulty style</label>
                  <select
                    value={questionStyle}
                    onChange={(e) => setQuestionStyle(e.target.value)}
                    className="select-input"
                  >
                    <option value="challenging">Tough &amp; lengthy (Recommended)</option>
                    <option value="standard">Standard difficulty</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Number of questions</label>
                  <select
                    value={questionCount}
                    onChange={(e) => setQuestionCount(Number(e.target.value))}
                    className="select-input"
                  >
                    {QUESTION_COUNT_OPTIONS.map((count) => (
                      <option key={count} value={count}>
                        {count}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </>
          ) : (
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
                <p className="option-hint">A shuffled blend from the real-paper bank and freshly generated questions.</p>
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
                <p className="option-hint">
                  Only real past-paper questions, but still shuffled/sampled across years - not the same as
                  replaying one exact paper (that's PYQ Practice, below).
                </p>
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
                <p className="option-hint">Entirely fresh questions, never seen on a real CAT paper.</p>
              </div>
              <p className="text-muted">
                Want to replay one exact real paper instead - same questions, same slot, same section split?
                Use <Link to="/pyq-tests">PYQ Practice</Link> instead of this page.
              </p>
            </div>
          )}

          {!isTopicDrill && showPyqFilter && (
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

          {testType !== 'full_mock' && !isTopicDrill && (
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
