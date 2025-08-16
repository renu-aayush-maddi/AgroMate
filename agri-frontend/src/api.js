// src/shared/api.js
import axios from 'axios'

export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8080'

export function buildClient(token, sessionId) {
  const client = axios.create({
    baseURL: API_BASE,
    timeout: 60000,
  })
  client.interceptors.request.use((config) => {
    if (token) config.headers.Authorization = `Bearer ${token}`
    if (sessionId) config.headers['X-Session-Id'] = sessionId
    return config
  })
  return client
}

export async function getOrCreateProfile(client) {
  const { data } = await client.post('/me', {})
  return data
}

export async function updateProfile(client, payload) {
  const { data } = await client.post('/me', payload)
  return data
}
