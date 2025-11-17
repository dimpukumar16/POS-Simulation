import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export const getAuthHeader = () => {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error
    return error.response.data?.error || error.response.data?.message || 'An error occurred'
  } else if (error.request) {
    // Request made but no response
    return 'Server not responding. Please check if the backend is running.'
  } else {
    // Something else happened
    return error.message || 'An unexpected error occurred'
  }
}

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
})

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
