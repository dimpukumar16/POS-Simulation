import api from './config'

/**
 * Get all refunds
 * @param {Object} params - Query parameters
 * @returns {Promise} Response with refunds array
 */
export const getRefunds = async (params = {}) => {
  const response = await api.get('/refunds', { params })
  return response.data
}

/**
 * Get refund by ID
 * @param {number} refundId - Refund ID
 * @returns {Promise} Response with refund details
 */
export const getRefund = async (refundId) => {
  const response = await api.get(`/refunds/${refundId}`)
  return response.data
}

/**
 * Create a refund for a transaction
 * @param {number} transactionId - Transaction ID to refund
 * @param {Object} refundData - Refund details
 * @returns {Promise} Response with created refund
 */
export const createRefund = async (transactionId, refundData) => {
  const response = await api.post(`/refunds/transaction/${transactionId}`, refundData)
  return response.data
}

/**
 * Cancel a pending refund
 * @param {number} refundId - Refund ID to cancel
 * @returns {Promise} Response with cancellation confirmation
 */
export const cancelRefund = async (refundId) => {
  const response = await api.post(`/refunds/${refundId}/cancel`)
  return response.data
}
