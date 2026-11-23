import { useState } from 'react'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Pet Health Expert use cases
// Sprint IV: browse questions and posts in the expert's approved
//   area of expertise.  GET /api/expert/topics?q=
// Sprint V: answer a question inside that area.
//   POST /api/expert/questions/<question_id>/answer {response_text}
// (src/routes/expert.py)
// ------------------------------------------------------------

function ExpertQuestions() {
  const { user } = useAuth()
  const [drafts, setDrafts] = useState({})
  const [message, setMessage] = useState(null)
  const [busy, setBusy] = useState(null)
  const [text, setText] = useState('')
  const [search, setSearch] = useState('')

  const result = useApiData(`/expert/topics?${new URLSearchParams({ q: search })}`)
  const d = result.status === 200 ? result.data : null

  async function postAnswer(e, question) {
    e.preventDefault()
    if (busy !== null) return
    const id = question.question_id
    setMessage(null)
    setBusy(id)
    try {
      const res = await apiPost(`/expert/questions/${id}/answer`,
        { response_text: drafts[id] || '' }, user.token)
      setMessage({ id, ok: res.ok, text: res.data.message || 'Could not post your answer.' })
      if (res.ok) {
        setDrafts((previous) => ({ ...previous, [id]: '' }))
        result.reload()
      }
    } finally {
      setBusy(null)
    }
  }

  return (
    <UseCaseLayout title="Questions in My Expertise" subtitle="Questions and posts in your approved area of expertise." result={result}>
      {d && (
        <p className="uc-specialty">
          Approved specialty: <span className="uc-pill uc-pill-mine">{d.specialty}</span>
          {d.organization && <span className="uc-muted"> · {d.organization}</span>}
        </p>
      )}
      <form className="uc-toolbar" onSubmit={(e) => { e.preventDefault(); setSearch(text.trim()) }}>
        <input type="search" placeholder="Search within your specialty" value={text}
               onChange={(e) => setText(e.target.value)} aria-label="Search your specialty" />
        <button className="primary-button uc-button" type="submit">Search</button>
      </form>

      {d && (
        <div className="uc-two-col">
          <section>
            <h2 className="uc-section-title">Questions sent to you ({d.questions.length})</h2>
            <div className="uc-list">
              {d.questions.map((item) => (
                <article key={item.question_id} className="uc-card">
                  <p className="uc-body uc-quote">“{item.question_text}”</p>
                  <p className="uc-muted uc-small">
                    {item.asked_by}{item.pet_name && <> · {item.pet_name} ({item.pet_species})</>} · {formatDate(item.created_at)}
                  </p>
                  {item.answers > 0
                    ? <span className="uc-pill uc-pill-answered">{item.answers} {item.answers === 1 ? 'answer' : 'answers'}</span>
                    : <span className="uc-unanswered">No answers yet</span>}

                  {item.answers === 0 && (
                    <form className="uc-reply" onSubmit={(e) => postAnswer(e, item)} noValidate>
                      <label htmlFor={`expert-answer-${item.question_id}`}>Your answer ({d.specialty})</label>
                      <textarea id={`expert-answer-${item.question_id}`} rows="3" maxLength={2000}
                        value={drafts[item.question_id] || ''}
                        onChange={(e) => setDrafts((previous) => ({ ...previous, [item.question_id]: e.target.value }))}
                        disabled={busy === item.question_id} />
                      <button type="submit" className="primary-button uc-button" disabled={busy !== null}>
                        {busy === item.question_id ? 'Posting...' : 'Post answer'}
                      </button>
                    </form>
                  )}
                  {message && message.id === item.question_id && (
                    <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>
                      {message.text}
                    </p>
                  )}
                </article>
              ))}
              {d.questions.length === 0 && <p className="uc-empty">No questions match.</p>}
            </div>
          </section>
          <section>
            <h2 className="uc-section-title">Posts tagged #{d.tag} ({d.posts.length})</h2>
            <div className="uc-list">
              {d.posts.map((p) => (
                <article key={p.post_id} className="uc-card">
                  <p className="uc-body">{p.body}</p>
                  <p className="uc-muted uc-small">
                    {p.author}{p.pet_name && <> · about {p.pet_name}</>} · {formatDate(p.created_at)}
                  </p>
                </article>
              ))}
              {d.posts.length === 0 && <p className="uc-empty">No posts match.</p>}
            </div>
          </section>
        </div>
      )}
    </UseCaseLayout>
  )
}

export default ExpertQuestions
