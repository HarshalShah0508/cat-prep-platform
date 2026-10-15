import { Navigate, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute'
import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import VerifyEmailPage from './pages/VerifyEmailPage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import ResetPasswordPage from './pages/ResetPasswordPage'
import CatOnboardingPage from './pages/CatOnboardingPage'
import DashboardPage from './pages/DashboardPage'
import CatMockTestSetupPage from './pages/CatMockTestSetupPage'
import CatPyqSetupPage from './pages/CatPyqSetupPage'
import CatMockTestSessionPage from './pages/CatMockTestSessionPage'
import CatMockTestResultsPage from './pages/CatMockTestResultsPage'
import CatPiSetupPage from './pages/CatPiSetupPage'
import CatPiSessionPage from './pages/CatPiSessionPage'
import CatPiResultsPage from './pages/CatPiResultsPage'
import CatWeakConceptsPage from './pages/CatWeakConceptsPage'
import CatStudyPlanPage from './pages/CatStudyPlanPage'

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/verify-email" element={<VerifyEmailPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />

      <Route
        path="/onboarding"
        element={
          <ProtectedRoute>
            <CatOnboardingPage />
          </ProtectedRoute>
        }
      />
      <Route path="/dashboard" element={<DashboardPage />} />
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
        path="/pi/new"
        element={
          <ProtectedRoute>
            <CatPiSetupPage />
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
        path="/pi/:sessionId/results"
        element={
          <ProtectedRoute>
            <CatPiResultsPage />
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
      <Route
        path="/study-plan"
        element={
          <ProtectedRoute>
            <CatStudyPlanPage />
          </ProtectedRoute>
        }
      />

      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}
