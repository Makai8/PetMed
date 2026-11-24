import { useState } from 'react'
import { apiPost, formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Administrator: manage user accounts.
// Sprint IV: search, browse and list users.
//   GET  /api/admin/users?q=&role=&status=
// Account management: suspend or reactivate a user, add a user.
//   POST /api/admin/users/<user_id>/status {status, reason}
//   POST /api/admin/users {full_name, email, password, role}
// (src/routes/admin.py)
// ------------------------------------------------------------

// Vets and experts are not created here: they apply and get verified.
const CREATABLE = ['pet_owner', 'community_moderator', 'administrator']
const EMPTY_USER = { full_name: '', email: '', password: '', role: 'pet_owner' }

function ManageUsers() {
  const { user } = useAuth()
  const [text, setText] = useState('')
  const [search, setSearch] = useState('')
  const [role, setRole] = useState('')
  const [status, setStatus] = useState('')

  const [message, setMessage] = useState(null)
  const [suspending, setSuspending] = useState(null) // user_id whose reason box is open
  const [reason, setReason] = useState('')
  const [busy, setBusy] = useState(null)
  const [adding, setAdding] = useState(false)
  const [newUser, setNewUser] = useState(EMPTY_USER)
  const [addMessage, setAddMessage] = useState(null)

  const result = useApiData(`/admin/users?${new URLSearchParams({ q: search, role, status })}`)
  const d = result.status === 200 ? result.data : null

  async function changeStatus(u, newStatus) {
    setBusy(u.user_id)
    setMessage(null)
    const res = await apiPost(`/admin/users/${u.user_id}/status`, { status: newStatus, reason }, user.token)
    setBusy(null)
    setMessage({ ok: res.ok, text: res.data.message || 'Could not change the account.' })
    if (res.ok) {
      setSuspending(null)
      setReason('')
      result.reload()
    }
  }

  async function addUser(e) {
    e.preventDefault()
    setAddMessage(null)
    const res = await apiPost('/admin/users', newUser, user.token)
    setAddMessage({ ok: res.ok, text: res.data.message || 'Could not add the user.' })
    if (res.ok) {
      setNewUser(EMPTY_USER)
      result.reload()
    }
  }

  function changeNew(e) {
    setNewUser({ ...newUser, [e.target.name]: e.target.value })
  }

  return (
    <UseCaseLayout title="Manage Users" subtitle="Search user accounts, suspend or reactivate them, and add new users."
                   result={result}>
      <form className="uc-toolbar" onSubmit={(e) => { e.preventDefault(); setSearch(text.trim()) }}>
        <input type="search" placeholder="Search name or email" value={text}
               onChange={(e) => setText(e.target.value)} aria-label="Search users" />
        <select value={role} onChange={(e) => setRole(e.target.value)} aria-label="Role">
          <option value="">All roles</option>
          {Object.entries(roles).map(([value, r]) => <option key={value} value={value}>{r.label}</option>)}
        </select>
        <select value={status} onChange={(e) => setStatus(e.target.value)} aria-label="Account status">
          <option value="">Any status</option>
          <option value="active">Active</option>
          <option value="suspended">Suspended</option>
        </select>
        <button className="primary-button uc-button" type="submit">Search</button>
        <button type="button" className="uc-chip" onClick={() => { setAdding(!adding); setAddMessage(null) }}>
          {adding ? 'Close' : '+ Add user'}
        </button>
      </form>

      {adding && (
        <form className="uc-form uc-panel uc-add-user" onSubmit={addUser} noValidate>
          <h2 className="uc-section-title">Add a user</h2>
          <div className="uc-add-grid">
            <div>
              <label htmlFor="full_name">Full name</label>
              <input id="full_name" name="full_name" value={newUser.full_name} onChange={changeNew} />
            </div>
            <div>
              <label htmlFor="email">Email</label>
              <input id="email" name="email" type="email" value={newUser.email} onChange={changeNew} />
            </div>
            <div>
              <label htmlFor="password">Temporary password</label>
              <input id="password" name="password" type="text" value={newUser.password} onChange={changeNew}
                     placeholder="8+ characters, a letter and a number" />
            </div>
            <div>
              <label htmlFor="new_role">Role</label>
              <select id="new_role" name="role" value={newUser.role} onChange={changeNew}>
                {CREATABLE.map((r) => <option key={r} value={r}>{roles[r].label}</option>)}
              </select>
            </div>
          </div>
          <p className="uc-muted uc-small">Veterinarians and pet health experts apply with credentials and are approved on Professional Verification.</p>
          {addMessage && (
            <p className={addMessage.ok ? 'uc-success' : 'login-error'} role={addMessage.ok ? 'status' : 'alert'}>{addMessage.text}</p>
          )}
          <button type="submit" className="primary-button uc-button">Add user</button>
        </form>
      )}

      {d && (
        <>
          <p className="uc-count">{d.count} {d.count === 1 ? 'user' : 'users'} found</p>
          {message && (
            <p className={message.ok ? 'uc-success' : 'login-error'} role={message.ok ? 'status' : 'alert'}>{message.text}</p>
          )}
          <div className="uc-table-wrap">
            <table className="uc-table">
              <thead>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Joined</th><th>Account</th></tr>
              </thead>
              <tbody>
                {d.users.map((u) => (
                  <tr key={u.user_id}>
                    <td className="uc-mono">{u.user_id}</td>
                    <td>{u.full_name}</td>
                    <td>{u.email}</td>
                    <td>{u.roles.map((r) => roles[r]?.label || r).join(', ')}</td>
                    <td><span className={`uc-pill uc-pill-${u.account_status}`}>{u.account_status}</span></td>
                    <td>{formatDate(u.created_at)}</td>
                    <td className="uc-actions">
                      {u.email === user.email ? <span className="uc-muted uc-small">You</span>
                        : u.account_status === 'suspended' ? (
                          <button type="button" className="uc-chip" disabled={busy === u.user_id}
                                  onClick={() => changeStatus(u, 'active')}>Reactivate</button>
                        ) : suspending === u.user_id ? (
                          <span className="uc-suspend">
                            <input aria-label={`Reason for suspending ${u.full_name}`} placeholder="Reason" value={reason}
                                   onChange={(e) => setReason(e.target.value)} />
                            <button type="button" className="uc-reject" disabled={busy === u.user_id}
                                    onClick={() => changeStatus(u, 'suspended')}>Suspend</button>
                            <button type="button" className="uc-chip" onClick={() => { setSuspending(null); setReason('') }}>Cancel</button>
                          </span>
                        ) : (
                          <button type="button" className="uc-chip"
                                  onClick={() => { setSuspending(u.user_id); setReason(''); setMessage(null) }}>Suspend</button>
                        )}
                    </td>
                  </tr>
                ))}
                {d.count === 0 && <tr><td colSpan="7" className="uc-empty">No users match your search.</td></tr>}
              </tbody>
            </table>
          </div>
        </>
      )}
    </UseCaseLayout>
  )
}

export default ManageUsers
