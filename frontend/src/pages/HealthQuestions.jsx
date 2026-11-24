import { useState } from 'react'
import { apiPost, formatDate } from '../api/petmedApi.js'
import { useAuth } from '../auth/AuthContext.jsx'
import useApiData from '../api/useApiData.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Veterinarian use cases
// Sprint IV: view pet-health questions from pet owners.
//   GET  /api/vet/questions?show=&q=
// Sprint V: answer a question with general veterinary guidance.
//   POST /api/vet/questions/<question_id>/answer {response_text}
// (src/routes/vet.py)
// ------------------------------------------------------------

const FILTERS = [
  ['all', 'All questions'],
  ['mine', 'Sent to me'],
  ['open', 'Open to any vet'],
  ['unanswered', 'Unanswered'],
]
const SOURCE_LABELS = { veterinarian: 'Veterinarian', pet_health_expert: 'Pet Health Expert', community: 'Community' }
const PET_ICONS = { Cat: '🐱', Bird: '🐦' }

function HealthQuestions() {
  const { user } = useAuth()
  const [drafts, setDrafts] = useState({})
  const [message, setMessage] = useState(null)
  const [busy, setBusy] = useState(null)
  const [show, setShow] = useState('all')
  const [text, setText] = useState('')
  const [search, setSearch] = useState('')

  const result = useApiData(`/vet/questions?${new URLSearchParams({ show, q: search })}`)
  const d = result.status === 200 ? result.data : null
  
  async function postAnswer(e, question) {
    e.preventDefault()
    setBusy(question.question_id)
    setMessage(null)

    try {
      const res = await apiPost(
        `/vet/questions/${question.question_id}/answer`,
        { response_text: drafts[question.question_id] || '' },
        user.token
      )

      setMessage({
        ok: res.ok,
        id: question.question_id,
        text: res.data.message || 'Could not post your guidance.'
      })

      if (res.ok) {
        setDrafts(prev => ({
          ...prev,
          [question.question_id]: ''
        }))
        result.reload()
      }
    } catch {
      setMessage({
        ok: false,
        id: question.question_id,
        text: 'Could not post your guidance.'
      })
    } finally {
      setBusy(null)
    }
  }


  return (
    <UseCaseLayout title="Pet Health Questions" subtitle="Questions submitted by pet owners, newest first." result={result}>
      <div className="uc-chips" role="group" aria-label="Which questions">
        {FILTERS.map(([value, label]) => (
          <button type="button" key={value} className={show === value ? 'uc-chip active' : 'uc-chip'} onClick={() => setShow(value)}>{label}</button>
        ))}
      </div>
      <form className="uc-toolbar" onSubmit={(e) => { e.preventDefault(); setSearch(text.trim()) }}>
        <input type="search" placeholder="Search questions, pets or owners" value={text}
               onChange={(e) => setText(e.target.value)} aria-label="Search questions" />
        <button className="primary-button uc-button" type="submit">Search</button>
      </form>

      {d && (
        <>
          <p className="uc-count">
            {d.count} {d.count === 1 ? 'question' : 'questions'} ·{' '}
            {d.questions.filter((item) => item.answer_list.length === 0).length} unanswered
          </p>
          <div className="uc-list">

            {d.questions.map((item) => (
              <article key={item.question_id} className="uc-card">
                <header className="uc-card-head">
                  <span className="uc-avatar" aria-hidden="true">{PET_ICONS[item.pet_species] || '🐶'}</span>
                  <div>
                    <strong>{item.pet_name ? `${item.pet_name}, ${item.pet_breed}` : 'General question'}</strong>
                    <div className="uc-muted uc-small">Asked by {item.asked_by} · {formatDate(item.created_at)}</div>
                  </div>
                  {item.sent_to_me ? <span className="uc-pill uc-pill-mine">Sent to you</span>
                    : item.sent_to ? <span className="uc-pill">To {item.sent_to}</span>
                    : <span className="uc-pill uc-pill-open">Open to any vet</span>}
                </header>
                <p className="uc-body uc-quote">“{item.question_text}”</p>
                {item.answer_list.length === 0 ? (
                  <p className="uc-unanswered">No answers yet</p>
                ) : (
                  <ul className="uc-comments">
                    {item.answer_list.map((a, i) => (
                      <li key={i}>
                        <strong>{a.author}</strong>{' '}
                        <span className="uc-muted uc-small">({SOURCE_LABELS[a.source_type] || a.source_type})</span>{' '}
                        {a.response_text}
                      </li>
                    ))}
                  </ul>
                )}

                
{(item.sent_to_me || !item.sent_to) &&
  !item.answer_list.some(a => a.author === user.name) && (
    <form
      className="uc-reply"
      onSubmit={e => postAnswer(e, item)}
    >
      <label htmlFor={`guidance-${item.question_id}`}>
        Your guidance
      </label>

      <textarea
        id={`guidance-${item.question_id}`}
        rows="3"
        value={drafts[item.question_id] || ''}
        onChange={e => setDrafts(prev => ({
          ...prev,
          [item.question_id]: e.target.value
        }))}
      />

      <button
        type="submit"
        className="primary-button uc-button"
        disabled={busy !== null}
      >
        {busy === item.question_id
          ? 'Posting...'
          : 'Post guidance'}
      </button>
    </form>
)}

{message && message.id === item.question_id && (
  <p className={message.ok ? 'uc-success' : 'login-error'}>
    {message.text}
  </p>
)}

              </article>
            ))}
            {d.count === 0 && <p className="uc-empty">No questions here.</p>}
          </div>
        </>
      )}
    </UseCaseLayout>
  )
}

export default HealthQuestions
