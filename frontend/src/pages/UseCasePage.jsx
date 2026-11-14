import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import PortalHeader from '../components/PortalHeader.jsx'
import '../Portal.css'

// ------------------------------------------------------------
// Placeholder for each role's Sprint IV retrieval use case.
// The teammate who owns the use case replaces this with the
// real page that loads data from the database.
// ------------------------------------------------------------

function UseCasePage({ title, description }) {
  const { user } = useAuth()
  const role = roles[user.role]

  return (
    <div className="portal-shell">
      <PortalHeader />

      <main className="portal-main">
        <Link to={role.home} className="back-link">← Back to dashboard</Link>
        <h1 className="portal-title">{title}</h1>
        <p className="portal-subtitle">{description}</p>

        <div className="placeholder-box">
          This page will list data from the PetMed database.
        </div>
      </main>
    </div>
  )
}

export default UseCasePage
