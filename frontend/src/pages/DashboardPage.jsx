import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getDashboard } from '../api/dashboardApi'
import { getCatProfile } from '../api/catProfileApi'
import { useAuth } from '../context/AuthContext'
import PageHeader from '../components/ui/PageHeader'
import AuthGatedLink from '../components/auth/AuthGatedLink'

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
  const { isAuthenticated } = useAuth()
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    if (!isAuthenticated) {
      setData(null)
      setError('')
      setLoading(false)
      return
    }

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
  }, [isAuthenticated])

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
      {isAuthenticated ? (
        <PageHeader
          eyebrow="Dashboard"
          title={`Welcome back${data?.username ? `, ${data.username}` : ''}`}
          subtitle={data?.email}
          stats={[
            { value: data?.mock_tests_taken ?? 0, label: 'Mock tests' },
            {
              value: data?.avg_percentile != null ? data.avg_percentile.toFixed(2) : '—',
              label: 'Avg percentile',
              accent: true,
            },
            { value: data?.pi_sessions_completed ?? 0, label: 'PI sessions' },
            { value: data?.weak_concepts_flagged ?? 0, label: 'Weak concepts' },
          ]}
        />
      ) : (
        <PageHeader
          eyebrow="Dashboard"
          title="Welcome to CATPrep"
          subtitle="Full mocks, real past papers, AI-scored Personal Interview practice, and automatic weak-topic tracking."
        />
      )}

      <div className="dashboard-hub">
        <div className="ui-card dashboard-cta-card">
          <div className="ui-eyebrow">Ready when you are</div>
          <h2>Start your next mock test</h2>
          <p className="text-muted">
            Full mock, sectional, or a topic drill - pick the format and go.
          </p>
          {isAuthenticated ? (
            data?.latest_mock_result ? (
              <div>
                <p>
                  Last result: <strong>{data.latest_mock_result.raw_score}</strong> raw score,{' '}
                  <strong>{data.latest_mock_result.percentile_estimate}</strong> percentile
                </p>
                <p className="text-muted">{formatDate(data.latest_mock_result.created_at)}</p>
              </div>
            ) : (
              <p className="text-muted">No mock tests taken yet.</p>
            )
          ) : (
            <p className="text-muted">Log in to track your results here.</p>
          )}
          <AuthGatedLink to="/mock-tests/new" className="ui-btn-hero">
            Start a new mock test
          </AuthGatedLink>
        </div>

        <div className="dashboard-side-col">
          <div className="ui-card">
            <div className="ui-eyebrow">PYQ practice</div>
            <h2>Real past papers</h2>
            <p className="text-muted">Replay an exact past CAT paper, slot by slot.</p>
            <AuthGatedLink to="/pyq-tests" className="btn btn-secondary btn-sm">
              Browse PYQ papers →
            </AuthGatedLink>
          </div>

          <div className="ui-card">
            <div className="ui-eyebrow">Latest PI session</div>
            <h2>Personal Interview</h2>
            {isAuthenticated ? (
              data?.latest_pi_session ? (
                <p className="text-muted">
                  Last score {data.latest_pi_session.overall_score} ·{' '}
                  {formatDate(data.latest_pi_session.created_at)}
                </p>
              ) : (
                <p className="text-muted">No PI practice sessions yet.</p>
              )
            ) : (
              <p className="text-muted">AI-scored mock interviews with delivery feedback.</p>
            )}
            <AuthGatedLink to="/pi/new" className="btn btn-secondary btn-sm">
              Start PI practice →
            </AuthGatedLink>
          </div>

          <div className="ui-card">
            <div className="ui-eyebrow">Study plan</div>
            <h2>Weak concepts</h2>
            {isAuthenticated ? (
              <p className="text-muted">
                {data?.weak_concepts_flagged ?? 0} flagged, {data?.weak_concepts_resolved ?? 0}{' '}
                resolved.
              </p>
            ) : (
              <p className="text-muted">Automatically flagged from your mock test performance.</p>
            )}
            <AuthGatedLink to="/weak-concepts" className="btn btn-secondary btn-sm">
              View weak concepts →
            </AuthGatedLink>
          </div>
        </div>
      </div>
    </div>
  )
}
