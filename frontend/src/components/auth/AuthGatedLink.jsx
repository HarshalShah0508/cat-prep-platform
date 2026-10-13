import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'

export default function AuthGatedLink({ to, onClick, children, ...rest }) {
  const { isAuthenticated, promptLogin } = useAuth()

  function handleClick(e) {
    if (!isAuthenticated) {
      e.preventDefault()
      promptLogin()
      return
    }
    onClick?.(e)
  }

  return (
    <Link to={to} onClick={handleClick} {...rest}>
      {children}
    </Link>
  )
}
