import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  getMockTest,
  startSection,
  submitSectionAnswers,
  submitMockTest,
} from '../api/catMockTestApi'
import { useCatMockTest } from '../context/CatMockTestContext'

const SECTION_ORDER = ['VARC', 'DILR', 'QA']
const AUTOSAVE_INTERVAL_MS = 20000

function deadlineKey(sessionId, section) {
  return `cat_mock_deadline_${sessionId}_${section}`
}

function formatRemaining(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000))
  const minutes = Math.floor(totalSeconds / 60)
  const seconds = totalSeconds % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

export default function CatMockTestSessionPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const { sessionId: trackedSessionId, status: trackedStatus, trackSession } = useCatMockTest()

  const [test, setTest] = useState(null)
  const [loadError, setLoadError] = useState('')
  const [sectionIndex, setSectionIndex] = useState(0)
  const [answers, setAnswers] = useState({}) // { [questionId]: { selected_answer, time_spent_seconds, was_skipped } }
  const [deadline, setDeadline] = useState(null)
  const [now, setNow] = useState(Date.now())
  const [sectionStarting, setSectionStarting] = useState(false)
  const [finishing, setFinishing] = useState(false)
  const sectionStartedRef = useRef(new Set())

  // Make sure the shared polling context is tracking this session (handles direct
  // navigation / refresh landing straight on this page).
  useEffect(() => {
    if (sessionId && trackedSessionId !== sessionId) {
      trackSession(sessionId)
    }
  }, [sessionId, trackedSessionId, trackSession])

  const effectiveStatus = trackedSessionId === sessionId ? trackedStatus : null

  // Backend returns sections as a list (e.g. [{section: "QA", questions: [...]}]),
  // not a dict keyed by section name.
  const sectionsMap = useMemo(() => {
    const map = {}
    for (const s of test?.sections ?? []) map[s.section] = s
    return map
  }, [test])

  const sections = useMemo(() => {
    return SECTION_ORDER.filter((s) => sectionsMap[s])
  }, [sectionsMap])

  const currentSection = sections[sectionIndex]
  const currentSectionData = currentSection ? sectionsMap[currentSection] : null

  // Load the full test once it's ready (or already in progress).
  useEffect(() => {
    if (!sessionId) return
    if (effectiveStatus !== 'ready' && effectiveStatus !== 'in_progress' && effectiveStatus !== 'submitted') {
      return
    }
    let cancelled = false
    async function load() {
      try {
        const data = await getMockTest(sessionId)
        if (!cancelled) setTest(data)
      } catch (err) {
        if (!cancelled) {
          setLoadError(err?.response?.data?.detail || 'Could not load the test.')
        }
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [sessionId, effectiveStatus])

  const goToNextSectionOrSubmit = useCallback(async () => {
    if (sectionIndex < sections.length - 1) {
      setSectionIndex((i) => i + 1)
    } else {
      setFinishing(true)
      try {
        const result = await submitMockTest(sessionId)
        navigate(`/mock-tests/${sessionId}/results`, { state: result })
      } catch (err) {
        setLoadError(err?.response?.data?.detail || 'Could not submit the test.')
        setFinishing(false)
      }
    }
  }, [sectionIndex, sections.length, sessionId, navigate])

  const buildAnswersPayload = useCallback(
    (sectionData) => {
      if (!sectionData) return []
      return sectionData.questions.map((q) => {
        const entry = answers[q.id] || {}
        return {
          question_id: q.id,
          selected_answer: entry.selected_answer ?? null,
          time_spent_seconds: entry.time_spent_seconds ?? 0,
          was_skipped: entry.was_skipped ?? !entry.selected_answer,
        }
      })
    },
    [answers],
  )

  const saveCurrentSectionAnswers = useCallback(async () => {
    if (!currentSection || !currentSectionData) return
    try {
      await submitSectionAnswers(sessionId, currentSection, buildAnswersPayload(currentSectionData))
    } catch {
      // Autosave failures are non-fatal; the final submit on section change will retry.
    }
  }, [sessionId, currentSection, currentSectionData, buildAnswersPayload])

  // Start the section (once) when we land on it, and persist its deadline.
  useEffect(() => {
    if (!currentSection || !sessionId) return
    const key = deadlineKey(sessionId, currentSection)
    const stored = localStorage.getItem(key)

    if (stored) {
      setDeadline(Number(stored))
      return
    }

    if (sectionStartedRef.current.has(currentSection)) return
    sectionStartedRef.current.add(currentSection)

    setSectionStarting(true)
    startSection(sessionId, currentSection)
      .then((data) => {
        const deadlineMs = new Date(data.deadline).getTime()
        localStorage.setItem(key, String(deadlineMs))
        setDeadline(deadlineMs)
      })
      .catch((err) => {
        setLoadError(err?.response?.data?.detail || 'Could not start this section.')
      })
      .finally(() => setSectionStarting(false))
  }, [currentSection, sessionId])

  // Tick the clock every second.
  useEffect(() => {
    const interval = setInterval(() => setNow(Date.now()), 1000)
    return () => clearInterval(interval)
  }, [])

  const remainingMs = deadline ? deadline - now : null

  // Auto-advance when the timer runs out.
  useEffect(() => {
    if (remainingMs !== null && remainingMs <= 0 && !finishing) {
      saveCurrentSectionAnswers().finally(() => {
        if (sessionId && currentSection) {
          localStorage.removeItem(deadlineKey(sessionId, currentSection))
        }
        setDeadline(null)
        goToNextSectionOrSubmit()
      })
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [remainingMs])

  // Periodic autosave while a section is active.
  useEffect(() => {
    if (!currentSection) return undefined
    const interval = setInterval(() => {
      saveCurrentSectionAnswers()
    }, AUTOSAVE_INTERVAL_MS)
    return () => clearInterval(interval)
  }, [currentSection, saveCurrentSectionAnswers])

  function setAnswer(questionId, selectedAnswer) {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: {
        selected_answer: selectedAnswer,
        time_spent_seconds: prev[questionId]?.time_spent_seconds ?? 0,
        was_skipped: false,
      },
    }))
  }

  function skipQuestion(questionId) {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: {
        selected_answer: null,
        time_spent_seconds: prev[questionId]?.time_spent_seconds ?? 0,
        was_skipped: true,
      },
    }))
  }

  async function handleManualNext() {
    if (sessionId && currentSection) {
      localStorage.removeItem(deadlineKey(sessionId, currentSection))
    }
    await saveCurrentSectionAnswers()
    setDeadline(null)
    goToNextSectionOrSubmit()
  }

  if (loadError) {
    return (
      <div className="page-container">
        <div className="alert alert-error">{loadError}</div>
      </div>
    )
  }

  if (effectiveStatus === 'generating' || (!test && effectiveStatus !== 'ready' && effectiveStatus !== 'in_progress')) {
    return (
      <div className="page-container">
        <div className="card generating-card">
          <h1>Generating your test...</h1>
          <p className="text-muted">This can take a little while. Hang tight.</p>
          <div className="spinner" />
        </div>
      </div>
    )
  }

  if (!test || !currentSection || !currentSectionData) {
    return <div className="page-loading">Loading test...</div>
  }

  const isLastSection = sectionIndex === sections.length - 1

  return (
    <div className="page-container">
      <div className="mock-session-header">
        <div>
          <h1>
            {test.test_type === 'full_mock' ? 'Full Mock' : test.test_type} — {currentSection}
          </h1>
          <p className="text-muted">
            Section {sectionIndex + 1} of {sections.length}
          </p>
        </div>
        <div className={`timer ${remainingMs !== null && remainingMs < 60000 ? 'timer-warning' : ''}`}>
          {sectionStarting || remainingMs === null ? '--:--' : formatRemaining(remainingMs)}
        </div>
      </div>

      <div className="question-list">
        {currentSectionData.questions.map((q, idx) => {
          const entry = answers[q.id]
          const isTita = q.question_type === 'TITA' || q.question_type === 'tita'
          const prevGroupId = idx > 0 ? currentSectionData.questions[idx - 1].group_id : null
          const showPassage = q.passage_text && q.group_id !== prevGroupId
          return (
            <div key={q.id}>
              {showPassage && (
                <div className="card passage-card">
                  <div className="question-meta">
                    <span className="badge">Comprehension</span>
                  </div>
                  <p className="passage-text">{q.passage_text}</p>
                </div>
              )}
              <div className="card question-card">
                <div className="question-meta">
                  <span>Q{idx + 1}</span>
                  {q.topic && <span className="badge">{q.topic}</span>}
                  {q.difficulty && <span className="badge badge-muted">{q.difficulty}</span>}
                </div>
                <p className="question-text">{q.question_text}</p>

                {!isTita && Array.isArray(q.options) ? (
                  <div className="options-list">
                    {q.options.map((option, optIdx) => (
                      <label key={optIdx} className="radio-item">
                        <input
                          type="radio"
                          name={`q-${q.id}`}
                          checked={entry?.selected_answer === option}
                          onChange={() => setAnswer(q.id, option)}
                        />
                        <span>{option}</span>
                      </label>
                    ))}
                  </div>
                ) : (
                  <input
                    type="text"
                    className="tita-input"
                    placeholder="Type your answer"
                    value={entry?.selected_answer ?? ''}
                    onChange={(e) => setAnswer(q.id, e.target.value)}
                  />
                )}

                <div className="question-actions">
                  <button
                    type="button"
                    className="btn btn-ghost btn-sm"
                    onClick={() => skipQuestion(q.id)}
                  >
                    {entry?.was_skipped ? 'Skipped' : 'Mark for review / skip'}
                  </button>
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <div className="mock-session-footer">
        <button type="button" className="btn btn-primary" onClick={handleManualNext} disabled={finishing}>
          {finishing
            ? 'Submitting...'
            : isLastSection
              ? 'Submit test'
              : 'Submit section & continue'}
        </button>
      </div>
    </div>
  )
}
