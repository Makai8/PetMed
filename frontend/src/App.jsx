import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext.jsx'
import RequireRole from './auth/RequireRole.jsx'
import Home from './pages/Home.jsx'
import Login from './pages/Login.jsx'
import Dashboard from './pages/Dashboard.jsx'
import UseCasePage from './pages/UseCasePage.jsx'
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
          <Route path="/unauthorized" element={<Unauthorized />} />

          {/* Pet Owner */}
          <Route path="/owner" element={<RequireRole role="pet_owner"><Dashboard /></RequireRole>} />
          <Route path="/owner/feed" element={<RequireRole role="pet_owner"><UseCasePage title="Community Feed" description="Pet health posts and discussions from the PetMed community." /></RequireRole>} />

          {/* Veterinarian */}
          <Route path="/vet" element={<RequireRole role="veterinarian"><Dashboard /></RequireRole>} />
          <Route path="/vet/questions" element={<RequireRole role="veterinarian"><UseCasePage title="Pet Health Questions" description="Questions submitted by pet owners." /></RequireRole>} />

          {/* Pet Health Expert */}
          <Route path="/expert" element={<RequireRole role="pet_health_expert"><Dashboard /></RequireRole>} />
          <Route path="/expert/questions" element={<RequireRole role="pet_health_expert"><UseCasePage title="Questions in My Expertise" description="Posts and questions in your approved area of expertise." /></RequireRole>} />

          {/* Community Moderator */}
          <Route path="/moderator" element={<RequireRole role="community_moderator"><Dashboard /></RequireRole>} />
          <Route path="/moderator/reports" element={<RequireRole role="community_moderator"><UseCasePage title="Reported Posts and Advice" description="Content reported by PetMed users." /></RequireRole>} />

          {/* Administrator */}
          <Route path="/admin" element={<RequireRole role="administrator"><Dashboard /></RequireRole>} />
          <Route path="/admin/users" element={<RequireRole role="administrator"><UseCasePage title="Manage Users" description="Search and list PetMed user accounts." /></RequireRole>} />

          {/* Any unknown address goes home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
