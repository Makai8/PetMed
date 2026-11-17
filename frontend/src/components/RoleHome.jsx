import { Link } from 'react-router-dom'
import { formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import '../RoleHome.css'

// ------------------------------------------------------------
// The top of each role's home screen: live numbers and short lists
// that matter to that role, from GET /api/home?role= (src/routes/home.py).
// The full feature menu stays below it on the dashboard.
// ------------------------------------------------------------

const PET_ICONS = { Dog: '🐶', Cat: '🐱', Bird: '🐦' }
const KIND_LABELS = { post: 'Post', advice: 'Health advice', user: 'User', product: 'Product', comment: 'Comment' }

function Panel({ title, action, children }) {
  return (
    <section className="rh-panel">
      <header className="rh-panel-head">
        <h2>{title}</h2>
        {action}
      </header>
      {children}
    </section>
  )
}

function Empty({ children }) {
  return <p className="rh-empty">{children}</p>
}

function PetOwnerHome({ d }) {
  return (
    <div className="rh-panels">
      <Panel title="My pets">
        {d.pets.length === 0 ? <Empty>No pets yet. Adding pets is coming soon.</Empty> : (
          <div className="rh-pets">
            {d.pets.map((p) => (
              <div key={p.pet_id} className="rh-pet">
                <span className="rh-pet-icon" aria-hidden="true">{PET_ICONS[p.species] || '🐾'}</span>
                <strong>{p.name}</strong>
                <small>{p.breed} · {p.weight} lbs</small>
              </div>
            ))}
          </div>
        )}
      </Panel>
      <Panel title="My recent questions">
        {d.questions.length === 0 ? <Empty>You haven't asked a question yet.</Empty> : (
          <ul className="rh-list">
            {d.questions.map((q) => (
              <li key={q.question_id}>
                <span>“{q.question_text}”</span>
                <small>{formatDate(q.created_at)} · {q.answers > 0 ? `${q.answers} ${q.answers === 1 ? 'answer' : 'answers'}` : 'waiting for an answer'}</small>
              </li>
            ))}
          </ul>
        )}
      </Panel>
      <Panel title="Upcoming reminders" action={<Link to="/owner/feed" className="rh-link">Community Feed →</Link>}>
        {d.reminders.length === 0 ? <Empty>No reminders scheduled.</Empty> : (
          <ul className="rh-list">
            {d.reminders.map((r, i) => (
              <li key={i}>
                <span>{r.medication ? `${r.medication} for ${r.pet_name}` : `Check-in for ${r.pet_name}`}</span>
                <small>{formatDate(r.due_at)}</small>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  )
}

function VetHome({ d }) {
  return (
    <div className="rh-panels">
      <Panel title="Waiting for a vet" action={<Link to="/vet/questions" className="rh-link">All questions →</Link>}>
        {d.questions.length === 0 ? <Empty>Every question has an answer. Nice work!</Empty> : (
          <ul className="rh-list">
            {d.questions.map((q) => (
              <li key={q.question_id}>
                <span>“{q.question_text}”</span>
                <small>
                  {q.asked_by}{q.pet_name && <> · {q.pet_name}</>} · {formatDate(q.created_at)}
                  {q.sent_to_me && <b className="rh-tag">Sent to you</b>}
                </small>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  )
}

function ExpertHome({ d }) {
  if (!d.profile) return <Empty>Your expert profile hasn't been set up yet.</Empty>
  return (
    <div className="rh-panels">
      <Panel title="My expertise">
        <p className="rh-specialty">
          <span className="rh-badge">{d.profile.specialty}</span>
          <span className={`rh-status rh-status-${d.profile.verification_status}`}>{d.profile.verification_status}</span>
        </p>
        <p className="rh-muted">{d.profile.organization}</p>
      </Panel>
      <Panel title={`Latest in #${d.tag}`} action={<Link to="/expert/questions" className="rh-link">My expertise feed →</Link>}>
        {d.posts.length === 0 ? <Empty>No posts in your specialty yet.</Empty> : (
          <ul className="rh-list">
            {d.posts.map((p) => (
              <li key={p.post_id}>
                <span>{p.body}</span>
                <small>{p.author} · {formatDate(p.created_at)}</small>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  )
}

function ModeratorHome({ d }) {
  return (
    <div className="rh-panels">
      <Panel title="Newest open reports" action={<Link to="/moderator/reports" className="rh-link">Review reports →</Link>}>
        {d.reports.length === 0 ? <Empty>No open reports. The community is quiet.</Empty> : (
          <ul className="rh-list">
            {d.reports.map((r) => (
              <li key={r.report_id}>
                <span><b className="rh-tag">{KIND_LABELS[r.kind]}</b> {r.reason}</span>
                <small>Reported by {r.reported_by} · {formatDate(r.created_at)}</small>
              </li>
            ))}
          </ul>
        )}
      </Panel>
    </div>
  )
}

function AdminHome({ d }) {
  return (
    <div className="rh-panels">
      <Panel title="Newest members" action={<Link to="/admin/users" className="rh-link">Manage users →</Link>}>
        <ul className="rh-list">
          {d.newest_users.map((u) => (
            <li key={u.user_id}>
              <span>{u.full_name} <small className="rh-inline">{u.email}</small></span>
              <small>Joined {formatDate(u.created_at)} · {u.account_status}</small>
            </li>
          ))}
        </ul>
      </Panel>
      <Panel title="Waiting on you" action={<Link to="/admin/role-requests" className="rh-link">Role requests →</Link>}>
        <p className="rh-muted">Approve or reject people who asked to become a vet, expert, moderator or administrator.</p>
      </Panel>
    </div>
  )
}

const VIEWS = {
  pet_owner: PetOwnerHome,
  veterinarian: VetHome,
  pet_health_expert: ExpertHome,
  community_moderator: ModeratorHome,
  administrator: AdminHome,
}

function RoleHome() {
  const { user } = useAuth()
  const result = useApiData(`/home?${new URLSearchParams({ role: user.role })}`)
  const d = result.status === 200 ? result.data : null
  const View = VIEWS[user.role]

  if (!result.data) return <p className="rh-muted rh-loading">Loading your home screen…</p>
  if (!d) return <p className="rh-muted rh-loading">{result.data.message || 'Your home screen could not load.'}</p>

  return (
    <div className={`rh rh-${user.role}`}>
      <div className="rh-stats">
        {d.stats.map((s) => (
          <div key={s.label} className="rh-stat">
            <strong>{s.value}</strong>
            <span>{s.label}</span>
          </div>
        ))}
      </div>
      <View d={d} />
      <h2 className="rh-all">All features</h2>
    </div>
  )
}

export default RoleHome
