// ------------------------------------------------------------
// Sign in request.
// USE_TEST_USERS = true  -> checks the test list below (no backend needed)
// USE_TEST_USERS = false -> calls the real backend at POST /api/login
// Flip it to false once the backend login route is ready.
// ------------------------------------------------------------

const USE_TEST_USERS = false
// Empty = same address as the website; Vite forwards /api to the API (vite.config.js)
const API_URL = ''
const TEST_PASSWORD = 'PetMed123!'

// Same people as backend/seed.sql
const testUsers = [
  { userId: 87370000, email: 'maya.johnson@petmed.com', name: 'Maya Johnson', role: 'pet_owner', status: 'active' },
  { userId: 87370002, email: 'sofia.ramirez@petmed.com', name: 'Sofia Ramirez', role: 'pet_owner', status: 'suspended' },
  { userId: 87370003, email: 'dr.james.carter@petmed.com', name: 'Dr. James Carter', role: 'veterinarian', status: 'active' },
  { userId: 87370005, email: 'kevin.nguyen@petmed.com', name: 'Kevin Nguyen', role: 'pet_health_expert', status: 'active' },
  { userId: 87370006, email: 'tasha.brooks@petmed.com', name: 'Tasha Brooks', role: 'community_moderator', status: 'active' },
  { userId: 87370007, email: 'daniel.owens@petmed.com', name: 'Daniel Owens', role: 'administrator', status: 'active' },
]

// Returns { userId, name, email, role, token } or throws an Error with a message
export async function loginRequest(email, password) {
  if (USE_TEST_USERS) {
    const user = testUsers.find((u) => u.email === email.trim().toLowerCase())

    if (!user || password !== TEST_PASSWORD) {
      throw new Error('Invalid email or password.')
    }
    if (user.status !== 'active') {
      throw new Error('This account is suspended. Contact PetMed support.')
    }
    return { userId: user.userId, name: user.name, email: user.email, role: user.role, token: 'test-token' }
  }

  const response = await fetch(`${API_URL}/api/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.message || 'Invalid email or password.')
  }
  return data
}
