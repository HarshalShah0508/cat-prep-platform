import { useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function LoginPromptModal() {
  const { showLoginPrompt, dismissLoginPrompt } = useAuth()
  const navigate = useNavigate()

  if (!showLoginPrompt) return null

  function goTo(path) {
    dismissLoginPrompt()
    navigate(path)
  }

  return (
    <div className="pi-modal-overlay">
      <div className="card pi-modal-card">
        <h2>Log in to continue</h2>
        <p className="text-muted">
          Create a free account or log in to start mock tests, PYQ practice, PI practice, and
          weak-concept tracking.
        </p>
        <div className="pi-modal-actions">
          <button type="button" className="btn btn-primary" onClick={() => goTo('/login')}>
            Log in
          </button>
          <button type="button" className="btn btn-secondary" onClick={() => goTo('/signup')}>
            Create account
          </button>
          <button type="button" className="btn btn-ghost" onClick={dismissLoginPrompt}>
            Not now
          </button>
        </div>
      </div>
    </div>
  )
}
