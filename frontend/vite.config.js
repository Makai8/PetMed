import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Forward /api requests to the Python API (python src/app.py, port 4000)
    proxy: {
      '/api': 'http://127.0.0.1:4000',
    },
    // Let classmates open the site on the same Wi-Fi or through a
    // Cloudflare link (docs/Sharing_Live_Demo.md)
    host: true,
    allowedHosts: ['.trycloudflare.com'],
  },
})
