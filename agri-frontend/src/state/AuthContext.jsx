import React, { createContext, useContext, useEffect, useState } from 'react'

const AuthCtx = createContext(null)
export const useAuth = () => useContext(AuthCtx)

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('token') || '')
  const [sessionId, setSessionId] = useState(localStorage.getItem('session_id') || '')
  const [profile, setProfile] = useState(null)

  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
  }, [token])

  useEffect(() => {
    if (sessionId) localStorage.setItem('session_id', sessionId)
  }, [sessionId])

  const logout = () => {
    setToken('')
    setProfile(null)
  }

  return (
    <AuthCtx.Provider value={{ token, setToken, sessionId, setSessionId, profile, setProfile, logout }}>
      {children}
    </AuthCtx.Provider>
  )
}
