import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getWeakConcepts, practiceWeakConcept } from '../api/catWeakConceptsApi'
import { useCatMockTest } from '../context/CatMockTestContext'

function statusBadgeClass(status) {
  switch (status) {
    case 'resolved':
      return 'badge badge-success'
    case 'practicing':
      return 'badge badge-warning'
    default:
      return 'badge badge-error'
  }
}

export default function CatWeakConceptsPage() {
  const navigate = useNavigate()
  const { trackSession } = useCatMockTest()
  const [concepts, setConcepts] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const [practicingId, setPracticingId] = useState(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const data = await getWeakConcepts()
        if (!cancelled) setConcepts(data)
      } catch (err) {
        if (!cancelled) {
          setError(err?.response?.data?.detail || 'Could not load weak concepts.')
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [])

  async function handlePractice(id) {
    setPracticingId(id)
    setError('')
    try {
      const drill = await practiceWeakConcept(id)
      trackSession(drill.id, drill.status)
      navigate(`/mock-tests/${drill.id}`)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not start a practice drill.')
    } finally {
      setPracticingId(null)
    }
  }

  if (loading) return <div className="page-loading">Loading weak concepts...</div>

  return (
    <div className="page-container">
      <h1>Weak concepts</h1>
      <p className="text-muted">Topics flagged from your mock tests that could use more practice.</p>

      {error && <div className="alert alert-error">{error}</div>}

      {concepts.length === 0 ? (
        <div className="card">
          <p className="text-muted">No weak concepts flagged yet. Take a mock test to get started.</p>
        </div>
      ) : (
        <div className="weak-concept-list">
          {concepts.map((c) => (
            <div key={c.id} className="card weak-concept-card">
              <div>
                <div className="weak-concept-section">{c.section}</div>
                <div className="weak-concept-name">{c.concept}</div>
              </div>
              <div className="weak-concept-actions">
                <span className={statusBadgeClass(c.status)}>{c.status}</span>
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() => handlePractice(c.id)}
                  disabled={practicingId === c.id}
                >
                  {practicingId === c.id ? 'Starting...' : 'Practice'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
