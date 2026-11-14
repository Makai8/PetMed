import { useState } from 'react'
import { formatDate } from '../api/petmedApi.js'
import useApiData from '../api/useApiData.js'
import { roles } from '../auth/roles.js'
import UseCaseLayout from '../components/UseCaseLayout.jsx'

// ------------------------------------------------------------
// Administrator use case: search, browse and list users.
// Data: GET /api/admin/users?q=&role=&status=  (src/routes/admin.py)
// ------------------------------------------------------------

function ManageUsers() {
  const [text, setText] = useState('')
  const [search, setSearch] = useState('')
  const [role, setRole] = useState('')
  const [status, setStatus] = useState('')

  const result = useApiData(`/admin/users?${new URLSearchParams({ q: search, role, status })}`)
  const d = result.status === 200 ? result.data : null

  return (
    <UseCaseLayout title="Manage Users" subtitle="Search, browse and list PetMed user accounts." result={result}>
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
      </form>

      {d && (
        <>
          <p className="uc-count">{d.count} {d.count === 1 ? 'user' : 'users'} found</p>
          <div className="uc-table-wrap">
            <table className="uc-table">
              <thead>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Role</th><th>Status</th><th>Joined</th></tr>
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
                  </tr>
                ))}
                {d.count === 0 && <tr><td colSpan="6" className="uc-empty">No users match your search.</td></tr>}
              </tbody>
            </table>
          </div>
        </>
      )}
    </UseCaseLayout>
  )
}

export default ManageUsers
