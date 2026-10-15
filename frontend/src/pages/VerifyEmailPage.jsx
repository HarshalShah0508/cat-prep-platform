import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { verifyEmail, resendVerification } from '../api/authApi'
import AuthLayout from '../components/auth/AuthLayout'

export default function VerifyEmailPage() {
  const { completeAuth } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState(location.state?.email || '')
  const [notice] = useState(location.state?.notice || '')
  const [otpCode, setOtpCode] = useState('')
  const [error, setError] = useState('')
  const [info, setInfo] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [resending, setResending] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setInfo('')

    if (!email || !otpCode) {
      setError('Please enter both your email and the verification code.')
      return
    }

    setSubmitting(true)
    try {
      const data = await verifyEmail({ email, otp_code: otpCode })
      completeAuth(data)
      navigate('/onboarding')
    } catch (err) {
      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Could not verify your email. Please try again.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  async function handleResend() {
    setError('')
    setInfo('')
    if (!email) {
      setError('Please enter your email first.')
      return
    }

    setResending(true)
    try {
      const data = await resendVerification({ email })
      setInfo(data.message)
    } catch (err) {
      const message = err?.response?.data?.detail || 'Could not resend the code. Please try again shortly.'
      setError(message)
    } finally {
      setResending(false)
    }
  }

  return (
    <AuthLayout
      eyebrow="Almost there"
      title="Verify your email"
      body="We sent a 6-digit code to your inbox. Enter it below to activate your account."
    >
      <div className="ui-card auth-card">
        <h1>Enter verification code</h1>
        <p className="text-muted">Check your inbox for the code we just sent.</p>

        {notice && <div className="alert alert-error">{notice}</div>}
        {error && <div className="alert alert-error">{error}</div>}
        {info && <div className="alert alert-success">{info}</div>}

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

          <div className="form-group">
            <label htmlFor="otpCode">6-digit code</label>
            <input
              id="otpCode"
              type="text"
              inputMode="numeric"
              maxLength={6}
              value={otpCode}
              onChange={(e) => setOtpCode(e.target.value.replace(/\D/g, ''))}
              placeholder="123456"
            />
          </div>

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Verifying...' : 'Verify email'}
          </button>
        </form>

        <p className="auth-switch">
          Didn't get a code?{' '}
          <button type="button" className="btn-link" onClick={handleResend} disabled={resending}>
            {resending ? 'Resending...' : 'Resend code'}
          </button>
        </p>
        <p className="auth-switch">
          <Link to="/login">Back to login</Link>
        </p>
      </div>
    </AuthLayout>
  )
}
