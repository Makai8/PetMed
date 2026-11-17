import { useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthContext.jsx'
import { roles } from '../auth/roles.js'
import logo from '../assets/petmed-logo.png'
import '../Splash.css'

// ------------------------------------------------------------
// Short welcome splash shown once right after signing in, on top
// of the role's dashboard: logo, name and role. It fades out by
// itself after about a second and a half; a click skips it.
// AuthContext sets the "petmedSplash" flag when a user signs in.
// ------------------------------------------------------------

const ROLE_ICONS = {
  pet_owner: '🐾',
  veterinarian: '🩺',
  pet_health_expert: '🎓',
  community_moderator: '🛡️',
  administrator: '⚙️',
}
const SHOW_MS = 1500
const FADE_MS = 400

function takeSplashFlag() {
  try {
    const show = sessionStorage.getItem('petmedSplash') === '1'
    sessionStorage.removeItem('petmedSplash')
    return show
  } catch {
    return false
  }
}

function WelcomeSplash() {
  const { user } = useAuth()
  const [stage, setStage] = useState(() => (takeSplashFlag() ? 'show' : 'done'))

  useEffect(() => {
    if (stage !== 'show') return undefined
    const fade = setTimeout(() => setStage('fade'), SHOW_MS)
    return () => clearTimeout(fade)
  }, [stage])

  useEffect(() => {
    if (stage !== 'fade') return undefined
    const done = setTimeout(() => setStage('done'), FADE_MS)
    return () => clearTimeout(done)
  }, [stage])

  if (stage === 'done' || !user) return null

  const role = roles[user.role]
  const parts = user.name.split(' ')
  const name = parts[0] === 'Dr.' ? `Dr. ${parts[parts.length - 1]}` : parts[0]

  return (
    <div className={`splash splash-${user.role}${stage === 'fade' ? ' splash-out' : ''}`}
         role="status" aria-live="polite" onClick={() => setStage('fade')}>
      <div className="splash-card">
        <img src={logo} alt="PetMed logo" className="splash-logo" />
        <p className="splash-hello">Welcome, {name}!</p>
        <p className="splash-role">
          <span aria-hidden="true">{ROLE_ICONS[user.role]}</span> {role.label}
        </p>
        <div className="splash-bar" aria-hidden="true"><span /></div>
      </div>
    </div>
  )
}

export default WelcomeSplash
