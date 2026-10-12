import SessionFeedbackForm from './SessionFeedbackForm'

export default function ExitFeedbackModal({ onSubmit, onSkip }) {
  return (
    <div className="pi-modal-overlay">
      <SessionFeedbackForm onSubmit={onSubmit} onSkip={onSkip} />
    </div>
  )
}
