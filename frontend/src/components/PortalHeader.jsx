import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import logo from '../assets/petmed-logo.png'

// Top bar shown on every signed in page: logo, user name, role and Log Out
function PortalHeader() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const role = roles[user.role]

  function handleLogout() {
    logout()
    navigate('/')
  }

  return (
    <header className="portal-header">
      <Link to={role.home} className="brand">
        <img className="brand-mark" src={logo} alt="" aria-hidden="true" />
        <span>PetMed</span>
      </Link>

      <div className="portal-user">
        <div className="portal-user-text">
          <strong>{user.name}</strong>
          <span className="role-badge">{role.label}</span>
        </div>
        <button type="button" className="logout-button" onClick={handleLogout}>Log Out</button>
      </div>
    </header>
  )
}

export default PortalHeader
