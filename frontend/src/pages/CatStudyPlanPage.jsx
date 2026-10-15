import { useEffect, useState } from 'react'
import { listMockTests } from '../api/catMockTestApi'
import { generateStudyPlan, getStudyPlan } from '../api/catStudyPlanApi'
import PageHeader from '../components/ui/PageHeader'
import Pill from '../components/ui/Pill'
import ListRow from '../components/ui/ListRow'

const DAY_TYPE_LABELS = {
  weak_focus: 'Weak topic',
  strong_revision: 'Strong revision',
  mock_test: 'Mock test',
  taper_revision: 'Final revision',
}

const DAY_TYPE_TONES = {
  weak_focus: 'critical',
  strong_revision: 'positive',
  mock_test: 'accent',
  taper_revision: 'warning',
}

function formatDate(value) {
  try {
    return new Date(value).toLocaleDateString(undefined, {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
    })
  } catch {
    return value
  }
}

export default function CatStudyPlanPage() {
  const [plan, setPlan] = useState(null)
  const [sessions, setSessions] = useState([])
  const [loading, setLoading] = useState(true)
  const [showGenerator, setShowGenerator] = useState(false)
  const [generatingKey, setGeneratingKey] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    let cancelled = false
    async function load() {
      setLoading(true)
      try {
        const data = await getStudyPlan()
        if (!cancelled) setPlan(data)
      } catch {
        if (!cancelled) setPlan(null)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [])

  async function loadSessions() {
    try {
      const data = await listMockTests()
      setSessions(data.filter((s) => s.status === 'submitted'))
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not load your mock test history.')
    }
  }

  function openGenerator() {
    setShowGenerator(true)
    setError('')
    loadSessions()
  }

  async function handleGenerate(source, sessionId) {
    const key = sessionId ? `single_${sessionId}` : 'full_history'
    setGeneratingKey(key)
    setError('')
    try {
      const data = await generateStudyPlan({ source, session_id: sessionId ?? null })
      setPlan(data)
      setShowGenerator(false)
    } catch (err) {
      setError(err?.response?.data?.detail || 'Could not generate a study plan.')
    } finally {
      setGeneratingKey(null)
    }
  }

  if (loading) return <div className="page-loading">Loading your study plan...</div>

  return (
    <div className="page-container">
      <PageHeader
        eyebrow="Study plan"
        title="Day-by-day prep schedule"
        subtitle="A 2-hour/day plan from today to the CAT exam, weighted toward your weak topics with periodic revision and mock tests."
        stats={
          plan
            ? [
                { value: plan.days.length, label: 'Total days' },
                { value: plan.exam_date, label: 'Exam date', accent: true },
              ]
            : undefined
        }
        actions={
          <button type="button" className="btn btn-secondary btn-sm" onClick={openGenerator}>
            {plan ? 'Generate a new plan' : 'Generate my plan'}
          </button>
        }
      />

      {error && <div className="alert alert-error">{error}</div>}

      {showGenerator && (
        <div className="ui-card">
          <h2>Generate from...</h2>
          <p className="text-muted">
            Pick one test to base the plan on, or use your whole history for a more complete picture.
          </p>

          <button
            type="button"
            className="btn btn-primary"
            onClick={() => handleGenerate('full_history', null)}
            disabled={generatingKey === 'full_history'}
            style={{ marginBottom: '1rem' }}
          >
            {generatingKey === 'full_history' ? 'Generating...' : 'Generate from my full history'}
          </button>

          {sessions.length === 0 ? (
            <p className="text-muted">No submitted tests found to use individually.</p>
          ) : (
            <div>
              {sessions.map((s) => (
                <ListRow
                  key={s.id}
                  title={`${s.test_type.replace('_', ' ')} - ${s.sections_included.join(', ')}`}
                  meta={
                    <>
                      <span className="ui-eyebrow" style={{ marginBottom: 0 }}>{formatDate(s.created_at)}</span>
                      {s.percentile_estimate != null && (
                        <Pill tone="accent">{s.percentile_estimate.toFixed(1)} %ile</Pill>
                      )}
                    </>
                  }
                  actions={
                    <button
                      type="button"
                      className="btn btn-secondary btn-sm"
                      onClick={() => handleGenerate('single_test', s.id)}
                      disabled={generatingKey === `single_${s.id}`}
                    >
                      {generatingKey === `single_${s.id}` ? 'Generating...' : 'Use this test'}
                    </button>
                  }
                />
              ))}
            </div>
          )}
        </div>
      )}

      {!plan && !showGenerator && (
        <div className="ui-card">
          <p className="text-muted">No study plan generated yet. Click "Generate my plan" to get started.</p>
        </div>
      )}

      {plan && (
        <div>
          {plan.days.map((day) => (
            <ListRow
              key={day.day_number}
              title={
                day.topics.length > 0
                  ? `Day ${day.day_number}: ${day.topics.join(', ')}`
                  : `Day ${day.day_number}`
              }
              meta={
                <>
                  <span className="ui-eyebrow" style={{ marginBottom: 0 }}>{formatDate(day.date)}</span>
                  <Pill tone={DAY_TYPE_TONES[day.day_type] || 'neutral'}>
                    {DAY_TYPE_LABELS[day.day_type] || day.day_type}
                  </Pill>
                  {day.section && <Pill tone="neutral">{day.section}</Pill>}
                </>
              }
              actions={<span className="text-muted">{day.note}</span>}
            />
          ))}
        </div>
      )}
    </div>
  )
}
