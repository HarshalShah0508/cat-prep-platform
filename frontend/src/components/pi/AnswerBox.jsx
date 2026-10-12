import { forwardRef, useImperativeHandle, useState } from 'react'
import VoiceInput from './VoiceInput'

// Unlike InterviewAI's AnswerBox, this one doesn't call the API itself - it hands the
// answer text + delivery signals to the parent (CatPiSessionPage) via onSubmit, which
// owns the actual request/error/follow-up orchestration. Also has no coding-related
// branches (CodeEditor/CustomInput/ConsoleOutput) - PI never had a coding mode.
const AnswerBox = forwardRef(function AnswerBox(
  { onSubmit, onSubmittingChange, disabled = false, getDeliverySignals, onRecordingStateChange },
  ref,
) {
  const [answerText, setAnswerText] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const handleSubmit = async (event) => {
    if (event) event.preventDefault()
    if (disabled || submitting || !answerText.trim()) {
      if (!answerText.trim()) setError('Please provide an answer.')
      return
    }

    try {
      setSubmitting(true)
      onSubmittingChange?.(true)
      setError('')

      const deliverySignals = getDeliverySignals?.() ?? null
      await onSubmit(answerText.trim(), deliverySignals)
      setAnswerText('')
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to submit your answer.')
    } finally {
      setSubmitting(false)
      onSubmittingChange?.(false)
    }
  }

  useImperativeHandle(ref, () => ({
    submit: () => handleSubmit(),
  }))

  return (
    <form className="card" onSubmit={handleSubmit}>
      <VoiceInput value={answerText} onChange={setAnswerText} disabled={disabled} onRecordingStateChange={onRecordingStateChange} />
      {error && <div className="alert alert-error">{error}</div>}
    </form>
  )
})

export default AnswerBox
