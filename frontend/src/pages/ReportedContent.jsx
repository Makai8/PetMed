import { useState } from 'react'
import { formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Community Moderator use case: view reported posts and reported
// health advice. Data: GET /api/moderation/reports?type=&status=
// (src/routes/moderator.py)
// ------------------------------------------------------------

function ReportedContent() {
  const [type, setType] = useState('all')
  const [status, setStatus] = useState('open')

  const result = useApiData(`/moderation/reports?${new URLSearchParams({ type, status })}`)
  const d = result.status === 200 ? result.data : null

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

                  {r.assigned_to === 'Tasha' && (
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
                </p>
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
