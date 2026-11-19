import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import PortalHeader from '../components/PortalHeader.jsx'
import WelcomeSplash from '../components/WelcomeSplash.jsx'
import RoleHome from '../components/RoleHome.jsx'
import '../Portal.css'

// ------------------------------------------------------------
// Landing and navigation screen.
// One component, five screens: the menu comes from roles.js
// based on the signed in user's role.
// ------------------------------------------------------------

function Dashboard() {
  const { user } = useAuth()
  const role = roles[user.role]
  // Doctors are greeted by last name, everyone else by first name
  const parts = user.name.split(' ')
  const greetingName = parts[0] === 'Dr.' ? `Dr. ${parts[parts.length - 1]}` : parts[0]
  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 18 ? 'Good afternoon' : 'Good evening'

  return (
    <div className="portal-shell">
      <WelcomeSplash />
      <PortalHeader />

      <main className="portal-main">
        <p className="eyebrow">{role.label.toUpperCase()} DASHBOARD</p>
        <h1 className="portal-title">{greeting}, {greetingName}.</h1>
        <p className="portal-subtitle">{role.welcome}</p>

        <RoleHome />

        <div className="menu-grid">
          {role.menu.map((item) =>
            item.path ? (
              <Link key={item.title} to={item.path} className="menu-card menu-card-active">
                <span className="menu-icon" aria-hidden="true">{item.icon}</span>
                <strong>{item.title}</strong>
                <small>{item.text}</small>
                <span className="menu-tag">Open</span>
              </Link>
            ) : (
              <div key={item.title} className="menu-card menu-card-soon" aria-disabled="true">
                <span className="menu-icon" aria-hidden="true">{item.icon}</span>
                <strong>{item.title}</strong>
                <small>{item.text}</small>
                <span className="menu-tag menu-tag-soon">Coming soon</span>
              </div>
            )
          )}
        </div>
      </main>
    </div>
  )
}

export default Dashboard
