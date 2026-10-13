import { Link } from 'react-router-dom'
import ThemeToggle from '../ui/ThemeToggle'

export default function AuthLayout({ eyebrow, title, body, preview, children }) {
  return (
    <div className="auth-screen">
      <div className="auth-screen-left">
        <Link to="/" className="navbar-brand">
          CAT<span className="navbar-brand-accent">Prep</span>
        </Link>
        <div className="auth-screen-copy">
          <div className="ui-eyebrow">{eyebrow}</div>
          <h1 className="auth-screen-headline">{title}</h1>
          <p className="auth-screen-body">{body}</p>
        </div>
        {preview && <div className="auth-preview-card">{preview}</div>}
      </div>
      <div className="auth-screen-right">
        <div className="auth-screen-toggle">
          <ThemeToggle />
        </div>
        <div className="auth-screen-form">{children}</div>
      </div>
    </div>
  )
}
