import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import PortalHeader from './PortalHeader.jsx'
import '../Portal.css'
import '../UseCases.css'

// ------------------------------------------------------------
// Frame for every role's use case page: header, back link, title,
// then the page's own content. `result` is the useApiData() reply;
// while it isn't ready, this shows loading or the server's error.
// ------------------------------------------------------------

function UseCaseLayout({ title, subtitle, result, children }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const role = roles[user.role]

  function signInAgain() {
    logout()
    navigate('/login')
  }

  let status = null
  if (!result.data) {
    status = <p className="uc-muted">Loading…</p>
  } else if (result.status === 401) {
    status = (
      <div className="uc-alert" role="alert">
        <strong>{result.data.message || 'Please sign in.'}</strong>
        <p>
          Live data needs a database sign-in. Make sure the API is running (python src/app.py) and
          that USE_TEST_USERS is false in src/auth/authApi.js, then sign in again.
        </p>
        <button type="button" className="logout-button" onClick={signInAgain}>Sign in again</button>
      </div>
    )
  } else if (result.status === 403) {
    status = (
      <div className="uc-alert" role="alert">
        <span className="denied-icon" aria-hidden="true">⛔</span>
        <strong>Access denied by the server (403)</strong>
        <p>{result.data.message}</p>
      </div>
    )
  } else if (result.status !== 200) {
    status = (
      <div className="uc-alert" role="alert">
        <strong>{result.data.message || 'Something went wrong.'}</strong>
      </div>
    )
  }

  return (
    <div className="portal-shell">
      <PortalHeader />
      <main className="portal-main">
        <Link to={role.home} className="back-link">← Back to dashboard</Link>
        <h1 className="portal-title">{title}</h1>
        <p className="portal-subtitle">{subtitle}</p>
        {status || children}
      </main>
    </div>
  )
}

export default UseCaseLayout
