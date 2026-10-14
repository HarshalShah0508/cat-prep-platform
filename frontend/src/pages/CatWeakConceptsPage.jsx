import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getWeakConcepts, practiceWeakConcept } from '../api/catWeakConceptsApi'
import { useCatMockTest } from '../context/CatMockTestContext'
import PageHeader from '../components/ui/PageHeader'
import Pill from '../components/ui/Pill'
import ListRow from '../components/ui/ListRow'
import { AI_FEATURES_DISABLED, AI_DISABLED_MESSAGE } from '../config/featureFlags'

function statusTone(status) {
  switch (status) {
    case 'resolved':
      return 'positive'
    case 'practicing':
      return 'warning'
    default:
      return 'critical'
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
      <PageHeader
        eyebrow="Study plan"
        title="Weak concepts"
        subtitle="Topics flagged from your mock tests that could use more practice."
        stats={[{ value: concepts.length, label: 'Flagged topics', accent: true }]}
      />

      {AI_FEATURES_DISABLED && <div className="alert alert-error">{AI_DISABLED_MESSAGE}</div>}
      {error && <div className="alert alert-error">{error}</div>}

      {concepts.length === 0 ? (
        <div className="ui-card">
          <p className="text-muted">No weak concepts flagged yet. Take a mock test to get started.</p>
        </div>
      ) : (
        <div>
          {concepts.map((c) => (
            <ListRow
              key={c.id}
              title={c.concept}
              meta={
                <>
                  <span className="ui-eyebrow" style={{ marginBottom: 0 }}>{c.section}</span>
                  <Pill tone={statusTone(c.status)}>{c.status}</Pill>
                </>
              }
              actions={
                <button
                  type="button"
                  className="btn btn-secondary btn-sm"
                  onClick={() => handlePractice(c.id)}
                  disabled={practicingId === c.id || AI_FEATURES_DISABLED}
                >
                  {practicingId === c.id ? 'Starting...' : 'Practice'}
                </button>
              }
            />
          ))}
        </div>
      )}
    </div>
  )
}
