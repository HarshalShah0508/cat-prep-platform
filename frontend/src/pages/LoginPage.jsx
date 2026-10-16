import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import AuthLayout from '../components/auth/AuthLayout'
import GoogleLoginButton from '../components/auth/GoogleLoginButton'
import { redirectAfterAuth } from '../utils/postAuthRedirect'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')

    if (!email || !password) {
      setError('Please enter both email and password.')
      return
    }

    setSubmitting(true)
    try {
      await login({ email, password })
      const redirectTo = location.state?.from?.pathname
      await redirectAfterAuth(navigate, redirectTo)
    } catch (err) {
      if (err?.response?.status === 403 && err?.response?.data?.detail === 'EMAIL_NOT_VERIFIED') {
        navigate('/verify-email', {
          state: { email, notice: 'Please verify your email before logging in. Enter the code below to continue.' },
        })
        return
      }
      if (
        err?.response?.status === 401 &&
        err?.response?.data?.detail === 'This account was created using Google Sign-In. Please continue with Google.'
      ) {
        setError(err.response.data.detail)
        return
      }
      const message =
        err?.response?.data?.detail ||
        err?.response?.data?.message ||
        'Login failed. Check your credentials and try again.'
      setError(message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <AuthLayout
      eyebrow="Welcome back"
      title="Keep the streak going"
      body="Pick up right where you left off - your mock tests, PI practice, and weak-concept tracking are all waiting."
      preview={
        <>
          <div className="ui-eyebrow">Last mock test</div>
          <div className="ui-slab-stat-value" style={{ fontSize: '1.6rem' }}>94.2</div>
          <div className="ui-slab-stat-label">percentile estimate</div>
        </>
      }
    >
      <div className="ui-card auth-card">
        <h1>Log in</h1>
        <p className="text-muted">Log in to keep prepping for CAT.</p>

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

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              placeholder="••••••••"
            />
          </div>

          <p className="auth-switch" style={{ textAlign: 'right', marginTop: '-0.5rem' }}>
            <Link to="/forgot-password">Forgot password?</Link>
          </p>

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? 'Logging in...' : 'Log in'}
          </button>
        </form>

        <div className="auth-divider">
          <span className="auth-divider-line" />
          <span className="auth-divider-text">OR</span>
          <span className="auth-divider-line" />
        </div>

        <GoogleLoginButton onError={setError} />

        <p className="auth-switch">
          New here? <Link to="/signup">Create an account</Link>
        </p>
      </div>
    </AuthLayout>
  )
}
