import { useState } from 'react'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Administrator (Sprint V): review a Veterinarian or Pet Health
// Expert account and update its professional verification status.
// API: GET  /api/admin/professionals?status=
//      POST /api/admin/professionals/<profile_id>/status {status, notes}
// (src/routes/verification.py)
//
// This page is also the worked example for the team: the other
// Sprint V pages follow the same pattern (form state -> apiPost ->
// show the server's message -> reload the list).
// ------------------------------------------------------------

const FILTERS = [
  ['pending', 'Waiting for review'],
  ['approved', 'Approved'],
  ['rejected', 'Rejected'],
  ['suspended', 'Suspended'],
  ['all', 'All'],
]

// What the admin can change each status to
const NEXT = {
  pending: [['approved', 'Approve'], ['rejected', 'Reject']],
  approved: [['suspended', 'Suspend']],
  rejected: [['approved', 'Approve']],
  suspended: [['approved', 'Reinstate']],
}

function Verification() {
  const { user } = useAuth()
  const [status, setStatus] = useState('pending')
  const [notes, setNotes] = useState({})
  const [message, setMessage] = useState(null)
  const [busy, setBusy] = useState(null)

  const result = useApiData(`/admin/professionals?${new URLSearchParams({ status })}`)
  const d = result.status === 200 ? result.data : null

  async function update(profile, newStatus) {
    setBusy(profile.profile_id)
    setMessage(null)
    const res = await apiPost(`/admin/professionals/${profile.profile_id}/status`,
      { status: newStatus, notes: notes[profile.profile_id] || '' }, user.token)
    setBusy(null)
    if (res.ok) {
      setMessage({ ok: true, id: profile.profile_id, text: `${profile.full_name}: ${res.data.message}` })
      setNotes({ ...notes, [profile.profile_id]: '' })
      result.reload()
    } else {
      setMessage({ ok: false, id: profile.profile_id, text: res.data.message || 'Could not save the change.' })
    }
  }

  return (
    <UseCaseLayout title="Professional Verification"
                   subtitle="Check each veterinarian's and expert's credentials, then approve, reject or suspend them."
                   result={result}>
      <div className="uc-chips" role="group" aria-label="Verification status">
        {FILTERS.map(([value, label]) => (
          <button type="button" key={value} className={status === value ? 'uc-chip active' : 'uc-chip'}
                  onClick={() => { setStatus(value); setMessage(null) }}>
            {label}{d && d.counts[value] !== undefined ? ` (${d.counts[value]})` : ''}
          </button>
        ))}
      </div>

      {message && !d?.professionals.some((p) => p.profile_id === message.id) && (
        <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
      )}

      {d && (
        <div className="uc-list">
          {d.professionals.map((p) => (
            <article key={p.profile_id} className="uc-card">
              <header className="uc-card-head">
                <span className="uc-avatar" aria-hidden="true">{p.professional_type === 'veterinarian' ? '🩺' : '🎓'}</span>
                <div>
                  <strong>{p.full_name}</strong>
                  <div className="uc-muted uc-small">{p.email} · joined {formatDate(p.created_at)}</div>
                </div>
                <span className="uc-pill uc-pill-mine">{roles[p.professional_type]?.label}</span>
                <span className={`uc-pill uc-pill-${p.verification_status}`}>{p.verification_status}</span>
              </header>

              <dl className="uc-details">
                <dt>Credentials</dt><dd>{p.credentials}</dd>
                <dt>Specialty</dt><dd>{p.specialty}</dd>
                <dt>Organization</dt><dd>{p.organization}</dd>
                {p.experience && <><dt>Experience</dt><dd>{p.experience}</dd></>}
              </dl>

              {p.history.length > 0 && (
                <ul className="uc-history">
                  {p.history.map((h, i) => (
                    <li key={i}>
                      <span className={`uc-pill uc-pill-${h.decision}`}>{h.decision}</span>{' '}
                      by {h.reviewed_by} on {formatDate(h.reviewed_at)}{h.notes && <> · “{h.notes}”</>}
                    </li>
                  ))}
                </ul>
              )}

              <div className="uc-decision">
                <input type="text" aria-label={`Note about ${p.full_name}`}
                       placeholder={p.verification_status === 'pending' ? 'Note (required to reject)' : 'Reason (required to suspend)'}
                       value={notes[p.profile_id] || ''}
                       onChange={(e) => setNotes({ ...notes, [p.profile_id]: e.target.value })} />
                {NEXT[p.verification_status].map(([value, label]) => (
                  <button key={value} type="button" disabled={busy === p.profile_id}
                          className={value === 'approved' ? 'primary-button uc-button' : 'uc-reject'}
                          onClick={() => update(p, value)}>{label}</button>
                ))}
              </div>
              {message && message.id === p.profile_id && (
                <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
              )}
            </article>
          ))}
          {d.count === 0 && <p className="uc-empty">Nobody here.</p>}
        </div>
      )}
    </UseCaseLayout>
  )
}

export default Verification
