import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { forgotPassword } from '../api/authApi'
import AuthLayout from '../components/auth/AuthLayout'

export default function ForgotPasswordPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!email) {
      setError('Please enter your email.')
      return
    }

    setSubmitting(true)
    try {
      await forgotPassword({ email })
      navigate('/reset-password', { state: { email } })
    } catch (err) {
      const message = err?.response?.data?.detail || 'Something went wrong. Please try again.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthLayout
      eyebrow="Forgot password"
      title="Reset your password"
      body="Enter your email and we'll send you a 6-digit code to reset your password."
    >
      <div className="ui-card auth-card">
        <h1>Forgot password</h1>
        <p className="text-muted">We'll email you a code to reset your password.</p>

        {error && <div className="alert alert-error">{error}</div>}

        <form onSubmit={handleSubmit} noValidate>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              placeholder="you@example.com"
            />
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Sending...' : 'Send reset code'}
          </button>
        </form>

        <p className="auth-switch">
          <Link to="/login">Back to login</Link>
        </p>
      </div>
    </AuthLayout>
  )
}
