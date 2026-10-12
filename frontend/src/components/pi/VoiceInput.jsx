import { useEffect, useRef, useState } from 'react'

export default function VoiceInput({ value, onChange, disabled = false, onRecordingStateChange }) {
  const recognitionRef = useRef(null)
  const shouldContinueRef = useRef(false)

  const [supported, setSupported] = useState(false)
  const [isListening, setIsListening] = useState(false)
  const [hasStartedOnce, setHasStartedOnce] = useState(false)

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition

    if (!SpeechRecognition) {
      setSupported(false)
      return
    }

    setSupported(true)

    const recognition = new SpeechRecognition()
    recognition.continuous = true
    recognition.interimResults = true
    recognition.lang = 'en-US'

    recognition.onresult = (event) => {
      let transcript = ''
      for (let i = event.resultIndex; i < event.results.length; i++) {
        if (event.results[i].isFinal) {
          transcript += event.results[i][0].transcript + ' '
        }
      }
      transcript = transcript.trim()
      if (!transcript) return

      onChange((previous) => (previous ? `${previous.trim()} ${transcript}` : transcript))
    }

    recognition.onstart = () => setIsListening(true)

    recognition.onend = () => {
      setIsListening(false)
      if (shouldContinueRef.current && !disabled) {
        recognition.start()
      }
    }

    recognition.onerror = (event) => {
      if (event.error === 'no-speech') return
      setIsListening(false)
    }

    recognitionRef.current = recognition

    return () => {
      shouldContinueRef.current = false
      recognition.stop()
    }
  }, [onChange, disabled])

  useEffect(() => {
    onRecordingStateChange?.(isListening)
  }, [isListening, onRecordingStateChange])

  const startListening = () => {
    if (!recognitionRef.current || disabled || isListening) return
    shouldContinueRef.current = true
    recognitionRef.current.start()
    setHasStartedOnce(true)
  }

  const stopListening = () => {
    shouldContinueRef.current = false
    recognitionRef.current?.stop()
  }

  return (
    <div className="pi-voice-block">
      <div className="pi-voice-block__header">
        <span className="form-label">Your answer</span>
        {isListening && (
          <span className="badge badge-error pi-recording-badge">
            <span className="pi-recording-dot" />
            Recording
          </span>
        )}
      </div>

      {!supported && <p className="text-muted">Speech recognition isn't supported in this browser.</p>}

      <textarea
        rows={6}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        placeholder="Speak, or type your answer..."
      />

      <div className="pi-voice-button-row">
        <button type="button" className="btn btn-ghost btn-sm" onClick={startListening} disabled={disabled || !supported || isListening}>
          {hasStartedOnce ? 'Resume recording' : 'Start recording'}
        </button>
        <button type="button" className="btn btn-ghost btn-sm" onClick={stopListening} disabled={disabled || !isListening}>
          Stop recording
        </button>
      </div>
    </div>
  )
}
