import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import logo from '../assets/petmed-logo.png'

// ------------------------------------------------------------
// Navy sidebar shown on every signed in page: logo, the role's
// menu (working features are links, the rest say "Soon"), and
// the signed in user with Log Out. On phones it becomes a top bar.
// ------------------------------------------------------------

function PortalHeader() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const role = roles[user.role]

  function handleLogout() {
    logout()
    navigate('/')
  }

  return (
    <aside className="sidebar" aria-label={`${role.label} navigation`}>
      <Link to={role.home} className="sidebar-brand">
        <img src={logo} alt="" aria-hidden="true" />
        <span>PetMed</span>
      </Link>

      <p className="sidebar-role">{role.label}</p>

      <nav className="sidebar-nav">
        <NavLink to={role.home} end className="sidebar-link">
          <span aria-hidden="true">🏠</span> Home
        </NavLink>
        {role.menu.map((item) =>
          item.path ? (
            <NavLink key={item.title} to={item.path} className="sidebar-link">
              <span aria-hidden="true">{item.icon}</span> {item.title}
            </NavLink>
          ) : (
            <span key={item.title} className="sidebar-link sidebar-link-soon" aria-disabled="true">
              <span aria-hidden="true">{item.icon}</span> {item.title}
              <small>Soon</small>
            </span>
          )
        )}
      </nav>

      <div className="sidebar-user">
        <span className="sidebar-avatar" aria-hidden="true">{user.name[0]}</span>
        <div className="sidebar-user-text">
          <strong>{user.name}</strong>
          <small>{user.email}</small>
        </div>
        <button type="button" className="logout-button" onClick={handleLogout}>Log Out</button>
      </div>
    </aside>
  )
}

export default PortalHeader
