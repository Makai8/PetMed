import { useState } from 'react'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import ReportButton from '../components/ReportButton.jsx'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Pet Owner: ask for health advice, and read the answers.
// The questions asked here are what veterinarians and pet health
// experts answer (their Sprint V use cases).
// API: GET  /api/owner/professionals
//      GET  /api/owner/questions
//      POST /api/owner/questions {question_text, pet_id?, directed_to_user_id?}
// (src/routes/advice.py)
// ------------------------------------------------------------

const SOURCE_LABELS = { veterinarian: 'Veterinarian', pet_health_expert: 'Pet Health Expert', community: 'Community' }
const EMPTY = { pet_id: '', directed_to_user_id: '', question_text: '' }

function AskAdvice() {
  const { user } = useAuth()
  const [form, setForm] = useState(EMPTY)
  const [message, setMessage] = useState(null)
  const [saving, setSaving] = useState(false)
  const [newId, setNewId] = useState(null)

  const pets = useApiData('/owner/pets')
  const pros = useApiData('/owner/professionals')
  const result = useApiData('/owner/questions')
  const petList = pets.status === 200 ? pets.data.pets : []
  const proList = pros.status === 200 ? pros.data.professionals : []
  const d = result.status === 200 ? result.data : null

  function change(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setMessage(null)
    setSaving(true)
    const res = await apiPost('/owner/questions', form, user.token)
    setSaving(false)
    if (res.ok) {
      setMessage({ ok: true, text: res.data.message })
      setNewId(res.data.question_id)
      setForm(EMPTY)
      result.reload()
    } else {
      setMessage({ ok: false, text: res.data.message || 'Could not send your question.' })
    }
  }

  return (
    <UseCaseLayout title="Ask for Health Advice"
                   subtitle="Ask a veterinarian or a pet health expert. Answers show up here." result={result}>
      <div className="uc-split">
        <form className="uc-form uc-panel" onSubmit={handleSubmit} noValidate>
          <h2 className="uc-section-title">Ask a question</h2>

          <label htmlFor="pet_id">About which pet? (optional)</label>
          <select id="pet_id" name="pet_id" value={form.pet_id} onChange={change}>
            <option value="">No specific pet</option>
            {petList.map((p) => <option key={p.pet_id} value={p.pet_id}>{p.name} ({p.species})</option>)}
          </select>

          <label htmlFor="directed_to_user_id">Send to</label>
          <select id="directed_to_user_id" name="directed_to_user_id" value={form.directed_to_user_id} onChange={change}>
            <option value="">Any veterinarian</option>
            {proList.map((p) => (
              <option key={p.user_id} value={p.user_id}>
                {p.full_name} ({SOURCE_LABELS[p.professional_type]}, {p.specialty})
              </option>
            ))}
          </select>

          <label htmlFor="question_text">Your question</label>
          <textarea id="question_text" name="question_text" rows="4" value={form.question_text} onChange={change}
                    placeholder="Describe what you've noticed, how long it's been happening, and anything that changed." />

          {message && (
            <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
          )}
          <button type="submit" className="primary-button uc-button" disabled={saving}>
            {saving ? 'Sending…' : 'Send question'}
          </button>
        </form>

        <section>
          <h2 className="uc-section-title">My questions {d && `(${d.count})`}</h2>
          <div className="uc-list">
            {d && d.questions.map((q) => (
              <article key={q.question_id} className={`uc-card${q.question_id === newId ? ' uc-new' : ''}`}>
                <p className="uc-body"><strong>{q.question_text}</strong></p>
                <p className="uc-muted uc-small">
                  Asked {formatDate(q.created_at)}{q.pet_name && <> · about {q.pet_name}</>} · sent to {q.sent_to || 'any veterinarian'}
                </p>
                {q.answer_list.length > 0 ? (
                  <ul className="uc-answers">
                    {q.answer_list.map((a) => (
                      <li key={a.response_id}>
                        <span className={`uc-pill uc-pill-${a.source_type}`}>{SOURCE_LABELS[a.source_type] || a.source_type}</span>{' '}
                        <strong>{a.author}</strong>: {a.response_text}
                        <ReportButton responseId={a.response_id} />
                      </li>
                    ))}
                  </ul>
                ) : <span className="uc-unanswered">Waiting for an answer</span>}
              </article>
            ))}
            {d && d.count === 0 && <p className="uc-empty">You haven't asked anything yet.</p>}
          </div>
        </section>
      </div>
    </UseCaseLayout>
  )
}

export default AskAdvice
