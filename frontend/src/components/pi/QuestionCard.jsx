import { useEffect, useState } from 'react'
import { speak, stopSpeaking, isSpeechSupported } from '../../utils/questionSpeech'

const TTS_PREFERENCE_KEY = 'cat_pi_read_questions_aloud'

function getStoredPreference() {
  if (typeof window === 'undefined') return true
  const stored = window.localStorage.getItem(TTS_PREFERENCE_KEY)
  return stored === null ? true : stored === 'true'
}

export default function QuestionCard({ questionText, isFollowUp, ttsEnabled = true }) {
  const [readAloud, setReadAloud] = useState(getStoredPreference)
  const [isSpeaking, setIsSpeaking] = useState(false)

  // ttsEnabled is deliberately a dependency here (not just a guard) - it starts false
  // while the delivery consent/calibration overlay is up, then flips to true once that
  // resolves, so the first question gets spoken then instead of the instant the page
  // mounted.
  useEffect(() => {
    if (!readAloud || !ttsEnabled) return

    speak(questionText, {
      onStart: () => setIsSpeaking(true),
      onEnd: () => setIsSpeaking(false),
    })

    return () => stopSpeaking()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [questionText, isFollowUp, ttsEnabled])

  useEffect(() => {
    return () => stopSpeaking()
  }, [])

  const handleToggleReadAloud = () => {
    const next = !readAloud
    setReadAloud(next)
    window.localStorage.setItem(TTS_PREFERENCE_KEY, String(next))

    if (!next) {
      stopSpeaking()
      setIsSpeaking(false)
    }
  }

  const handleReplayOrStop = () => {
    if (isSpeaking) {
      stopSpeaking()
      setIsSpeaking(false)
    } else {
      speak(questionText, {
        onStart: () => setIsSpeaking(true),
        onEnd: () => setIsSpeaking(false),
      })
    }
  }

  return (
    <div className="card question-card">
      {isFollowUp && (
        <div className="pi-followup-banner">
          <span className="badge badge-warning">FOLLOW-UP</span>
          <span>The panel is digging deeper into your previous answer.</span>
        </div>
      )}

      {isSpeaking && (
        <span className="badge badge-muted pi-speaking-badge">Speaking…</span>
      )}

      <p className="question-text">{questionText}</p>

      {isSpeechSupported() && (
        <div className="pi-voice-controls">
          <button type="button" className="btn btn-ghost btn-sm" onClick={handleReplayOrStop}>
            {isSpeaking ? 'Stop' : 'Replay question'}
          </button>

          <label className="pi-voice-toggle">
            <input type="checkbox" checked={readAloud} onChange={handleToggleReadAloud} />
            Read questions aloud
          </label>
        </div>
      )}
    </div>
  )
}
