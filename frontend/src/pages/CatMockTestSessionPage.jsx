import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import {
  getMockTest,
  startSection,
  submitSectionAnswers,
  submitMockTest,
} from '../api/catMockTestApi'
import { useCatMockTest } from '../context/CatMockTestContext'
import StepChart from '../components/StepChart'
import QuestionPalette from '../components/QuestionPalette'
import Calculator from '../components/Calculator'

const SECTION_ORDER = ['VARC', 'DILR', 'QA']
const AUTOSAVE_INTERVAL_MS = 20000
const SLOT_LABELS = { slot1: 'Slot 1', slot2: 'Slot 2', slot3: 'Slot 3' }

function testTitle(test) {
  if (test.test_type === 'pyq_paper') {
    const slot = SLOT_LABELS[test.pyq_source_slot] || test.pyq_source_slot
    return `CAT ${test.pyq_source_year} · ${slot}`
  }
  if (test.test_type === 'full_mock') return 'Full Mock'
  if (test.test_type === 'topic_drill') return 'Topic Drill'
  return 'Sectional Test'
}

function deadlineKey(sessionId, section) {
  return `cat_mock_deadline_${sessionId}_${section}`
}

function formatRemaining(ms) {
  const totalSeconds = Math.max(0, Math.floor(ms / 1000))
  const minutes = Math.floor(totalSeconds / 60)
  const seconds = totalSeconds % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
}

const DEFAULT_ENTRY = {
  selected_answer: null,
  time_spent_seconds: 0,
  was_skipped: true,
  marked_for_review: false,
  visited: false,
  status: 'not_visited',
}

export default function CatMockTestSessionPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const { sessionId: trackedSessionId, status: trackedStatus, trackSession } = useCatMockTest()

  const [test, setTest] = useState(null)
  const [loadError, setLoadError] = useState('')
  const [sectionIndex, setSectionIndex] = useState(0)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  // Committed per-question state: { [questionId]: { selected_answer, time_spent_seconds,
  // was_skipped, marked_for_review, visited, status } }. Only Save & Next / Mark for
  // Review write here - navigating away any other way discards unsaved changes.
  const [answers, setAnswers] = useState({})
  // Transient selection for the CURRENTLY shown question only, pre-filled from the
  // committed answer when landing on a question, discarded if left without saving.
  const [draftAnswer, setDraftAnswer] = useState(null)
  const [deadline, setDeadline] = useState(null)
  const [now, setNow] = useState(Date.now())
  const [sectionStarting, setSectionStarting] = useState(false)
  const [finishing, setFinishing] = useState(false)
  const [isFullscreen, setIsFullscreen] = useState(Boolean(document.fullscreenElement))
  const [showCalculator, setShowCalculator] = useState(false)
  const [paletteCollapsed, setPaletteCollapsed] = useState(false)
  const sectionStartedRef = useRef(new Set())
  const questionEnteredAtRef = useRef(Date.now())

  function enterFullscreen() {
    const el = document.documentElement
    const request = el.requestFullscreen || el.webkitRequestFullscreen
    if (request) {
      request.call(el).catch(() => {})
    }
  }

  function exitFullscreen() {
    const exit = document.exitFullscreen || document.webkitExitFullscreen
    if ((document.fullscreenElement || document.webkitFullscreenElement) && exit) {
      exit.call(document).catch(() => {})
    }
  }

  // Track real fullscreen state (the user can always bail with Escape - don't fight it,
  // just reflect it so the "enter fullscreen" prompt can reappear).
  useEffect(() => {
    function handleChange() {
      setIsFullscreen(Boolean(document.fullscreenElement || document.webkitFullscreenElement))
    }
    document.addEventListener('fullscreenchange', handleChange)
    document.addEventListener('webkitfullscreenchange', handleChange)
    return () => {
      document.removeEventListener('fullscreenchange', handleChange)
      document.removeEventListener('webkitfullscreenchange', handleChange)
    }
  }, [])

  // Leaving the page (submit, exit, navigating away, unmount) always drops fullscreen.
  useEffect(() => {
    return () => exitFullscreen()
  }, [])

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
  const currentQuestion = currentSectionData?.questions?.[currentQuestionIndex] ?? null

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
        if (!cancelled) {
          setTest(data)
          // Seed committed answers from any previously-saved state (refresh recovery).
          const seeded = {}
          for (const s of data.sections ?? []) {
            for (const q of s.questions ?? []) {
              seeded[q.id] = {
                selected_answer: q.selected_answer ?? null,
                time_spent_seconds: 0,
                was_skipped: q.was_skipped,
                marked_for_review: q.marked_for_review,
                visited: q.visited,
                // Authoritative, verbatim from the backend - never re-derived, since
                // "visited but never saved" must stay 'not_visited', not become red.
                status: q.status || 'not_visited',
              }
            }
          }
          setAnswers(seeded)
        }
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

  // Reset to the first question whenever the active section changes, and close the
  // calculator (it's only offered for QA/DILR, matching the real exam).
  useEffect(() => {
    setCurrentQuestionIndex(0)
    setShowCalculator(false)
  }, [currentSection])

  // Pre-fill the transient draft from committed state whenever the shown question
  // changes, and start the per-question time-tracking clock.
  useEffect(() => {
    if (!currentQuestion) return
    setDraftAnswer(answers[currentQuestion.id]?.selected_answer ?? null)
    questionEnteredAtRef.current = Date.now()
    // Mark visited (without touching status/selected_answer) the first time we land here.
    setAnswers((prev) => {
      const existing = prev[currentQuestion.id] || DEFAULT_ENTRY
      if (existing.visited) return prev
      return { ...prev, [currentQuestion.id]: { ...existing, visited: true } }
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentQuestion?.id])

  const accumulateTime = useCallback((questionId) => {
    if (!questionId) return
    const elapsedSeconds = Math.round((Date.now() - questionEnteredAtRef.current) / 1000)
    if (elapsedSeconds <= 0) return
    setAnswers((prev) => {
      const existing = prev[questionId] || DEFAULT_ENTRY
      return {
        ...prev,
        [questionId]: {
          ...existing,
          time_spent_seconds: (existing.time_spent_seconds || 0) + elapsedSeconds,
        },
      }
    })
  }, [])

  const buildAnswersPayload = useCallback(
    (sectionData) => {
      if (!sectionData) return []
      return sectionData.questions.map((q) => {
        const entry = answers[q.id] || DEFAULT_ENTRY
        return {
          question_id: q.id,
          selected_answer: entry.selected_answer ?? null,
          time_spent_seconds: entry.time_spent_seconds ?? 0,
          was_skipped: !entry.selected_answer,
          marked_for_review: entry.marked_for_review ?? false,
          visited: entry.visited ?? false,
          status: entry.status || 'not_visited',
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

  const goToNextSectionOrSubmit = useCallback(async () => {
    if (sectionIndex < sections.length - 1) {
      setSectionIndex((i) => i + 1)
    } else {
      setFinishing(true)
      try {
        const result = await submitMockTest(sessionId)
        exitFullscreen()
        navigate(`/mock-tests/${sessionId}/results`, { state: result })
      } catch (err) {
        setLoadError(err?.response?.data?.detail || 'Could not submit the test.')
        setFinishing(false)
      }
    }
  }, [sectionIndex, sections.length, sessionId, navigate])

  // Start the section (once) when we land on it, and persist its deadline. Gated on
  // fullscreen so the clock doesn't start before the user clicks "Begin Test".
  useEffect(() => {
    if (!currentSection || !sessionId || !isFullscreen) return
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
  }, [currentSection, sessionId, isFullscreen])

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

  function commitCurrentQuestion(status) {
    if (!currentQuestion) return
    accumulateTime(currentQuestion.id)
    setAnswers((prev) => {
      const existing = prev[currentQuestion.id] || DEFAULT_ENTRY
      return {
        ...prev,
        [currentQuestion.id]: {
          ...existing,
          selected_answer: draftAnswer || null,
          was_skipped: !draftAnswer,
          marked_for_review: status === 'marked_for_review' || status === 'answered_marked_for_review',
          visited: true,
          status,
        },
      }
    })
  }

  function goToQuestionIndex(nextIndex) {
    const total = currentSectionData?.questions?.length ?? 0
    if (nextIndex < 0 || nextIndex >= total) return
    setCurrentQuestionIndex(nextIndex)
  }

  function handleSaveNext() {
    commitCurrentQuestion(draftAnswer ? 'answered' : 'not_answered')
    goToQuestionIndex(currentQuestionIndex + 1)
  }

  function handleMarkForReview() {
    // Real exam: marking a question with an answer already selected still counts it in
    // scoring and shows a distinct 5th palette state (purple with a green dot), not
    // plain "marked for review".
    commitCurrentQuestion(draftAnswer ? 'answered_marked_for_review' : 'marked_for_review')
    goToQuestionIndex(currentQuestionIndex + 1)
  }

  function handleClearResponse() {
    setDraftAnswer(null)
  }

  function handlePaletteJump(index) {
    if (index === currentQuestionIndex) return
    // Leaving without Save & Next / Mark for Review discards the draft selection -
    // only accumulate time spent, don't commit selected_answer/status.
    accumulateTime(currentQuestion?.id)
    goToQuestionIndex(index)
  }

  async function handleSubmitNow() {
    const label = sectionIndex < sections.length - 1 ? 'this section' : 'the test'
    if (!window.confirm(`Submit ${label}? You won't be able to change answers after this.`)) {
      return
    }
    accumulateTime(currentQuestion?.id)
    if (sessionId && currentSection) {
      localStorage.removeItem(deadlineKey(sessionId, currentSection))
    }
    await saveCurrentSectionAnswers()
    setDeadline(null)
    goToNextSectionOrSubmit()
  }

  async function handleExitTest() {
    if (
      !window.confirm(
        "Exit the test now? You'll be scored on whatever you've answered so far and taken to your results - you won't be able to come back to finish it.",
      )
    ) {
      return
    }
    accumulateTime(currentQuestion?.id)
    if (sessionId && currentSection) {
      localStorage.removeItem(deadlineKey(sessionId, currentSection))
    }
    await saveCurrentSectionAnswers()
    setDeadline(null)
    setFinishing(true)
    try {
      const result = await submitMockTest(sessionId)
      exitFullscreen()
      navigate(`/mock-tests/${sessionId}/results`, { state: result })
    } catch (err) {
      setLoadError(err?.response?.data?.detail || 'Could not submit the test.')
      setFinishing(false)
    }
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

  if (!test || !currentSection || !currentSectionData || !currentQuestion) {
    return <div className="page-loading">Loading test...</div>
  }

  if (!isFullscreen) {
    return (
      <div className="page-container">
        <div className="card generating-card">
          <h1>Ready to begin?</h1>
          <p className="text-muted">
            The test runs in full screen, just like the real exam. Click below to enter full
            screen and start the timer.
          </p>
          <button
            type="button"
            className="btn btn-primary"
            onClick={() => {
              enterFullscreen()
            }}
          >
            Begin Test (Full Screen)
          </button>
        </div>
      </div>
    )
  }

  const isLastSection = sectionIndex === sections.length - 1
  const isTita = currentQuestion.question_type === 'TITA' || currentQuestion.question_type === 'tita'
  const paletteQuestions = currentSectionData.questions.map((q) => ({
    id: q.id,
    status: answers[q.id]?.status || 'not_visited',
  }))

  return (
    <div className="page-container exam-page">
      <div className="mock-session-header">
        <div>
          <h1>{testTitle(test)} — {currentSection}</h1>
          <p className="text-muted">
            Question {currentQuestionIndex + 1} of {currentSectionData.questions.length}
          </p>
        </div>
        <div className={`timer ${remainingMs !== null && remainingMs < 60000 ? 'timer-warning' : ''}`}>
          {sectionStarting || remainingMs === null ? '--:--' : formatRemaining(remainingMs)}
        </div>
        <div className="exam-header-actions">
          {(currentSection === 'QA' || currentSection === 'DILR') && (
            <button
              type="button"
              className="btn btn-ghost btn-sm"
              onClick={() => setShowCalculator((v) => !v)}
            >
              Calculator
            </button>
          )}
          <button type="button" className="btn btn-ghost btn-sm" onClick={handleExitTest} disabled={finishing}>
            Exit Test
          </button>
          <button type="button" className="btn btn-secondary btn-sm" onClick={handleSubmitNow} disabled={finishing}>
            {finishing ? 'Submitting...' : isLastSection ? 'Submit Test' : 'Submit Section'}
          </button>
        </div>
      </div>

      <div className={`exam-layout ${paletteCollapsed ? 'exam-layout-collapsed' : ''}`}>
        <div className="exam-question-area">
          {currentQuestion.passage_text && (
            <div className="card passage-card">
              <div className="question-meta">
                <span className="badge">Comprehension</span>
              </div>
              <p className="passage-text">{currentQuestion.passage_text}</p>
              <StepChart charts={currentQuestion.chart_data} />
            </div>
          )}

          <div className="card question-card">
            <div className="question-meta">
              <span>Q{currentQuestionIndex + 1}</span>
              {currentQuestion.topic && <span className="badge">{currentQuestion.topic}</span>}
              {currentQuestion.difficulty && (
                <span className="badge badge-muted">{currentQuestion.difficulty}</span>
              )}
            </div>
            <p className="question-text">{currentQuestion.question_text}</p>

            {!isTita && Array.isArray(currentQuestion.options) ? (
              <div className="options-list">
                {currentQuestion.options.map((option, optIdx) => (
                  <label key={optIdx} className="radio-item">
                    <input
                      type="radio"
                      name={`q-${currentQuestion.id}`}
                      checked={draftAnswer === option}
                      onChange={() => setDraftAnswer(option)}
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
                value={draftAnswer ?? ''}
                onChange={(e) => setDraftAnswer(e.target.value)}
              />
            )}

            <div className="exam-actions">
              <button type="button" className="btn btn-ghost" onClick={handleClearResponse}>
                Clear Response
              </button>
              <button type="button" className="btn btn-secondary" onClick={handleMarkForReview}>
                Mark for Review &amp; Next
              </button>
              <button type="button" className="btn btn-primary" onClick={handleSaveNext}>
                Save &amp; Next
              </button>
            </div>
          </div>
        </div>

        <button
          type="button"
          className="palette-toggle"
          onClick={() => setPaletteCollapsed((v) => !v)}
          aria-label={paletteCollapsed ? 'Expand question palette' : 'Collapse question palette'}
          title={paletteCollapsed ? 'Expand question palette' : 'Collapse question palette'}
        >
          {paletteCollapsed ? '‹' : '›'}
        </button>

        {!paletteCollapsed && (
          <QuestionPalette
            questions={paletteQuestions}
            currentIndex={currentQuestionIndex}
            onJump={handlePaletteJump}
          />
        )}
      </div>

      {showCalculator && (currentSection === 'QA' || currentSection === 'DILR') && (
        <Calculator onClose={() => setShowCalculator(false)} />
      )}
    </div>
  )
}
