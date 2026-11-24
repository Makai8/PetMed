import { useState } from 'react'
import { Link } from 'react-router-dom'
import { apiPost } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Pet Owner: create a pet profile.
// Every other pet feature (Symptom Tracker, medications, questions
// about a pet) needs the pet on file first.
// API: GET  /api/owner/pets/profiles
//      POST /api/owner/pets {name, species, breed, birth_date, weight}
// (src/routes/pets.py)
// ------------------------------------------------------------

const SPECIES = ['Dog', 'Cat', 'Bird', 'Rabbit', 'Reptile', 'Fish', 'Other']
const ICONS = { Dog: '🐶', Cat: '🐱', Bird: '🐦', Rabbit: '🐰', Reptile: '🦎', Fish: '🐟' }
const EMPTY = { name: '', species: 'Dog', breed: '', birth_date: '', weight: '' }

function today() {
  const d = new Date()
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset())
  return d.toISOString().slice(0, 10)
}

// "2018-04-12" -> "7 years" / "8 months"
function age(birthDate) {
  const born = new Date(`${String(birthDate).slice(0, 10)}T00:00`)
  const now = new Date()
  let months = (now.getFullYear() - born.getFullYear()) * 12 + now.getMonth() - born.getMonth()
  if (now.getDate() < born.getDate()) months -= 1
  if (months < 12) return `${Math.max(months, 0)} ${months === 1 ? 'month' : 'months'}`
  const years = Math.floor(months / 12)
  return `${years} ${years === 1 ? 'year' : 'years'}`
}

function birthday(birthDate) {
  return new Date(`${String(birthDate).slice(0, 10)}T00:00`)
    .toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}

function MyPets() {
  const { user } = useAuth()
  const [form, setForm] = useState(EMPTY)
  const [message, setMessage] = useState(null)
  const [saving, setSaving] = useState(false)
  const [newId, setNewId] = useState(null)

  const result = useApiData('/owner/pets/profiles')
  const d = result.status === 200 ? result.data : null

  function change(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setMessage(null)
    setSaving(true)
    const res = await apiPost('/owner/pets', form, user.token)
    setSaving(false)
    if (res.ok) {
      setMessage({ ok: true, text: res.data.message })
      setNewId(res.data.pet.pet_id)
      setForm(EMPTY)
      result.reload()
    } else {
      setMessage({ ok: false, text: res.data.message || 'Could not add the pet.' })
    }
  }

  return (
    <UseCaseLayout title="My Pets" subtitle="Add each of your pets so you can track their health." result={result}>
      <div className="uc-split">
        <form className="uc-form uc-panel" onSubmit={handleSubmit} noValidate>
          <h2 className="uc-section-title">Add a pet</h2>

          <label htmlFor="name">Name</label>
          <input id="name" name="name" value={form.name} onChange={change} maxLength={100} placeholder="For example: Daisy" />

          <label htmlFor="species">Species</label>
          <select id="species" name="species" value={form.species} onChange={change}>
            {SPECIES.map((s) => <option key={s} value={s}>{s}</option>)}
          </select>

          <label htmlFor="breed">Breed</label>
          <input id="breed" name="breed" value={form.breed} onChange={change} maxLength={100}
                 placeholder="For example: Beagle, or Mixed" />

          <label htmlFor="birth_date">Birth date</label>
          <input id="birth_date" name="birth_date" type="date" max={today()} value={form.birth_date} onChange={change} />

          <label htmlFor="weight">Weight (lb)</label>
          <input id="weight" name="weight" type="number" min="0.1" step="0.1" value={form.weight} onChange={change}
                 placeholder="For example: 22.5" />

          {message && (
            <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
          )}
          <button type="submit" className="primary-button uc-button" disabled={saving}>
            {saving ? 'Saving…' : 'Add pet'}
          </button>
        </form>

        <section>
          <h2 className="uc-section-title">Your pets {d && `(${d.count})`}</h2>
          <div className="uc-list">
            {d && d.pets.map((p) => (
              <article key={p.pet_id} className={`uc-card${p.pet_id === newId ? ' uc-new' : ''}`}>
                <header className="uc-card-head">
                  <span className="uc-avatar" aria-hidden="true">{ICONS[p.species] || '🐾'}</span>
                  <div>
                    <strong>{p.name}</strong>
                    <div className="uc-muted uc-small">{p.species} · {p.breed}</div>
                  </div>
                </header>
                <dl className="uc-details">
                  <dt>Age</dt><dd>{age(p.birth_date)} (born {birthday(p.birth_date)})</dd>
                  <dt>Weight</dt><dd>{p.weight} lb</dd>
                  <dt>Health records</dt>
                  <dd>
                    {p.symptoms} {p.symptoms === 1 ? 'symptom' : 'symptoms'} · {p.allergies} {p.allergies === 1 ? 'allergy' : 'allergies'} · {p.conditions} {p.conditions === 1 ? 'condition' : 'conditions'}
                  </dd>
                </dl>
                <Link to="/owner/symptoms" className="uc-chip">Record a symptom</Link>
              </article>
            ))}
            {d && d.count === 0 && <p className="uc-empty">No pets yet. Add your first pet with the form.</p>}
          </div>
        </section>
      </div>
    </UseCaseLayout>
  )
}

export default MyPets
