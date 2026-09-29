import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getDashboard } from '../api/dashboardApi'
import { getCatProfile } from '../api/catProfileApi'

function StatCard({ label, value }) {
  return (
    <div className="card stat-card">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
    </div>
  )
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

export default function DashboardPage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      setError('')
      try {
        const profile = await getCatProfile().catch(() => null)
        if (!profile || !profile.cat_academic_background) {
          if (!cancelled) navigate('/onboarding', { replace: true })
          return
        }
        const result = await getDashboard()
        if (!cancelled) setData(result)
      } catch (err) {
        if (!cancelled) {
          setError(
            err?.response?.data?.detail || 'Could not load your dashboard. Please try again.',
          )
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

  if (loading) {
    return <div className="page-loading">Loading dashboard...</div>
  }

  if (error) {
    return (
      <div className="page-container">
        <div className="alert alert-error">{error}</div>
      </div>
    )
  }

  return (
    <div className="page-container">
      <h1>Welcome back{data?.username ? `, ${data.username}` : ''}</h1>
      <p className="text-muted">{data?.email}</p>

      <div className="stat-grid">
        <StatCard label="Mock tests taken" value={data?.mock_tests_taken ?? 0} />
        <StatCard
          label="Avg percentile"
          value={data?.avg_percentile != null ? data.avg_percentile.toFixed(2) : '—'}
        />
        <StatCard label="PI sessions completed" value={data?.pi_sessions_completed ?? 0} />
        <StatCard label="Weak concepts flagged" value={data?.weak_concepts_flagged ?? 0} />
        <StatCard label="Weak concepts resolved" value={data?.weak_concepts_resolved ?? 0} />
      </div>

      <div className="dashboard-grid">
        <div className="card">
          <h2>Latest mock test</h2>
          {data?.latest_mock_result ? (
            <div>
              <p>
                Raw score: <strong>{data.latest_mock_result.raw_score}</strong>
              </p>
              <p>
                Percentile estimate:{' '}
                <strong>{data.latest_mock_result.percentile_estimate}</strong>
              </p>
              <p className="text-muted">{formatDate(data.latest_mock_result.created_at)}</p>
            </div>
          ) : (
            <p className="text-muted">No mock tests taken yet.</p>
          )}
          <Link to="/mock-tests/new" className="btn btn-primary">
            Start a new mock test
          </Link>
        </div>

        <div className="card">
          <h2>Latest PI session</h2>
          {data?.latest_pi_session ? (
            <div>
              <p>
                Overall score: <strong>{data.latest_pi_session.overall_score}</strong>
              </p>
              <p className="text-muted">{formatDate(data.latest_pi_session.created_at)}</p>
            </div>
          ) : (
            <p className="text-muted">No PI practice sessions yet.</p>
          )}
          <Link to="/pi" className="btn btn-primary">
            Start PI practice
          </Link>
        </div>

        <div className="card">
          <h2>Weak concepts</h2>
          <p className="text-muted">
            {data?.weak_concepts_flagged ?? 0} flagged, {data?.weak_concepts_resolved ?? 0}{' '}
            resolved.
          </p>
          <Link to="/weak-concepts" className="btn btn-secondary">
            View weak concepts
          </Link>
        </div>
      </div>
    </div>
  )
}
