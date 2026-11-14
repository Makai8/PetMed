import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext.jsx'
import RequireRole from './auth/RequireRole.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Signup from './pages/Signup.jsx'
import Dashboard from './pages/Dashboard.jsx'
import CommunityFeed from './pages/CommunityFeed.jsx'
import HealthQuestions from './pages/HealthQuestions.jsx'
import ExpertQuestions from './pages/ExpertQuestions.jsx'
import ReportedContent from './pages/ReportedContent.jsx'
import ManageUsers from './pages/ManageUsers.jsx'
import Unauthorized from './pages/Unauthorized.jsx'
import './App.css'

// ------------------------------------------------------------
// All pages in the app. Every role page is wrapped in
// RequireRole, so only that role can open it.
// ------------------------------------------------------------

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/unauthorized" element={<Unauthorized />} />

          {/* Pet Owner */}
          <Route path="/owner" element={<RequireRole role="pet_owner"><Dashboard /></RequireRole>} />
          <Route path="/owner/feed" element={<RequireRole role="pet_owner"><CommunityFeed /></RequireRole>} />

          {/* Veterinarian */}
          <Route path="/vet" element={<RequireRole role="veterinarian"><Dashboard /></RequireRole>} />
          <Route path="/vet/questions" element={<RequireRole role="veterinarian"><HealthQuestions /></RequireRole>} />

          {/* Pet Health Expert */}
          <Route path="/expert" element={<RequireRole role="pet_health_expert"><Dashboard /></RequireRole>} />
          <Route path="/expert/questions" element={<RequireRole role="pet_health_expert"><ExpertQuestions /></RequireRole>} />

          {/* Community Moderator */}
          <Route path="/moderator" element={<RequireRole role="community_moderator"><Dashboard /></RequireRole>} />
          <Route path="/moderator/reports" element={<RequireRole role="community_moderator"><ReportedContent /></RequireRole>} />

          {/* Administrator */}
          <Route path="/admin" element={<RequireRole role="administrator"><Dashboard /></RequireRole>} />
          <Route path="/admin/users" element={<RequireRole role="administrator"><ManageUsers /></RequireRole>} />

          {/* Any unknown address goes home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
