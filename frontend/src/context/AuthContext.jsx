import { createContext, useContext, useEffect, useState } from 'react'
import * as authApi from '../api/authApi'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showLoginPrompt, setShowLoginPrompt] = useState(false)

  // Load persisted auth state on first mount. If nothing is stored, the user
  // is simply unauthenticated - ProtectedRoute sends them to /login.
  useEffect(() => {
    const storedToken = localStorage.getItem('access_token')
    const storedUser = localStorage.getItem('cat_user')
    if (storedToken && storedUser) {
      try {
        setToken(storedToken)
        setUser(JSON.parse(storedUser))
      } catch {
        localStorage.removeItem('access_token')
        localStorage.removeItem('cat_user')
      }
    }
    setLoading(false)
  }, [])

  function persist(data) {
    setToken(data.access_token)
    setUser(data.user)
    localStorage.setItem('access_token', data.access_token)
    localStorage.setItem('cat_user', JSON.stringify(data.user))
  }

  async function signup({ email, password, username }) {
    // No token comes back here - the account isn't usable until the email is verified.
    return authApi.signup({ email, password, username })
  }

  async function login({ email, password }) {
    const data = await authApi.login({ email, password })
    persist(data)
    return data
  }

  function completeAuth(data) {
    persist(data)
  }

  async function googleLogin(idToken) {
    const data = await authApi.googleLogin({ id_token: idToken })
    persist(data)
    return data
  }

  function logout() {
    setToken(null)
    setUser(null)
    localStorage.removeItem('access_token')
    localStorage.removeItem('cat_user')
  }

  function promptLogin() {
    setShowLoginPrompt(true)
  }

  function dismissLoginPrompt() {
    setShowLoginPrompt(false)
  }

  const value = {
    user,
    token,
    loading,
    isAuthenticated: Boolean(token && user),
    signup,
    login,
    logout,
    completeAuth,
    googleLogin,
    showLoginPrompt,
    promptLogin,
    dismissLoginPrompt,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return ctx
}
