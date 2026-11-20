import { useState } from 'react'
import { formatDate } from '../api/petmedApi.js' // DAVID: also import apiPost
import useApiData from '../api/useApiData.js'
// DAVID: import { useAuth } from '../auth/AuthContext.jsx'
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
  // DAVID: add the form state here, for example
  //   const { user } = useAuth()
  //   const [form, setForm] = useState({ ...EMPTY, observed_at: nowForInput() })
  //   const [message, setMessage] = useState(null)
  //   const [saving, setSaving] = useState(false)
  const [newId] = useState(null) // DAVID: becomes [newId, setNewId]; highlights the row just saved

  const pets = useApiData('/owner/pets')
  const history = useApiData('/owner/symptoms')
  const petList = pets.status === 200 ? pets.data.pets : []
  const h = history.status === 200 ? history.data : null

  // DAVID: write change(e) and handleSubmit(e) here.

  return (
    <UseCaseLayout title="Symptom Tracker" subtitle="Record a symptom or health event so you and your vet can see the pattern."
                   result={history}>
      <div className="uc-split">
        {/* ================= DAVID: build the form here (Sprint V) =================
            Worked example: pages/Verification.jsx (form state -> apiPost -> message -> reload).
            Use <form className="uc-form uc-panel" onSubmit={handleSubmit} noValidate> with:
              - "Pet": <select id="pet_id" name="pet_id"> with an empty "Choose a pet…" option,
                then one <option> per pet in petList (value = pet_id, text = "Bella (Dog)")
              - "Symptom or event": <input id="symptom" name="symptom" maxLength={255}>
              - "How serious?": a <fieldset className="uc-severity"> with one
                <label className={`uc-sev uc-sev-${s}${form.severity === s ? ' selected' : ''}`}>
                containing a radio input, for each value in SEVERITIES
              - "When did you notice it?": <input id="observed_at" name="observed_at" type="datetime-local" max={nowForInput()}>
              - "Notes (optional)": <textarea id="notes" name="notes" rows="3">
              - the message (uc-success / login-error) and a "Save symptom" button
            Every input uses value={form.x} onChange={change}.
            handleSubmit: preventDefault, apiPost('/owner/symptoms', form, user.token);
              ok  -> show res.data.message, setNewId(res.data.symptom.symptom_id),
                     clear the form (keep the pet), history.reload()
              not ok -> show res.data.message as an error
            Test it: sign in as maya.johnson@petmed.com, save one good symptom and
            one with no pet chosen (the invalid case for the video). */}
        <div className="uc-panel">
          <h2 className="uc-section-title">Record a symptom</h2>
          <p className="uc-muted">Coming in Sprint V.</p>
        </div>

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
