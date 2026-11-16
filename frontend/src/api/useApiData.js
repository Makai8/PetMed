import { useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthContext.jsx'
import { apiGet } from './petmedApi.js'

// Loads `path` from the API for the signed in user, again whenever `path`
// changes (for example after a new search) or reload() is called. Returns
// { loading, status, data, reload } and keeps the last results while reloading.
export default function useApiData(path) {
  const { user } = useAuth()
  const [result, setResult] = useState({ status: null, data: null, path: null })
  const [version, setVersion] = useState(0)

  useEffect(() => {
    let cancelled = false
    apiGet(path, user.token).then((res) => {
      if (!cancelled) setResult({ status: res.status, data: res.data, path })
    })
    return () => {
      cancelled = true
    }
  }, [path, user.token, version])

  return { ...result, loading: result.path !== path, reload: () => setVersion((v) => v + 1) }
}
