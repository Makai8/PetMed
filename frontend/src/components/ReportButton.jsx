import { useState } from 'react'
import { apiPost } from '../api/petmedApi.js'
import { useAuth } from '../auth/AuthContext.jsx'

// ------------------------------------------------------------
// "Report" link that opens a one-line reason form.
// Files a Report the Community Moderator then reviews.
// Use it with exactly one of: postId (a feed post) or responseId (an answer).
// API: POST /api/reports {post_id | response_id, reason} (src/routes/reports.py)
// ------------------------------------------------------------

function ReportButton({ postId, responseId }) {
  const { user } = useAuth()
  const [open, setOpen] = useState(false)
  const [reason, setReason] = useState('')
  const [message, setMessage] = useState(null)
  const [saving, setSaving] = useState(false)

  async function submit(e) {
    e.preventDefault()
    setSaving(true)
    const body = postId ? { post_id: postId, reason } : { response_id: responseId, reason }
    const res = await apiPost('/reports', body, user.token)
    setSaving(false)
    setMessage({ ok: res.ok, text: res.data.message || 'Could not send the report.' })
    if (res.ok) {
      setOpen(false)
      setReason('')
    }
  }

  return (
    <div className="uc-report">
      {!open && (
        <button type="button" className="uc-report-link" onClick={() => { setOpen(true); setMessage(null) }}>
          🚩 Report
        </button>
      )}
      {open && (
        <form className="uc-report-form" onSubmit={submit}>
          <input aria-label="Why are you reporting this?" placeholder="What is wrong with it?" value={reason}
                 onChange={(e) => setReason(e.target.value)} maxLength={1000} />
          <button type="submit" className="primary-button uc-button" disabled={saving}>Send report</button>
          <button type="button" className="uc-chip" onClick={() => setOpen(false)}>Cancel</button>
        </form>
      )}
      {message && (
        <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
      )}
    </div>
  )
}

export default ReportButton
