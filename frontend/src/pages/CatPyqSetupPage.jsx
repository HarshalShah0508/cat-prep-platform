import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getAvailablePyqPapers, startPyqPaper } from '../api/catPyqApi'
import { useCatMockTest } from '../context/CatMockTestContext'

const SLOT_LABELS = {
  slot1: 'Slot 1',
  slot2: 'Slot 2',
  slot3: 'Slot 3',
}

export default function CatPyqSetupPage() {
  const navigate = useNavigate()
  const { trackSession } = useCatMockTest()
  const [papers, setPapers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [startingKey, setStartingKey] = useState(null)

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

  async function handleStart(paper) {
    const key = `${paper.source_year}-${paper.source_slot}`
    setStartingKey(key)
    setError('')
    try {
      const data = await startPyqPaper({
        source_year: paper.source_year,
        source_slot: paper.source_slot,
      })
      trackSession(data.session_id, data.status)
      navigate(`/mock-tests/${data.session_id}`)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not start this paper. Please try again.')
      setStartingKey(null)
    }
  }

  if (loading) return <div className="page-loading">Loading PYQ papers...</div>

  return (
    <div className="page-container">
      <h1>PYQ practice</h1>
      <p className="text-muted">
        Take a real past CAT paper exactly as it was administered - same questions, same
        slot, same section split.
      </p>

      {error && <div className="alert alert-error">{error}</div>}

      {papers.length === 0 ? (
        <p className="text-muted">No PYQ papers available yet.</p>
      ) : (
        <div className="stat-grid">
          {papers.map((paper) => {
            const key = `${paper.source_year}-${paper.source_slot}`
            const totalQuestions = Object.values(paper.sections).reduce((a, b) => a + b, 0)
            return (
              <div key={key} className="card">
                <h2>
                  CAT {paper.source_year} &middot; {SLOT_LABELS[paper.source_slot] || paper.source_slot}
                </h2>
                <div className="section-result-stats">
                  {Object.entries(paper.sections).map(([section, count]) => (
                    <span key={section} className="tag tag-skipped">
                      {section}: {count}
                    </span>
                  ))}
                </div>
                <p className="text-muted">{totalQuestions} questions total</p>
                <button
                  type="button"
                  className="btn btn-primary btn-block"
                  disabled={startingKey === key}
                  onClick={() => handleStart(paper)}
                >
                  {startingKey === key ? 'Starting...' : 'Start this paper'}
                </button>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
