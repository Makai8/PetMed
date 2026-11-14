import { useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthContext.jsx'
import { apiGet } from './petmedApi.js'

// Loads `path` from the API for the signed in user, again whenever `path`
// changes (for example after a new search). Returns
// { loading, status, data } and keeps the last results while reloading.
export default function useApiData(path) {
  const { user } = useAuth()
  const [result, setResult] = useState({ status: null, data: null, path: null })

  useEffect(() => {
    let cancelled = false
    apiGet(path, user.token).then((res) => {
      if (!cancelled) setResult({ status: res.status, data: res.data, path })
    })
    return () => {
      cancelled = true
    }
  }, [path, user.token])

  return { ...result, loading: result.path !== path }
}
