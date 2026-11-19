import { Link } from 'react-router-dom'
import logo from '../assets/petmed-logo.png'
import '../App.css'

// Public landing page: top bar, centered hero with a preview of the
// signed in dashboard, three features, and a sign up band.
function Home() {
  return (
    <div className="landing">
      <header className="topbar">
        <div className="topbar-inner">
          <Link to="/" className="brand" aria-label="PetMed home">
            <img src={logo} alt="" aria-hidden="true" />
            <span>PetMed</span>
          </Link>

          <nav className="topbar-links" aria-label="Main navigation">
            <a href="#about">About</a>
            <a href="#help">Help</a>
            <a href="#contact">Contact Us</a>
          </nav>

          <div className="topbar-actions">
            <Link to="/login" className="topbar-login">Login</Link>
            <Link to="/signup" className="primary-button">Sign Up</Link>
          </div>
        </div>
      </header>

      <main>
        <section className="landing-hero" id="home">
          <span className="hero-pill">🐾 Pet health + community</span>
          <h1>Healthy pets.<br /><span>Happier lives.</span></h1>
          <p className="tagline">
            PetMed helps pet owners organize health information, track care,
            and connect with trusted pet-health professionals and the community.
          </p>

          <div className="hero-actions">
            <Link to="/login" className="primary-button">Get Started Here!</Link>
            <a href="#about" className="secondary-button">Learn More</a>
          </div>

          <ul className="audience" aria-label="Who PetMed is for">
            <li>🐶 Pet Owners</li>
            <li>🩺 Veterinarians</li>
            <li>🎓 Pet Health Experts</li>
            <li>🛡️ Community Moderators</li>
          </ul>

          <div className="preview" aria-hidden="true">
            <div className="preview-bar"><span /><span /><span /></div>
            <div className="preview-body">
              <div className="preview-side">
                <span className="on">🏠 Home</span>
                <span>📰 Community Feed</span>
                <span>🐶 My Pets</span>
                <span>💊 Medications</span>
                <span>❓ Ask for Advice</span>
              </div>
              <div className="preview-main">
                <h3>Good morning, Maya.</h3>
                <div className="preview-stats">
                  <div><strong>2</strong><small>My pets</small></div>
                  <div><strong>3</strong><small>Questions asked</small></div>
                  <div><strong>1</strong><small>Reminders</small></div>
                </div>
                <div className="preview-row">💊 Medication reminder for Buddy <small>6:00 PM</small></div>
                <div className="preview-row">📅 Annual checkup <small>Next week</small></div>
              </div>
            </div>
          </div>
        </section>

        <section className="features" id="about">
          <div className="section-head">
            <p className="eyebrow">WHY PETMED</p>
            <h2>Everything your pet's health needs, in one place</h2>
          </div>
          <div className="feature-grid">
            <article className="feature">
              <div className="feature-icon" aria-hidden="true">🩺</div>
              <h3>Health Tracking</h3>
              <p>Profiles, medications, symptoms, and reminders.</p>
            </article>
            <article className="feature">
              <div className="feature-icon" aria-hidden="true">💬</div>
              <h3>Helpful Community</h3>
              <p>Ask questions and share pet-care experiences.</p>
            </article>
            <article className="feature">
              <div className="feature-icon" aria-hidden="true">✅</div>
              <h3>Professional Guidance</h3>
              <p>Clearly identify verified veterinarians and experts.</p>
            </article>
          </div>
        </section>

        <section className="cta" id="help">
          <h2>Ready to get started?</h2>
          <p>Create a free account and add your first pet in minutes.</p>
          <Link to="/signup" className="primary-button">Create an account</Link>
        </section>
      </main>

      <footer className="site-footer" id="contact">
        <span>PetMed • Healthy pets. Happier lives.</span>
        <span>Pet health and community in one place.</span>
      </footer>
    </div>
  )
}

export default Home
