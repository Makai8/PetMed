import heroImg from './assets/hero.png'
import './App.css'

function App() {
  return (
    <div className="app">
      <header className="navbar">
        <div className="brand">
          <div className="logo-mark">🐶</div>
          <h2>PetMed</h2>
        </div>

        <nav className="nav-links">
          <a href="#home">Home</a>
          <a href="#about">About</a>
          <a href="#shop">PetMed Shop</a>
          <a href="#community">Community</a>
          <a href="#help">Help</a>
        </nav>

        <div className="nav-buttons">
          <button className="login-btn">Log In</button>
          <button className="signup-btn">Sign Up</button>
        </div>
      </header>

      <main id="home" className="hero-section">
        <div className="hero-text">
          <p className="eyebrow">Trusted pet health and wellness</p>

          <h1>
            Better Health.
            <br />
            <span>Happier Pets.</span>
            <br />
            Stronger Together.
          </h1>

          <p className="hero-description">
            PetMed helps pet owners manage their pets&apos; health, connect with
            veterinarians and pet health experts, track important health
            information, and join a trusted pet-health community.
          </p>

          <div className="hero-buttons">
            <button className="primary-btn">Get Started Here</button>
            <button className="secondary-btn">Learn More</button>
          </div>
        </div>

        <div className="hero-image-wrap">
          <img
            src={heroImg}
            className="hero-image"
            alt="Happy pets representing PetMed"
          />
        </div>
      </main>

      <section className="feature-section">
        <div className="feature-card">
          <div className="feature-icon">💚</div>
          <h3>Track Pet Health</h3>
          <p>
            Manage pet profiles, medications, symptoms, health records, and
            other important information.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">🩺</div>
          <h3>Ask Experts</h3>
          <p>
            Connect with verified veterinarians and pet health experts for
            guidance.
          </p>
        </div>

        <div className="feature-card">
          <div className="feature-icon">💬</div>
          <h3>Join the Community</h3>
          <p>
            Share experiences, ask questions, and learn from other pet owners.
          </p>
        </div>

        <div id="shop" className="feature-card">
          <div className="feature-icon">🛒</div>
          <h3>PetMed Shop</h3>
          <p>
            Browse trusted pet-health products, wellness resources, and pet
            essentials.
          </p>
        </div>
      </section>

      <section id="about" className="about-section">
        <h2>Healthier Pets Start Here</h2>

        <p>
          PetMed brings pet owners, veterinarians, experts, and the community
          together in one place to make pet health information easier to manage
          and understand.
        </p>
      </section>

      <footer className="footer">
        <div>
          <strong>PetMed</strong>
          <p>Healthy Pets. Happier Lives.</p>
        </div>

        <div className="footer-links">
          <a href="#about">About</a>
          <a href="#help">Help</a>
          <a href="#community">Community</a>
          <a href="#shop">PetMed Shop</a>
        </div>
      </footer>
    </div>
  )
}

export default App