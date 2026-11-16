import { useState } from 'react'
import { Link, Navigate, useLocation } from 'react-router-dom'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Optional step after sign up (and a Pet Owner menu item):
// ask to become a Veterinarian, Pet Health Expert, Community
// Moderator or Administrator. An administrator must approve it.
// API: POST /api/role-requests, GET /api/role-requests/mine
//      (src/routes/role_requests.py)
// ------------------------------------------------------------

const OPTIONS = [
  { role: 'veterinarian', icon: '🩺', text: 'Licensed vets answer health questions and review shared records.' },
  { role: 'pet_health_expert', icon: '🎓', text: 'Specialists (nutrition, training, behavior) answer within their area.' },
  { role: 'community_moderator', icon: '🛡️', text: 'Volunteers who review reports and keep the community safe.' },
  { role: 'administrator', icon: '⚙️', text: 'Staff who manage users, professionals and settings.' },
]
const PROFESSIONAL = ['veterinarian', 'pet_health_expert']

function RequestRoleForm() {
  const { user } = useAuth()
  const isNew = new URLSearchParams(useLocation().search).get('new') === '1'
  const result = useApiData('/role-requests/mine')
  const d = result.status === 200 ? result.data : null

  const [role, setRole] = useState('')
  const [reason, setReason] = useState('')
  const [credentials, setCredentials] = useState('')
  const [specialty, setSpecialty] = useState('')
  const [organization, setOrganization] = useState('')
  const [experience, setExperience] = useState('')
  const [message, setMessage] = useState(null)
  const [sending, setSending] = useState(false)
  const professional = PROFESSIONAL.includes(role)

  async function handleSubmit(event) {
    event.preventDefault()
    setMessage(null)
    if (!role) {
      setMessage({ ok: false, text: 'Choose the role you want to request.' })
      return
    }
    setSending(true)
    const res = await apiPost('/role-requests', { role, reason, credentials, specialty, organization, experience }, user.token)
    setSending(false)
    if (!res.ok) {
      setMessage({ ok: false, text: res.data.message || 'Could not send the request.' })
      return
    }
    setMessage({ ok: true, text: res.data.message })
    setRole('')
    setReason('')
    setCredentials('')
    setSpecialty('')
    setOrganization('')
    setExperience('')
    result.reload()
  }

  return (
    <UseCaseLayout
      title="Request a Professional Role"
      subtitle="Optional: ask to join PetMed as a professional or staff member. An administrator reviews every request."
      result={result}
    >
      {isNew && (
        <div className="uc-welcome">
          <strong>Your account is ready! 🎉</strong>
          <p>You're signed in as a Pet Owner. If you're also a vet, an expert, or want to help run PetMed, request a role below. Otherwise, skip this step.</p>
          <Link to={roles[user.role].home} className="secondary-button uc-skip">Skip for now</Link>
        </div>
      )}

      {d && (
        <>
          <form className="uc-form" onSubmit={handleSubmit} noValidate>
            <fieldset className="uc-role-options">
              <legend>Which role?</legend>
              {OPTIONS.map((o) => {
                const held = d.roles.includes(o.role)
                return (
                  <label key={o.role} className={`uc-role-option${role === o.role ? ' selected' : ''}${held ? ' held' : ''}`}>
                    <input type="radio" name="role" value={o.role} checked={role === o.role}
                           disabled={held} onChange={() => setRole(o.role)} />
                    <span className="uc-role-icon" aria-hidden="true">{o.icon}</span>
                    <strong>{roles[o.role].label}</strong>
                    <small>{held ? 'You already have this role.' : o.text}</small>
                  </label>
                )
              })}
            </fieldset>

            <label htmlFor="reason">Why are you requesting this role?</label>
            <textarea id="reason" rows="3" value={reason} onChange={(e) => setReason(e.target.value)}
                      placeholder="A few sentences about yourself" />

            {professional && (
              <>
                <label htmlFor="credentials">License number or credentials</label>
                <input id="credentials" value={credentials} onChange={(e) => setCredentials(e.target.value)}
                       placeholder={role === 'veterinarian' ? 'DVM, state license number' : 'Certifications or degree'} />

                <label htmlFor="specialty">{role === 'veterinarian' ? 'Specialty (optional)' : 'Area of expertise'}</label>
                <input id="specialty" value={specialty} onChange={(e) => setSpecialty(e.target.value)}
                       placeholder={role === 'veterinarian' ? 'General Practice' : 'Nutrition, Training, Behavior…'} />

                <label htmlFor="organization">Where you work</label>
                <input id="organization" value={organization} onChange={(e) => setOrganization(e.target.value)}
                       placeholder="Clinic or organization" />

                <label htmlFor="experience">Experience (optional)</label>
                <input id="experience" value={experience} onChange={(e) => setExperience(e.target.value)}
                       placeholder="For example: 6 years in small animal practice" />
              </>
            )}

            {message && (
              <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
            )}

            <button type="submit" className="primary-button uc-button" disabled={sending}>
              {sending ? 'Sending…' : 'Send request'}
            </button>
          </form>

          <h2 className="uc-section-title uc-gap">My requests</h2>
          {d.requests.length === 0 ? (
            <p className="uc-muted">You haven't requested a role yet.</p>
          ) : (
            <div className="uc-list">
              {d.requests.map((r) => (
                <article key={r.request_id} className="uc-card">
                  <header className="uc-card-head">
                    <strong>{roles[r.role]?.label || r.role}</strong>
                    <span className="uc-muted uc-small">Requested {formatDate(r.requested_at)}</span>
                    <span className={`uc-pill uc-pill-${r.status}`}>{r.status}</span>
                  </header>
                  <p className="uc-body">{r.reason}</p>
                  {r.status === 'approved' && <p className="uc-success">Approved! Log out and sign in again to use your new role.</p>}
                  {r.review_notes && <p className="uc-muted uc-small">Administrator's note: {r.review_notes}</p>}
                </article>
              ))}
            </div>
          )}
        </>
      )}
    </UseCaseLayout>
  )
}

function RequestRole() {
  const { user } = useAuth()
  if (!user) return <Navigate to="/login" replace />
  return <RequestRoleForm />
}

export default RequestRole
