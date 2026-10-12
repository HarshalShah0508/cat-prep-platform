import { useEffect, useRef, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import {
  answerPiQuestion,
  finishPiSession,
  generatePiFollowUp,
  getPiSession,
  submitPiSessionFeedback,
} from '../api/catPiApi'
import QuestionCard from '../components/pi/QuestionCard'
import AnswerBox from '../components/pi/AnswerBox'
import FeedbackCard from '../components/pi/FeedbackCard'
import DeliveryConsentModal from '../components/pi/DeliveryConsentModal'
import DeliveryCalibrationScreen from '../components/pi/DeliveryCalibrationScreen'
import PreInterviewDisclaimerModal from '../components/pi/PreInterviewDisclaimerModal'
import ExitFeedbackModal from '../components/pi/ExitFeedbackModal'
import WebcamMonitor from '../components/pi/WebcamMonitor'
import { createAudioDeliveryAnalyzer } from '../utils/audioDeliveryAnalyzer'
import { createVideoDeliveryAnalyzer } from '../utils/videoDeliveryAnalyzer'

const CALIBRATION_MS = 3000

export default function CatPiSessionPage() {
  const { sessionId } = useParams()
  const navigate = useNavigate()
  const answerBoxRef = useRef(null)

  const [session, setSession] = useState(null)
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const [answeredQuestions, setAnsweredQuestions] = useState(new Set())
  const [feedbackMap, setFeedbackMap] = useState({})
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false)
  const [disclaimerAcknowledged, setDisclaimerAcknowledged] = useState(false)
  const [showExitFeedback, setShowExitFeedback] = useState(false)
  // True while the on-demand follow-up check/generation triggered by "Next"/"Finish" is in
  // flight - whether a follow-up exists isn't known until this resolves.
  const [generatingFollowUp, setGeneratingFollowUp] = useState(false)

  // null = undecided (show consent modal), true/false once decided.
  const [deliveryConsent, setDeliveryConsent] = useState(null)
  const [calibrating, setCalibrating] = useState(false)
  const [webcamStream, setWebcamStream] = useState(null)
  const audioAnalyzerRef = useRef(null)
  const videoAnalyzerRef = useRef(null)

  useEffect(() => {
    let cancelled = false

    async function fetchSession() {
      try {
        setLoading(true)
        const data = await getPiSession(sessionId)
        if (cancelled) return

        if (data.status === 'finished') {
          navigate(`/pi/${sessionId}/results`, { replace: true })
          return
        }

        setSession(data)

        const answered = new Set()
        const feedbacks = {}
        data.questions.forEach((question) => {
          if (question.answer) {
            answered.add(question.id)
            feedbacks[question.id] = {
              answerId: question.answer.id,
              score: question.answer.score,
              feedback: question.answer.feedback,
              strengths: question.answer.strengths,
              improvements: question.answer.improvements,
              deliveryFeedback: question.answer.delivery_feedback,
              eligibleForFollowUp: false,
            }
          }
        })
        setAnsweredQuestions(answered)
        setFeedbackMap(feedbacks)

        const firstUnanswered = data.questions.findIndex((question) => !question.answer)
        if (firstUnanswered !== -1) setCurrentQuestionIndex(firstUnanswered)
      } catch (err) {
        if (!cancelled) setError(err?.response?.data?.detail || 'Could not load this PI session.')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    fetchSession()
    return () => {
      cancelled = true
    }
  }, [sessionId, navigate])

  useEffect(() => {
    return () => {
      audioAnalyzerRef.current?.stop()
      audioAnalyzerRef.current = null
      videoAnalyzerRef.current?.stop()
      videoAnalyzerRef.current = null
      setWebcamStream(null)
    }
  }, [])

  // Delivery signals are scoped per-question - clear counters whenever the visible
  // question changes, so one question's pauses never bleed into the next.
  useEffect(() => {
    audioAnalyzerRef.current?.reset()
    videoAnalyzerRef.current?.reset()
  }, [currentQuestionIndex])

  async function handleContinueDelivery({ audioEnabled, videoEnabled }) {
    let anyEnabled = false

    if (audioEnabled) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        const analyzer = createAudioDeliveryAnalyzer()
        await analyzer.start(stream)
        audioAnalyzerRef.current = analyzer
        anyEnabled = true
      } catch (err) {
        console.log('Delivery-analysis mic access failed:', err)
      }
    }

    if (videoEnabled) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true })
        const analyzer = createVideoDeliveryAnalyzer()
        await analyzer.start(stream)
        videoAnalyzerRef.current = analyzer
        setWebcamStream(stream)
        anyEnabled = true
      } catch (err) {
        console.log('Delivery-analysis camera access failed:', err)
      }
    }

    if (anyEnabled) {
      setCalibrating(true)
      await Promise.all(
        [audioAnalyzerRef.current, videoAnalyzerRef.current].filter(Boolean).map((a) => a.calibrate(CALIBRATION_MS)),
      )
      setCalibrating(false)
    }

    setDeliveryConsent(anyEnabled)
  }

  function handleDeclineDelivery() {
    setDeliveryConsent(false)
  }

  function handleRecordingStateChange(isActive) {
    audioAnalyzerRef.current?.setActive(isActive)
  }

  // Snapshots signals for this answer, then stops audio tracking so time spent AFTER
  // submitting never leaks into the next question's counters.
  function getDeliverySignals() {
    if (!deliveryConsent) return null

    const audioSignals = audioAnalyzerRef.current?.getSignalsSinceReset()
    const videoSignals = videoAnalyzerRef.current?.getSignalsSinceReset()
    audioAnalyzerRef.current?.setActive(false)

    if (!audioSignals && !videoSignals) return null
    return { ...audioSignals, ...videoSignals }
  }

  if (loading) return <div className="page-loading">Loading PI practice...</div>

  if (error) {
    return (
      <div className="page-container">
        <div className="alert alert-error">{error}</div>
      </div>
    )
  }

  // True the instant the consent/calibration gate resolves either way - questions should
  // never be spoken aloud while that overlay is up.
  const interviewReady = disclaimerAcknowledged && deliveryConsent !== null && !calibrating

  const currentQuestion = session.questions[currentQuestionIndex]
  const currentFeedback = feedbackMap[currentQuestion.id]

  const mainQuestions = session.questions.filter((q) => !q.is_follow_up)
  const totalMainQuestions = mainQuestions.length
  const currentMainQuestionNumber = session.questions
    .slice(0, currentQuestionIndex + 1)
    .filter((q) => !q.is_follow_up).length
  const currentMainIndex = currentMainQuestionNumber - 1

  async function handleAnswer(answerText, deliverySignals) {
    const response = await answerPiQuestion(sessionId, {
      pi_session_question_id: currentQuestion.id,
      answer_text: answerText,
      delivery_signals: deliverySignals,
    })

    setFeedbackMap((prev) => ({
      ...prev,
      [currentQuestion.id]: {
        answerId: response.answer.id,
        score: response.answer.score,
        feedback: response.answer.feedback,
        strengths: response.answer.strengths,
        improvements: response.answer.improvements,
        deliveryFeedback: response.answer.delivery_feedback,
        modelAnswer: response.model_answer,
        deliverySignals,
        eligibleForFollowUp: response.eligible_for_follow_up,
      },
    }))

    setAnsweredQuestions((prev) => {
      const updated = new Set(prev)
      updated.add(currentQuestion.id)
      return updated
    })
  }

  // Generates the follow-up for the just-answered current question, if eligible, and
  // splices it into the live question list right after the current one. Returns true if a
  // follow-up was added.
  async function maybeGenerateFollowUp() {
    const feedback = feedbackMap[currentQuestion.id]
    if (!feedback?.eligibleForFollowUp) return false

    setGeneratingFollowUp(true)
    try {
      const { question: followUp } = await generatePiFollowUp(sessionId, feedback.answerId)

      setSession((prev) => {
        const updatedQuestions = [...prev.questions]
        updatedQuestions.splice(currentQuestionIndex + 1, 0, {
          id: followUp.id,
          question_text: followUp.question_text,
          order_index: followUp.order_index,
          follow_up_depth: followUp.follow_up_depth,
          parent_question_id: followUp.parent_question_id,
          is_follow_up: true,
          answer: null,
        })
        return { ...prev, questions: updatedQuestions }
      })

      setFeedbackMap((prev) => ({
        ...prev,
        [currentQuestion.id]: { ...prev[currentQuestion.id], eligibleForFollowUp: false },
      }))

      return true
    } catch (err) {
      console.log('Follow-up generation failed:', err)
      return false
    } finally {
      setGeneratingFollowUp(false)
    }
  }

  function handlePrevious() {
    if (currentQuestionIndex > 0) setCurrentQuestionIndex((prev) => prev - 1)
  }

  async function handleNext() {
    const followUpAdded = await maybeGenerateFollowUp()
    if (followUpAdded || currentQuestionIndex < session.questions.length - 1) {
      setCurrentQuestionIndex((prev) => prev + 1)
    }
  }

  async function handleFinishOrContinue() {
    const followUpAdded = await maybeGenerateFollowUp()
    if (followUpAdded) {
      setCurrentQuestionIndex((prev) => prev + 1)
      return
    }
    await handleFinishInterview()
  }

  async function handleFinishInterview() {
    try {
      await finishPiSession(sessionId)
    } catch (err) {
      console.log('Failed to mark PI session as finished:', err)
    }
    navigate(`/pi/${sessionId}/results`)
  }

  const isLastQuestion = currentQuestionIndex === session.questions.length - 1
  const isCurrentAnswered = answeredQuestions.has(currentQuestion.id)

  async function handleExitFeedbackSubmit(payload) {
    await submitPiSessionFeedback(sessionId, payload)
    navigate('/dashboard')
  }

  function handleExitSkip() {
    navigate('/dashboard')
  }

  return (
    <div className="page-container">
      {!disclaimerAcknowledged && <PreInterviewDisclaimerModal onAcknowledge={() => setDisclaimerAcknowledged(true)} />}

      {disclaimerAcknowledged && deliveryConsent === null && !calibrating && (
        <DeliveryConsentModal onContinue={handleContinueDelivery} onDecline={handleDeclineDelivery} />
      )}

      {calibrating && <DeliveryCalibrationScreen durationMs={CALIBRATION_MS} />}

      <WebcamMonitor stream={webcamStream} />

      {showExitFeedback && <ExitFeedbackModal onSubmit={handleExitFeedbackSubmit} onSkip={handleExitSkip} />}

      <div className="pi-session-header">
        <div>
          <h1>AI Personal Interview Practice</h1>
          <p className="text-muted">
            Question {currentMainQuestionNumber} of {totalMainQuestions}
          </p>
          <div className="pi-progress-dots">
            {mainQuestions.map((question, index) => {
              let state = 'open'
              if (index === currentMainIndex) state = 'current'
              else if (answeredQuestions.has(question.id)) state = 'done'
              return <span key={question.id} className={`pi-dot pi-dot--${state}`} />
            })}
          </div>
        </div>
        <button type="button" className="btn btn-ghost btn-sm" onClick={() => setShowExitFeedback(true)}>
          Exit interview
        </button>
      </div>

      <QuestionCard questionText={currentQuestion.question_text} isFollowUp={currentQuestion.is_follow_up} ttsEnabled={interviewReady} />

      <AnswerBox
        ref={answerBoxRef}
        key={currentQuestion.id}
        onSubmit={handleAnswer}
        onSubmittingChange={setIsSubmittingAnswer}
        disabled={isCurrentAnswered}
        getDeliverySignals={getDeliverySignals}
        onRecordingStateChange={handleRecordingStateChange}
      />

      {currentFeedback && <FeedbackCard {...currentFeedback} />}

      <div className="pi-session-footer">
        <button type="button" className="btn btn-secondary" onClick={handlePrevious} disabled={currentQuestionIndex === 0}>
          ← Previous
        </button>

        {!isCurrentAnswered ? (
          <button type="button" className="btn btn-primary" onClick={() => answerBoxRef.current?.submit()} disabled={isSubmittingAnswer}>
            {isSubmittingAnswer ? 'Submitting...' : 'Submit answer'}
          </button>
        ) : isLastQuestion ? (
          <button type="button" className="btn btn-primary" onClick={handleFinishOrContinue} disabled={generatingFollowUp}>
            {generatingFollowUp ? 'Checking for follow-up...' : 'Finish Interview'}
          </button>
        ) : (
          <button type="button" className="btn btn-primary" onClick={handleNext} disabled={generatingFollowUp}>
            {generatingFollowUp ? 'Checking for follow-up...' : 'Next Question →'}
          </button>
        )}
      </div>

      <p className="text-muted">
        <Link to="/dashboard">Back to dashboard</Link>
      </p>
    </div>
  )
}
