import { useState } from 'react'
import { Link } from 'react-router-dom'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Pet Owner (Sprint V): record a symptom or health event for one
// of their pets, then see it in the pet's history.
// API: GET  /api/owner/pets          (the pet drop-down)
//      GET  /api/owner/symptoms      (the history list)
//      POST /api/owner/symptoms      {pet_id, symptom, severity, observed_at, notes}
// (src/routes/symptoms.py)
// ------------------------------------------------------------

const SEVERITIES = ['mild', 'moderate', 'severe']
const PET_ICONS = { Cat: '🐱', Bird: '🐦', Rabbit: '🐰' }

// "2026-11-20T08:30" for right now, the format a datetime-local input uses
function nowForInput() {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 16)
}

const EMPTY = { pet_id: '', symptom: '', severity: 'mild', observed_at: '', notes: '' }

function SymptomTracker() {
  const { user } = useAuth()
  const [form, setForm] = useState({ ...EMPTY, observed_at: nowForInput() })
  const [message, setMessage] = useState(null)
  const [saving, setSaving] = useState(false)
  const [newId, setNewId] = useState(null)

  const pets = useApiData('/owner/pets')
  const history = useApiData('/owner/symptoms')
  const petList = pets.status === 200 ? pets.data.pets : []
  const h = history.status === 200 ? history.data : null

  function change(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (saving) return
    setMessage(null)
    setSaving(true)
    try {
      const res = await apiPost('/owner/symptoms', form, user.token)
      if (res.ok) {
        setMessage({ ok: true, text: res.data.message })
        setNewId(res.data.symptom.symptom_id)
        setForm({ ...EMPTY, pet_id: form.pet_id, observed_at: nowForInput() })
        history.reload()
      } else {
        setMessage({ ok: false, text: res.data.message || 'Could not save the symptom.' })
      }
    } finally {
      setSaving(false)
    }
  }

  return (
    <UseCaseLayout title="Symptom Tracker" subtitle="Record a symptom or health event so you and your vet can see the pattern."
                   result={history}>
      <div className="uc-split">
        <form className="uc-form uc-panel" onSubmit={handleSubmit} noValidate>
          <h2 className="uc-section-title">Record a symptom</h2>

          <label htmlFor="pet_id">Pet</label>
          <select id="pet_id" name="pet_id" value={form.pet_id} onChange={change}>
            <option value="">Choose a pet…</option>
            {petList.map((p) => (
              <option key={p.pet_id} value={p.pet_id}>{p.name} ({p.species})</option>
            ))}
          </select>
          <p className="uc-muted uc-small">Pet not listed? <Link to="/owner/pets">Add it on My Pets</Link>.</p>

          <label htmlFor="symptom">Symptom or event</label>
          <input id="symptom" name="symptom" maxLength={255} value={form.symptom} onChange={change}
                 placeholder="For example: Sneezing after walks" />

          <fieldset className="uc-severity">
            <legend>How serious?</legend>
            {SEVERITIES.map((s) => (
              <label key={s} className={`uc-sev uc-sev-${s}${form.severity === s ? ' selected' : ''}`}>
                <input type="radio" name="severity" value={s} checked={form.severity === s} onChange={change} />
                {s}
              </label>
            ))}
          </fieldset>

          <label htmlFor="observed_at">When did you notice it?</label>
          <input id="observed_at" name="observed_at" type="datetime-local" max={nowForInput()}
                 value={form.observed_at} onChange={change} />

          <label htmlFor="notes">Notes (optional)</label>
          <textarea id="notes" name="notes" rows="3" value={form.notes} onChange={change} />

          {message && (
            <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
          )}

          <button type="submit" className="primary-button uc-button" disabled={saving}>
            {saving ? 'Saving...' : 'Save symptom'}
          </button>
        </form>

        <section>
          <h2 className="uc-section-title">Symptom history {h && `(${h.count})`}</h2>
          <div className="uc-list">
            {h && h.symptoms.map((s) => (
              <article key={s.symptom_id} className={`uc-card${s.symptom_id === newId ? ' uc-new' : ''}`}>
                <header className="uc-card-head">
                  <span className="uc-avatar" aria-hidden="true">{PET_ICONS[s.pet_species] || '🐶'}</span>
                  <div>
                    <strong>{s.symptom}</strong>
                    <div className="uc-muted uc-small">{s.pet_name} · {formatDate(s.observed_at)}</div>
                  </div>
                  <span className={`uc-pill uc-pill-${s.severity}`}>{s.severity}</span>
                </header>
                {s.notes && <p className="uc-body">{s.notes}</p>}
              </article>
            ))}
            {h && h.count === 0 && <p className="uc-empty">No symptoms recorded yet.</p>}
          </div>
        </section>
      </div>
    </UseCaseLayout>
  )
}

export default SymptomTracker
