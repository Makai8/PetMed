import { useState } from 'react'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Community Moderator use cases
// Sprint IV: view reported posts and reported health advice.
//   GET /api/moderation/reports?type=&status=
// Sprint V: review a report and update its moderation case.
//   POST /api/moderation/reports/<report_id>/decision {action, reason}
// (src/routes/moderator.py)
// ------------------------------------------------------------

const ACTIONS = [
  ['remove_content', 'Remove the content'],
  ['warn_user', 'Warn the author'],
  ['dismiss', 'Dismiss (no violation)'],
  ['escalate', 'Escalate to an administrator'],
]
const ACTION_LABELS = Object.fromEntries(ACTIONS)

function ReportedContent() {
  const { user } = useAuth()
  const [type, setType] = useState('all')
  const [status, setStatus] = useState('open')
  const [decisions, setDecisions] = useState({})
  const [message, setMessage] = useState(null)
  const [busy, setBusy] = useState(null)

  const result = useApiData(`/moderation/reports?${new URLSearchParams({ type, status })}`)
  const d = result.status === 200 ? result.data : null

  function decisionFor(id) {
    return decisions[id] || { action: 'remove_content', reason: '' }
  }

  function changeDecision(id, field, value) {
    setDecisions((previous) => ({ ...previous, [id]: { ...decisionFor(id), [field]: value } }))
  }

  async function saveDecision(e, report) {
    e.preventDefault()
    if (busy !== null) return
    const id = report.report_id
    setMessage(null)
    setBusy(id)
    try {
      const res = await apiPost(`/moderation/reports/${id}/decision`, decisionFor(id), user.token)
      if (res.ok) {
        setMessage({ ok: true, id, text: `Report #${id}: ${res.data.message}` })
        setDecisions((previous) => ({ ...previous, [id]: { action: 'remove_content', reason: '' } }))
        result.reload()
      } else {
        setMessage({ ok: false, id, text: res.data.message || 'Could not save the decision.' })
      }
    } finally {
      setBusy(null)
    }
  }

  return (
    <UseCaseLayout title="Reported Posts and Advice" subtitle="Content PetMed users have flagged for review." result={result}>
      <div className="uc-toolbar">
        <select value={type} onChange={(e) => setType(e.target.value)} aria-label="Content type">
          <option value="all">Posts and advice</option>
          <option value="post">Reported posts</option>
          <option value="advice">Reported health advice</option>
        </select>
        <select value={status} onChange={(e) => setStatus(e.target.value)} aria-label="Report status">
          <option value="open">Open</option>
          <option value="resolved">Resolved</option>
          <option value="all">All</option>
        </select>
      </div>

      {message && message.ok && (
        <p className="uc-success" role="status">{message.text}</p>
      )}

      {d && (
        <>
          <p className="uc-count">{d.count} {d.count === 1 ? 'report' : 'reports'}</p>
          <div className="uc-list">
            {d.reports.map((r) => (
              <article key={r.report_id} className="uc-card">
                <header className="uc-card-head">
                  <span className={`uc-pill uc-pill-${r.content_type}`}>
                    {r.content_type === 'post' ? 'Reported post' : 'Reported health advice'}
                  </span>
                  <span className="uc-muted uc-small">Report #{r.report_id} · {formatDate(r.created_at)}</span>
                  <span className={`uc-pill uc-pill-${r.status}`}>{r.status}</span>

                  {r.assigned_to === user.name && (
                    <span className="uc-pill uc-pill-open">
                      Assigned to you
                    </span>
                  )}
                </header>

                <blockquote className="uc-reported">
                  {r.content_type === 'post' ? (
                    <>
                      <p>{r.post_body}</p>
                      <cite>Post by {r.post_author}</cite>
                    </>
                  ) : (
                    <>
                      <p>{r.response_text}</p>
                      <cite>Answer by {r.advice_author} ({r.source_type}) to: “{r.advice_question}”</cite>
                    </>
                  )}
                </blockquote>

                <p><strong>Reason:</strong> {r.reason}</p>
                <p className="uc-muted uc-small">
                  Reported by {r.reported_by}
                  {r.case_status && <> · Case {r.case_status}{r.assigned_to ? `, assigned to ${r.assigned_to}` : ', not assigned yet'}</>}
                  {r.last_action && <> · Last action: {ACTION_LABELS[r.last_action] || r.last_action}</>}
                </p>

                {r.status === 'open' && (
                  <form className="uc-reply" onSubmit={(e) => saveDecision(e, r)} noValidate>
                    <label htmlFor={`action-${r.report_id}`}>Action</label>
                    <select id={`action-${r.report_id}`} value={decisionFor(r.report_id).action}
                            onChange={(e) => changeDecision(r.report_id, 'action', e.target.value)}
                            disabled={busy === r.report_id}>
                      {ACTIONS.map(([value, label]) => (
                        <option key={value} value={value}>{label}</option>
                      ))}
                    </select>
                    <label htmlFor={`reason-${r.report_id}`}>Reason</label>
                    <textarea id={`reason-${r.report_id}`} rows="2" value={decisionFor(r.report_id).reason}
                              onChange={(e) => changeDecision(r.report_id, 'reason', e.target.value)}
                              disabled={busy === r.report_id} />
                    <button type="submit" className="primary-button uc-button" disabled={busy !== null}>
                      {busy === r.report_id ? 'Saving...' : 'Save decision'}
                    </button>
                  </form>
                )}
                {message && !message.ok && message.id === r.report_id && (
                  <p className="login-error" role="alert">{message.text}</p>
                )}
              </article>
            ))}
            {d.count === 0 && <p className="uc-empty">No reports here.</p>}
          </div>
        </>
      )}
    </UseCaseLayout>
  )
}

export default ReportedContent
