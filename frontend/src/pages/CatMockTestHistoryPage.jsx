import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listMockTests } from '../api/catMockTestApi'
import PageHeader from '../components/ui/PageHeader'
import Pill from '../components/ui/Pill'
import ListRow from '../components/ui/ListRow'

const TEST_TYPE_LABELS = {
  full_mock: 'Full Mock',
  sectional: 'Sectional Test',
  topic_drill: 'Topic Drill',
  pyq_paper: 'PYQ Paper',
}

function formatDate(value) {
  if (!value) return ''
  try {
    return new Date(value).toLocaleDateString(undefined, {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  } catch {
    return value
  }
}

export default function CatMockTestHistoryPage() {
  const [sessions, setSessions] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const data = await listMockTests()
        if (!cancelled) setSessions(data.filter((s) => s.status === 'submitted'))
      } catch (err) {
        if (!cancelled) setError(err?.response?.data?.detail || 'Could not load your mock test history.')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [])

  if (loading) return <div className="page-loading">Loading your mock test history...</div>

  return (
    <div className="page-container">
      <PageHeader
        eyebrow="Mock tests"
        title="Your test history"
        subtitle="Every mock test and PYQ paper you've submitted, with a link back to its full results."
        actions={
          <Link className="btn btn-primary btn-sm" to="/mock-tests/new">
            Start a new mock test
          </Link>
        }
      />

      {error && <div className="alert alert-error">{error}</div>}

      <div className="ui-card">
        {sessions.length > 0 ? (
          sessions.map((s) => (
            <ListRow
              key={s.id}
              title={TEST_TYPE_LABELS[s.test_type] || s.test_type}
              meta={
                <>
                  <Pill tone="accent">{s.raw_score ?? '—'} raw score</Pill>
                  <Pill tone="positive">{s.percentile_estimate ?? '—'} percentile</Pill>
                  <span>{formatDate(s.created_at)}</span>
                </>
              }
              actions={
                <Link className="btn btn-secondary btn-sm" to={`/mock-tests/${s.id}/results`}>
                  View results
                </Link>
              }
            />
          ))
        ) : (
          <p className="text-muted">You haven't submitted any mock tests yet.</p>
        )}
      </div>
    </div>
  )
}
