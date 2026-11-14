import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import logo from '../assets/petmed-logo.png'
import '../Portal.css'

// ------------------------------------------------------------
// Sign in page for all five roles.
// On success the user goes to the landing page for their role.
// ------------------------------------------------------------

function Login() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  // Already signed in, skip the form
  if (user) {
    return <Navigate to={roles[user.role].home} replace />
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')

    if (!email || !password) {
      setError('Enter your email and password.')
      return
    }

    setLoading(true)
    try {
      const signedIn = await login(email, password)
      navigate(roles[signedIn.role].home)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-shell">
      <div className="login-card">
        <Link to="/" className="login-logo">
          <img src={logo} alt="PetMed logo" />
        </Link>
        <h1 className="login-title">Welcome back</h1>
        <p className="login-subtitle">Sign in to your PetMed account</p>

        <form onSubmit={handleSubmit} noValidate>
          <label htmlFor="email">Email</label>
          <input
            id="email"
            type="email"
            placeholder="you@petmed.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            autoComplete="username"
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="Your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete="current-password"
          />

          {error && <p className="login-error" role="alert">{error}</p>}

          <button type="submit" className="primary-button login-button" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <Link to="/" className="login-back">Back to home</Link>
      </div>
    </div>
  )
}

export default Login
