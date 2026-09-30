import { Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import CatOnboardingPage from './pages/CatOnboardingPage'
import DashboardPage from './pages/DashboardPage'
import CatMockTestSetupPage from './pages/CatMockTestSetupPage'
import CatPyqSetupPage from './pages/CatPyqSetupPage'
import CatMockTestSessionPage from './pages/CatMockTestSessionPage'
import CatMockTestResultsPage from './pages/CatMockTestResultsPage'
import CatPiSessionPage from './pages/CatPiSessionPage'
import CatWeakConceptsPage from './pages/CatWeakConceptsPage'

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />

      <Route
        path="/onboarding"
        element={
          <ProtectedRoute>
            <CatOnboardingPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/mock-tests/new"
        element={
          <ProtectedRoute>
            <CatMockTestSetupPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/pyq-tests"
        element={
          <ProtectedRoute>
            <CatPyqSetupPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/mock-tests/:sessionId"
        element={
          <ProtectedRoute>
            <CatMockTestSessionPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/mock-tests/:sessionId/results"
        element={
          <ProtectedRoute>
            <CatMockTestResultsPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/pi"
        element={
          <ProtectedRoute>
            <CatPiSessionPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/pi/:sessionId"
        element={
          <ProtectedRoute>
            <CatPiSessionPage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/weak-concepts"
        element={
          <ProtectedRoute>
            <CatWeakConceptsPage />
          </ProtectedRoute>
        }
      />

      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
