import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getAvailablePyqPapers, startPyqPaper } from '../api/catPyqApi'
import { useCatMockTest } from '../context/CatMockTestContext'
import PageHeader from '../components/ui/PageHeader'
import Pill from '../components/ui/Pill'
import ListRow from '../components/ui/ListRow'

const SLOT_LABELS = { slot1: 'Slot 1', slot2: 'Slot 2', slot3: 'Slot 3' }
const ALL_SECTIONS = ['VARC', 'DILR', 'QA']

export default function CatPyqSetupPage() {
  const navigate = useNavigate()
  const { trackSession } = useCatMockTest()
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [startingKey, setStartingKey] = useState(null)

  // null = top-level choice, 'sectional' | 'full_mock' = chosen mode,
  // within 'sectional' a section must also be picked before papers show.
  const [mode, setMode] = useState(null)
  const [section, setSection] = useState(null)

  useEffect(() => {
    let cancelled = false
    getAvailablePyqPapers()
      .then((data) => {
        if (!cancelled) setPapers(data)
      })
      .catch(() => {
        if (!cancelled) setError('Could not load available PYQ papers.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  async function handleStart(paper, sections) {
    const key = `${paper.source_year}-${paper.source_slot}-${sections ? sections.join(',') : 'full'}`
    setStartingKey(key)
    setError('')
    try {
      const data = await startPyqPaper({
        source_year: paper.source_year,
        source_slot: paper.source_slot,
        sections,
      })
      trackSession(data.session_id, data.status)
      navigate(`/mock-tests/${data.session_id}`)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not start this paper. Please try again.')
      setStartingKey(null)
    }
  }

  function reset() {
    setMode(null)
    setSection(null)
    setError('')
  }

  if (loading) return <div className="page-loading">Loading PYQ papers...</div>

  // ---------------------------------------------------------------- Top-level choice
  if (mode === null) {
    return (
      <div className="page-container">
        <PageHeader
          eyebrow="PYQ practice"
          title="PYQ practice"
          subtitle="Take a real past CAT paper exactly as it was administered - same questions, same slot, same section split."
        />
        {error && <div className="alert alert-error">{error}</div>}
        <div className="stat-grid">
          <div className="ui-card">
            <h2>Sectional Test</h2>
            <p className="text-muted">
              Practice one section at a time - pick VARC, DILR, or QA, then a specific
              year/slot paper for it.
            </p>
            <button type="button" className="btn btn-primary btn-block" onClick={() => setMode('sectional')}>
              Choose a section
            </button>
          </div>
          <div className="ui-card">
            <h2>Full Mock Test</h2>
            <p className="text-muted">
              The complete real exam sequence - VARC, then DILR, then QA, 40 minutes each,
              exactly as administered.
            </p>
            <button type="button" className="btn btn-primary btn-block" onClick={() => setMode('full_mock')}>
              Choose a paper
            </button>
          </div>
        </div>
      </div>
    )
  }

  // ---------------------------------------------------------------- Sectional: pick section
  if (mode === 'sectional' && section === null) {
    return (
      <div className="page-container">
        <button type="button" className="btn btn-ghost btn-sm" onClick={reset}>
          &larr; Back
        </button>
        <PageHeader
          eyebrow="Sectional test"
          title="Choose a section"
          breadcrumb={[{ label: 'PYQ Practice', onClick: reset }, { label: 'Sectional' }]}
        />
        {error && <div className="alert alert-error">{error}</div>}
        <div className="stat-grid">
          {ALL_SECTIONS.map((sec) => (
            <div key={sec} className="ui-card">
              <h2>{sec}</h2>
              <button type="button" className="btn btn-primary btn-block" onClick={() => setSection(sec)}>
                Select {sec}
              </button>
            </div>
          ))}
        </div>
      </div>
    )
  }

  // ---------------------------------------------------------------- Sectional: pick paper for that section
  if (mode === 'sectional' && section !== null) {
    const eligible = papers.filter((p) => (p.sections[section] ?? 0) > 0)
    return (
      <div className="page-container">
        <button type="button" className="btn btn-ghost btn-sm" onClick={() => setSection(null)}>
          &larr; Back
        </button>
        <PageHeader
          eyebrow="Sectional test"
          title={section}
          breadcrumb={[
            { label: 'PYQ Practice', onClick: reset },
            { label: 'Sectional', onClick: () => setSection(null) },
            { label: section },
          ]}
        />
        {error && <div className="alert alert-error">{error}</div>}
        {eligible.length === 0 ? (
          <p className="text-muted">No {section} papers available yet.</p>
        ) : (
          <div>
            {eligible.map((paper) => {
              const key = `${paper.source_year}-${paper.source_slot}-${section}`
              const slotLabel = SLOT_LABELS[paper.source_slot] || paper.source_slot
              return (
                <ListRow
                  key={key}
                  title={`CAT ${paper.source_year} · ${slotLabel}`}
                  meta={<Pill tone="neutral">{paper.sections[section]} questions</Pill>}
                  actions={
                    <button
                      type="button"
                      className="btn btn-primary"
                      disabled={startingKey === key}
                      onClick={() => handleStart(paper, [section])}
                    >
                      {startingKey === key ? 'Starting...' : 'Start'}
                    </button>
                  }
                />
              )
            })}
          </div>
        )}
      </div>
    )
  }

  // ---------------------------------------------------------------- Full mock: pick paper
  return (
    <div className="page-container">
      <button type="button" className="btn btn-ghost btn-sm" onClick={reset}>
        &larr; Back
      </button>
      <PageHeader
        eyebrow="Full mock test"
        title="Choose a paper"
        breadcrumb={[{ label: 'PYQ Practice', onClick: reset }, { label: 'Full mock' }]}
      />
      {error && <div className="alert alert-error">{error}</div>}
      {papers.length === 0 ? (
        <p className="text-muted">No PYQ papers available yet.</p>
      ) : (
        <div>
          {papers.map((paper) => {
            const key = `${paper.source_year}-${paper.source_slot}-full`
            const slotLabel = SLOT_LABELS[paper.source_slot] || paper.source_slot
            const totalQuestions = Object.values(paper.sections).reduce((a, b) => a + b, 0)
            return (
              <ListRow
                key={key}
                title={`CAT ${paper.source_year} · ${slotLabel}`}
                meta={
                  <>
                    {Object.entries(paper.sections).map(([sec, count]) => (
                      <Pill key={sec} tone="neutral">
                        {sec}: {count}
                      </Pill>
                    ))}
                    <span>{totalQuestions} questions total</span>
                  </>
                }
                actions={
                  <button
                    type="button"
                    className="btn btn-primary"
                    disabled={startingKey === key}
                    onClick={() => handleStart(paper, undefined)}
                  >
                    {startingKey === key ? 'Starting...' : 'Start full mock'}
                  </button>
                }
              />
            )
          })}
        </div>
      )}
    </div>
  )
}
