import { createContext, useContext, useState } from 'react'
import { loginRequest } from './authApi.js'

// ------------------------------------------------------------
// Remembers who is signed in, for every page in the app.
// The signed in user is kept in sessionStorage, so a page
// refresh keeps them signed in until they log out.
// ------------------------------------------------------------

const AuthContext = createContext(null)

function readSavedUser() {
  try {
    const saved = sessionStorage.getItem('petmedUser')
    return saved ? JSON.parse(saved) : null
  } catch {
    return null
  }
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(readSavedUser)

  async function login(email, password) {
    const signedIn = await loginRequest(email, password)
    sessionStorage.setItem('petmedUser', JSON.stringify(signedIn))
    setUser(signedIn)
    return signedIn
  }

  function logout() {
    sessionStorage.removeItem('petmedUser')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
