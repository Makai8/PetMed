// ------------------------------------------------------------
// Reads data from the PetMed API (python src/app.py, port 4000).
// Every request sends the signed in user's token, and the API
// checks the user's role again before returning any data.
// ------------------------------------------------------------

// Empty = same address as the website. Vite forwards every /api request to
// the API on port 4000 (vite.config.js), so this also works through a shared link.
const API_URL = ''

// Returns { ok, status, data }. HTTP errors don't throw, so each
// page can show the server's own message (for example a 403).
export async function apiGet(path, token) {
  try {
    const response = await fetch(`${API_URL}/api${path}`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    const data = await response.json().catch(() => ({}))
    return { ok: response.ok, status: response.status, data }
  } catch {
    return {
      ok: false,
      status: 0,
      data: { message: 'Cannot reach the PetMed API. Start it with: python src/app.py' },
    }
  }
}

// Sends JSON to the API (used by sign up). Same reply shape as apiGet.
export async function apiPost(path, body) {
  try {
    const response = await fetch(`${API_URL}/api${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    })
    const data = await response.json().catch(() => ({}))
    return { ok: response.ok, status: response.status, data }
  } catch {
    return {
      ok: false,
      status: 0,
      data: { message: 'Cannot reach the PetMed API. Start it with: python src/app.py' },
    }
  }
}

// "2026-10-28 10:00:00" -> "Oct 28, 2026"
export function formatDate(value) {
  if (!value) return ''
  const date = new Date(String(value).replace(' ', 'T'))
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
