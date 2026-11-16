import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { apiPost } from '../api/petmedApi.js'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import logo from '../assets/petmed-logo.png'
import '../Portal.css'

// ------------------------------------------------------------
// Sign up page: creates a Pet Owner account in the database
// (POST /api/signup, src/routes/signup.py), then signs the new
// user in. Veterinarians and experts are added by an administrator.
// ------------------------------------------------------------

function Signup() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Already signed in, skip the form
  if (user) {
    return <Navigate to={roles[user.role].home} replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    if (!fullName.trim() || !email.trim() || !password) {
      setError('Enter your name, email and password.')
      return
    }
    if (password !== confirm) {
      setError('The two passwords do not match.')
      return
    }

    setLoading(true)
    const res = await apiPost('/signup', { full_name: fullName, email, password })
    if (!res.ok) {
      setLoading(false)
      setError(res.data.message || 'Could not create the account.')
      return
    }

    // Account created: sign in with it right away, then offer the
    // optional step of requesting a professional or staff role
    try {
      await login(email, password)
      navigate('/request-role?new=1')
    } catch {
      navigate('/login')
    }
  }

  return (
    <div className="login-shell">
      <div className="login-card">
        <Link to="/" className="login-logo">
          <img src={logo} alt="PetMed logo" />
        </Link>
        <h1 className="login-title">Create your account</h1>
        <p className="login-subtitle">Join PetMed as a pet owner</p>

        <form onSubmit={handleSubmit} noValidate>
          <label htmlFor="fullName">Full name</label>
          <input
            id="fullName"
            type="text"
            placeholder="Your name"
            value={fullName}
            onChange={(e) => setFullName(e.target.value)}
            autoComplete="name"
          />

          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="email"
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="At least 8 characters"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="new-password"
          />
          <p className="login-hint">Use at least 8 characters, with a letter and a number.</p>

          <label htmlFor="confirm">Confirm password</label>
          <input
            id="confirm"
            type="password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
            autoComplete="new-password"
          />

          {error && <p className="login-error" role="alert">{error}</p>}

          <button type="submit" className="primary-button login-button" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <p className="login-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
        <p className="login-hint">Veterinarians and pet health experts: contact a PetMed administrator to have your account verified.</p>
      </div>
    </div>
  )
}

export default Signup
