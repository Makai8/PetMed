import { useState } from 'react'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Administrator: review role requests and approve or reject them.
// Approving gives the user the role; for vets and experts it also
// approves their Professional_Profile and logs a Verification_Review.
// API: GET /api/admin/role-requests, POST .../<id>/approve | reject
// ------------------------------------------------------------

const FILTERS = [
  ['pending', 'Pending'],
  ['approved', 'Approved'],
  ['rejected', 'Rejected'],
  ['all', 'All'],
]

function RoleRequests() {
  const { user } = useAuth()
  const [status, setStatus] = useState('pending')
  const [notes, setNotes] = useState({})
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(null)

  const result = useApiData(`/admin/role-requests?${new URLSearchParams({ status })}`)
  const d = result.status === 200 ? result.data : null

  async function decide(id, decision) {
    setError('')
    setBusy(id)
    const res = await apiPost(`/admin/role-requests/${id}/${decision}`, { notes: notes[id] || '' }, user.token)
    setBusy(null)
    if (!res.ok) setError(res.data.message || 'Could not save the decision.')
    result.reload()
  }

  return (
    <UseCaseLayout title="Role Requests" subtitle="Approve or reject requests to become a vet, expert, moderator or administrator." result={result}>
      <div className="uc-chips" role="group" aria-label="Request status">
        {FILTERS.map(([value, label]) => (
          <button type="button" key={value} className={status === value ? 'uc-chip active' : 'uc-chip'} onClick={() => setStatus(value)}>{label}</button>
        ))}
      </div>
      {error && <p className="login-error" role="alert">{error}</p>}

      {d && (
        <>
          <p className="uc-count">{d.count} {d.count === 1 ? 'request' : 'requests'}</p>
          <div className="uc-list">
            {d.requests.map((r) => (
              <article key={r.request_id} className="uc-card">
                <header className="uc-card-head">
                  <span className="uc-avatar" aria-hidden="true">{r.full_name[0]}</span>
                  <div>
                    <strong>{r.full_name}</strong>
                    <div className="uc-muted uc-small">{r.email} · requested {formatDate(r.requested_at)}</div>
                  </div>
                  <span className="uc-pill uc-pill-mine">{roles[r.role]?.label || r.role}</span>
                  <span className={`uc-pill uc-pill-${r.status}`}>{r.status}</span>
                </header>

                <p className="uc-body">“{r.reason}”</p>

                {r.credentials && (
                  <dl className="uc-details">
                    <dt>Credentials</dt><dd>{r.credentials}</dd>
                    <dt>Specialty</dt><dd>{r.specialty}</dd>
                    <dt>Organization</dt><dd>{r.organization}</dd>
                    {r.experience && <><dt>Experience</dt><dd>{r.experience}</dd></>}
                  </dl>
                )}

                {r.status === 'pending' ? (
                  <div className="uc-decision">
                    <input type="text" placeholder="Note to the user (optional)" aria-label={`Note for ${r.full_name}`}
                           value={notes[r.request_id] || ''}
                           onChange={(e) => setNotes({ ...notes, [r.request_id]: e.target.value })} />
                    <button type="button" className="primary-button uc-button" disabled={busy === r.request_id}
                            onClick={() => decide(r.request_id, 'approve')}>Approve</button>
                    <button type="button" className="uc-reject" disabled={busy === r.request_id}
                            onClick={() => decide(r.request_id, 'reject')}>Reject</button>
                  </div>
                ) : (
                  <p className="uc-muted uc-small">
                    {r.status === 'approved' ? 'Approved' : 'Rejected'} by {r.reviewed_by} on {formatDate(r.reviewed_at)}
                    {r.review_notes && <> · “{r.review_notes}”</>}
                  </p>
                )}
              </article>
            ))}
            {d.count === 0 && <p className="uc-empty">No requests here.</p>}
          </div>
        </>
      )}
    </UseCaseLayout>
  )
}

export default RoleRequests
