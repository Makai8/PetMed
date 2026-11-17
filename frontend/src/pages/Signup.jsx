import { useState } from 'react'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { apiPost } from '../api/petmedApi.js'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import logo from '../assets/petmed-logo.png'
import '../Portal.css'
import '../UseCases.css'

// ------------------------------------------------------------
// Sign up page: creates a Pet Owner account in the database
// (POST /api/signup, src/routes/signup.py), then signs the new
// user in. "I'm signing up as" lets them ask for another role;
// they stay a Pet Owner until an administrator approves it.
// ------------------------------------------------------------

function Signup() {
  const { user, login } = useAuth()
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const [userType, setUserType] = useState('pet_owner')
  const [reason, setReason] = useState('')
  const [credentials, setCredentials] = useState('')
  const [specialty, setSpecialty] = useState('')
  const [organization, setOrganization] = useState('')
  const [experience, setExperience] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const professional = userType === 'veterinarian' || userType === 'pet_health_expert'

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
    const res = await apiPost('/signup', {
      full_name: fullName,
      email,
      password,
      requested_role: userType,
      reason,
      credentials,
      specialty,
      organization,
      experience,
    })
    if (!res.ok) {
      setLoading(false)
      setError(res.data.message || 'Could not create the account.')
      return
    }

    // Account created: sign in right away. Anyone who asked for another
    // role sees their pending request; everyone else goes to their dashboard.
    try {
      const signedIn = await login(email, password)
      navigate(res.data.requested_role ? '/request-role?requested=1' : roles[signedIn.role].home)
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
        <p className="login-subtitle">Join the PetMed community</p>

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

          <label htmlFor="userType">I'm signing up as</label>
          <select id="userType" className="signup-select" value={userType} onChange={(e) => setUserType(e.target.value)}>
            <option value="pet_owner">Pet Owner</option>
            <option value="veterinarian">Veterinarian</option>
            <option value="pet_health_expert">Pet Health Expert</option>
            <option value="community_moderator">Community Moderator</option>
            <option value="administrator">Administrator</option>
          </select>

          {userType !== 'pet_owner' && (
            <div className="signup-request">
              <p className="login-hint">
                You'll start as a <strong>Pet Owner</strong>. An administrator reviews your request
                to become a {roles[userType].label}, and you get the new role once it's approved.
              </p>

              <label htmlFor="reason">Why are you requesting this role?</label>
              <textarea id="reason" rows="3" value={reason} onChange={(e) => setReason(e.target.value)}
                        placeholder="A few sentences about yourself" />

              {professional && (
                <>
                  <label htmlFor="credentials">License number or credentials</label>
                  <input id="credentials" value={credentials} onChange={(e) => setCredentials(e.target.value)}
                         placeholder={userType === 'veterinarian' ? 'DVM, state license number' : 'Certifications or degree'} />

                  <label htmlFor="specialty">{userType === 'veterinarian' ? 'Specialty (optional)' : 'Area of expertise'}</label>
                  <input id="specialty" value={specialty} onChange={(e) => setSpecialty(e.target.value)}
                         placeholder={userType === 'veterinarian' ? 'General Practice' : 'Nutrition, Training, Behavior…'} />

                  <label htmlFor="organization">Where you work</label>
                  <input id="organization" value={organization} onChange={(e) => setOrganization(e.target.value)}
                         placeholder="Clinic or organization" />

                  <label htmlFor="experience">Experience (optional)</label>
                  <input id="experience" value={experience} onChange={(e) => setExperience(e.target.value)}
                         placeholder="For example: 6 years in small animal practice" />
                </>
              )}
            </div>
          )}

          {error && <p className="login-error" role="alert">{error}</p>}

          <button type="submit" className="primary-button login-button" disabled={loading}>
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <p className="login-switch">
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </div>
    </div>
  )
}

export default Signup
