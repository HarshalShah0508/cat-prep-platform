import { createContext, useCallback, useContext, useEffect, useRef, useState } from 'react'
import { getMockTestStatus } from '../api/catMockTestApi'

const CatMockTestContext = createContext(null)

const STORAGE_KEY = 'cat_mock_test_session_id'

export function CatMockTestProvider({ children }) {
  const [sessionId, setSessionId] = useState(() => localStorage.getItem(STORAGE_KEY) || null)
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)
  const pollRef = useRef(null)

  // Start (or resume) tracking a generation job.
  const trackSession = useCallback((id, initialStatus) => {
    setSessionId(id)
    setStatus(initialStatus || 'generating')
    setError(null)
    localStorage.setItem(STORAGE_KEY, id)
  }, [])

  const clearSession = useCallback(() => {
    setSessionId(null)
    setStatus(null)
    setError(null)
    localStorage.removeItem(STORAGE_KEY)
  }, [])

  // Poll status every 2s while a session is tracked and still generating.
  useEffect(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current)
      pollRef.current = null
    }

    if (!sessionId) return undefined

    let cancelled = false

    async function poll() {
      try {
        const data = await getMockTestStatus(sessionId)
        if (cancelled) return
        setStatus(data.status)
        if (data.status !== 'generating' && pollRef.current) {
          clearInterval(pollRef.current)
          pollRef.current = null
        }
      } catch (err) {
        if (cancelled) return
        setError(err)
        if (pollRef.current) {
          clearInterval(pollRef.current)
          pollRef.current = null
        }
      }
    }

    poll()
    pollRef.current = setInterval(poll, 2000)

    return () => {
      cancelled = true
      if (pollRef.current) {
        clearInterval(pollRef.current)
        pollRef.current = null
      }
    }
  }, [sessionId])

  const value = {
    sessionId,
    status,
    error,
    trackSession,
    clearSession,
  }

  return <CatMockTestContext.Provider value={value}>{children}</CatMockTestContext.Provider>
}

export function useCatMockTest() {
  const ctx = useContext(CatMockTestContext)
  if (!ctx) {
    throw new Error('useCatMockTest must be used within a CatMockTestProvider')
  }
  return ctx
}
