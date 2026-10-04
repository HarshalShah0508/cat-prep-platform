import { NavLink, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const EXAM_ROUTE = /^\/mock-tests\/\d+$/

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()

  // Locked down during an active test - no navigating away except the page's own
  // "Exit Test" control, same as a real exam interface.
  if (!isAuthenticated || EXAM_ROUTE.test(location.pathname)) {
    return null
  }

  function handleLogout() {
    logout()
    navigate('/login')
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
          <NavLink to="/mock-tests/new" className={({ isActive }) => (isActive ? 'active' : '')}>
            Mock Tests
          </NavLink>
          <NavLink to="/pyq-tests" className={({ isActive }) => (isActive ? 'active' : '')}>
            PYQ Practice
          </NavLink>
          <NavLink to="/pi" className={({ isActive }) => (isActive ? 'active' : '')}>
            PI Practice
          </NavLink>
          <NavLink to="/weak-concepts" className={({ isActive }) => (isActive ? 'active' : '')}>
            Weak Concepts
          </NavLink>
        </nav>
        <div className="navbar-user">
          {user && <span className="navbar-username">{user.username}</span>}
          <button type="button" className="btn btn-ghost btn-sm" onClick={handleLogout}>
            Log out
          </button>
        </div>
      </div>
    </header>
  )
}
