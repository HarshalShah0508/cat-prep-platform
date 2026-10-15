import { NavLink, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import ThemeToggle from './ui/ThemeToggle'

const EXAM_ROUTE = /^\/mock-tests\/\d+$/
const PI_SESSION_ROUTE = /^\/pi\/\d+$/

function initialsFor(name) {
  if (!name) return '?'
  return name.trim().slice(0, 2).toUpperCase()
}

export default function Navbar() {
  const { isAuthenticated, user, logout, promptLogin } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  // Locked down during an active test or a live (recording) PI session - no
  // navigating away except each page's own "Exit" control, same as a real
  // exam interface.
  if (EXAM_ROUTE.test(location.pathname) || PI_SESSION_ROUTE.test(location.pathname)) {
    return null
  }

  function handleLogout() {
    logout()
    navigate('/login')
  }

  function gateClick(e) {
    if (!isAuthenticated) {
      e.preventDefault()
      promptLogin()
    }
  }

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <NavLink to="/dashboard" className="navbar-brand">
          CAT<span className="navbar-brand-accent">Prep</span>
        </NavLink>
        <nav className="navbar-links">
          <NavLink to="/dashboard" className={({ isActive }) => (isActive ? 'active' : '')}>
            Dashboard
          </NavLink>
          <NavLink to="/mock-tests/new" onClick={gateClick} className={({ isActive }) => (isActive ? 'active' : '')}>
            Mock Tests
          </NavLink>
          <NavLink to="/pyq-tests" onClick={gateClick} className={({ isActive }) => (isActive ? 'active' : '')}>
            PYQ Practice
          </NavLink>
          <NavLink to="/pi/new" onClick={gateClick} className={({ isActive }) => (isActive ? 'active' : '')}>
            Personal Interview
          </NavLink>
          <NavLink to="/weak-concepts" onClick={gateClick} className={({ isActive }) => (isActive ? 'active' : '')}>
            Weak Concepts
          </NavLink>
          <NavLink to="/study-plan" onClick={gateClick} className={({ isActive }) => (isActive ? 'active' : '')}>
            Study Plan
          </NavLink>
        </nav>
        <div className="navbar-user">
          <ThemeToggle />
          {isAuthenticated ? (
            <>
              {user && <span className="ui-avatar" title={user.username}>{initialsFor(user.username)}</span>}
              <button type="button" className="btn btn-ghost btn-sm" onClick={handleLogout}>
                Log out
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className="btn btn-ghost btn-sm">
                Log in
              </NavLink>
              <NavLink to="/signup" className="btn btn-primary btn-sm">
                Sign up
              </NavLink>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
