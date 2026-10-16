import client from './client'

export function signup({ email, password, username }) {
  return client.post('/auth/signup', { email, password, username }).then((res) => res.data)
}

export function login({ email, password }) {
  return client.post('/auth/login', { email, password }).then((res) => res.data)
}

export function googleLogin({ id_token }) {
  return client.post('/auth/google', { id_token }).then((res) => res.data)
}

export function verifyEmail({ email, otp_code }) {
  return client.post('/auth/verify-email', { email, otp_code }).then((res) => res.data)
}

export function resendVerification({ email }) {
  return client.post('/auth/resend-verification', { email }).then((res) => res.data)
}

export function forgotPassword({ email }) {
  return client.post('/auth/forgot-password', { email }).then((res) => res.data)
}

export function resetPassword({ email, otp_code, new_password }) {
  return client.post('/auth/reset-password', { email, otp_code, new_password }).then((res) => res.data)
}
