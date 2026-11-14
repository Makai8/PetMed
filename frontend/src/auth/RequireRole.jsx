import { Navigate } from 'react-router-dom'
import { useAuth } from './AuthContext.jsx'

// ------------------------------------------------------------
// Route guard.
// Not signed in       -> sent to the login page
// Signed in, wrong role -> sent to the Access Denied page
// Right role          -> page is shown
// ------------------------------------------------------------

function RequireRole({ role, children }) {
  const { user } = useAuth()

  if (!user) {
    return <Navigate to="/login" replace />
  }
  if (user.role !== role) {
    return <Navigate to="/unauthorized" replace />
  }
  return children
}

export default RequireRole
