import api from './config'

/**
 * Get all settings
 * @param {Object} params - Query parameters (category, public_only)
 * @returns {Promise} Response with settings array
 */
export const getSettings = async (params = {}) => {
  const response = await api.get('/settings', { params })
  return response.data
}

/**
 * Get setting by key
 * @param {string} key - Setting key
 * @returns {Promise} Response with setting details
 */
export const getSetting = async (key) => {
  const response = await api.get(`/settings/${key}`)
  return response.data
}

/**
 * Update a setting (admin only)
 * @param {string} key - Setting key
 * @param {Object} settingData - Setting data (value, description, etc.)
 * @returns {Promise} Response with updated setting
 */
export const updateSetting = async (key, settingData) => {
  const response = await api.put(`/settings/${key}`, settingData)
  return response.data
}

/**
 * Create a new setting (admin only)
 * @param {Object} settingData - Setting data (key, value, description, etc.)
 * @returns {Promise} Response with created setting
 */
export const createSetting = async (settingData) => {
  const response = await api.post('/settings', settingData)
  return response.data
}

/**
 * Delete a setting (admin only)
 * @param {string} key - Setting key
 * @returns {Promise} Response with deletion confirmation
 */
export const deleteSetting = async (key) => {
  const response = await api.delete(`/settings/${key}`)
  return response.data
}
