import { createContext, useCallback, useContext, useState } from 'react'

const CatPiContext = createContext(null)

const STORAGE_KEY = 'cat_pi_session_id'

// Mirrors CatMockTestContext's shape (sessionId/status/trackSession/clearSession) even
// though PI session generation is synchronous today - keeps a future upgrade to
// background-job + polling generation a drop-in rather than a rewrite.
export function CatPiProvider({ children }) {
  const [sessionId, setSessionId] = useState(() => localStorage.getItem(STORAGE_KEY) || null)
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)

  const trackSession = useCallback((id, initialStatus) => {
    setSessionId(id)
    setStatus(initialStatus || 'in_progress')
    setError(null)
    localStorage.setItem(STORAGE_KEY, id)
  }, [])

  const clearSession = useCallback(() => {
    setSessionId(null)
    setStatus(null)
    setError(null)
    localStorage.removeItem(STORAGE_KEY)
  }, [])

  const value = {
    sessionId,
    status,
    error,
    trackSession,
    clearSession,
  }

  return <CatPiContext.Provider value={value}>{children}</CatPiContext.Provider>
}

export function useCatPi() {
  const ctx = useContext(CatPiContext)
  if (!ctx) {
    throw new Error('useCatPi must be used within a CatPiProvider')
  }
  return ctx
}
