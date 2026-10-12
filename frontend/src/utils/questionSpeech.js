// Thin wrapper around the browser's native Web Speech Synthesis API (the "speak text
// aloud" counterpart to VoiceInput.jsx's speech *recognition*). Fully client-side, no
// backend/Gemini cost.
const SPEECH_LANG = 'en-US'
const SPEECH_RATE = 0.92
const SPEECH_PITCH = 0.95

export function isSpeechSupported() {
  return typeof window !== 'undefined' && 'speechSynthesis' in window
}

// Cancels any in-flight utterance first, so rapid question changes never overlap/garble
// two voices at once.
export function speak(text, { onStart, onEnd } = {}) {
  if (!isSpeechSupported() || !text) return

  window.speechSynthesis.cancel()

  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = SPEECH_LANG
  utterance.rate = SPEECH_RATE
  utterance.pitch = SPEECH_PITCH

  if (onStart) utterance.onstart = onStart
  if (onEnd) utterance.onend = onEnd
  utterance.onerror = onEnd

  window.speechSynthesis.speak(utterance)
}

export function stopSpeaking() {
  if (isSpeechSupported()) {
    window.speechSynthesis.cancel()
  }
}
