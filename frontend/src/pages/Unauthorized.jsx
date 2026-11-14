import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import '../Portal.css'

// Shown when a signed in user opens a page their role cannot use
function Unauthorized() {
  const { user } = useAuth()
  const home = user ? roles[user.role].home : '/login'

  return (
    <div className="login-shell">
      <div className="login-card">
        <div className="denied-icon" aria-hidden="true">⛔</div>
        <h1 className="login-title">Access denied</h1>
        <p className="login-subtitle">
          Your account does not have permission to view that page.
        </p>
        <Link to={home} className="primary-button login-button">Go to my dashboard</Link>
      </div>
    </div>
  )
}

export default Unauthorized
