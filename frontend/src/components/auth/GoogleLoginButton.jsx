import { GoogleLogin } from '@react-oauth/google'
import { useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { redirectAfterAuth } from '../../utils/postAuthRedirect'

export default function GoogleLoginButton({ onError }) {
  const { googleLogin } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  async function handleSuccess(credentialResponse) {
    try {
      if (!credentialResponse?.credential) {
        throw new Error('Google did not return an ID token.')
      }
      await googleLogin(credentialResponse.credential)
      const redirectTo = location.state?.from?.pathname
      await redirectAfterAuth(navigate, redirectTo)
    } catch (err) {
      const message = err?.response?.data?.detail || err?.message || 'Google sign-in failed.'
      onError?.(message)
    }
  }

  return (
    <div className="google-login-wrap">
      <GoogleLogin
        onSuccess={handleSuccess}
        onError={() => onError?.('Google Sign-In was cancelled or failed.')}
        shape="rectangular"
        size="large"
        text="continue_with"
        width="360"
      />
    </div>
  )
}
