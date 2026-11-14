import { Link, useNavigate } from 'react-router-dom'
import logo from '../assets/petmed-logo.png'
import '../App.css'

function Home() {
  // Lets the buttons send the user to another page
  const navigate = useNavigate()

  return (
    <div className="app-shell">
      <header className="site-header">
        <div className="brand" aria-label="PetMed home">
          <img className="brand-mark" src={logo} alt="" aria-hidden="true" />
          <span>PetMed</span>
        </div>

        <nav className="main-nav" aria-label="Main navigation">
          <Link to="/login">Login</Link>
          <Link to="/signup">Sign Up</Link>
          <a href="#about">About</a>
          <a href="#help">Help</a>
          <a href="#contact">Contact Us</a>
        </nav>
      </header>

      <main>
        <section className="hero" id="home">
          <div className="hero-copy">
            <p className="eyebrow">PET HEALTH + COMMUNITY</p>
            <h1>Healthy pets.<br /><span>Happier lives.</span></h1>
            <p className="tagline">
              PetMed helps pet owners organize health information, track care,
              and connect with trusted pet-health professionals and the community.
            </p>

            <div className="hero-actions">
              <button type="button" className="primary-button" onClick={() => navigate('/login')}>Get Started Here!</button>
              <button type="button" className="secondary-button">Learn More</button>
            </div>

            <div className="feature-row" aria-label="PetMed highlights">
              <div className="feature-card">
                <span aria-hidden="true">🩺</span>
                <div>
                  <strong>Health Tracking</strong>
                  <small>Profiles, medications, symptoms, and reminders.</small>
                </div>
              </div>
              <div className="feature-card">
                <span aria-hidden="true">💬</span>
                <div>
                  <strong>Helpful Community</strong>
                  <small>Ask questions and share pet-care experiences.</small>
                </div>
              </div>
              <div className="feature-card">
                <span aria-hidden="true">✅</span>
                <div>
                  <strong>Professional Guidance</strong>
                  <small>Clearly identify verified veterinarians and experts.</small>
                </div>
              </div>
            </div>
          </div>

          <div className="hero-visual" aria-label="PetMed application preview placeholder">
            <div className="visual-card">
              <div className="pet-icons" aria-hidden="true">
                <span>🐶</span>
                <span>🐱</span>
              </div>
              <div className="phone-frame">
                <div className="phone-header">
                  <img className="mini-logo" src={logo} alt="" />
                  <strong>PetMed</strong>
                </div>
                <div className="health-card">
                  <div className="health-icon">❤</div>
                  <div>
                    <strong>Buddy</strong>
                    <span>Health profile ready</span>
                  </div>
                </div>
                <div className="health-card">
                  <div className="health-icon">💊</div>
                  <div>
                    <strong>Medication reminder</strong>
                    <span>Next dose at 6:00 PM</span>
                  </div>
                </div>
                <div className="health-card">
                  <div className="health-icon">📅</div>
                  <div>
                    <strong>Next appointment</strong>
                    <span>Annual checkup</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer className="site-footer">
        <span>PetMed • Healthy pets. Happier lives.</span>
        <span>Pet health and community in one place.</span>
      </footer>
    </div>
  );
}

export default Home
