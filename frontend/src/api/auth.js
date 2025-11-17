import axios from 'axios'
import { API_BASE_URL, getAuthHeader } from './config'

export const login = async (username, password) => {
  const response = await axios.post(`${API_BASE_URL}/auth/login`, {
    username,
    password
  })
  return response.data
}

export const logout = async () => {
  const response = await axios.post(
    `${API_BASE_URL}/auth/logout`,
    {},
    {
      headers: getAuthHeader()
    }
  )
  return response.data
}

export const getCurrentUser = async () => {
  const response = await axios.get(`${API_BASE_URL}/auth/me`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const changePassword = async (oldPassword, newPassword) => {
  const response = await axios.post(
    `${API_BASE_URL}/auth/change-password`,
    { old_password: oldPassword, new_password: newPassword },
    { headers: getAuthHeader() }
  )
  return response.data
}

export const refreshToken = async (refreshToken) => {
  const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
    refresh_token: refreshToken
  })
  return response.data
}

export const verifyPin = async (pin, action) => {
  const response = await axios.post(
    `${API_BASE_URL}/auth/verify-pin`,
    { pin, action },
    { headers: getAuthHeader() }
  )
  return response.data
}

export const revokeToken = async (refreshToken) => {
  const response = await axios.post(
    `${API_BASE_URL}/auth/revoke-token`,
    { refresh_token: refreshToken },
    { headers: getAuthHeader() }
  )
  return response.data
}
