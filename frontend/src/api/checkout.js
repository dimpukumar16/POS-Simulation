import axios from 'axios'
import { API_BASE_URL, getAuthHeader } from './config'

export const getTransactions = async (params = {}) => {
  const response = await axios.get(
    `${API_BASE_URL}/reports/history`,
    {
      params,
      headers: getAuthHeader()
    }
  )
  return response.data
}

export const processCheckout = async (paymentMethod, amountPaid = 0, paymentReference = null) => {
  const response = await axios.post(
    `${API_BASE_URL}/checkout/process`,
    {
      payment_method: paymentMethod,
      amount_paid: amountPaid,
      payment_reference: paymentReference
    },
    { headers: getAuthHeader() }
  )
  return response.data
}

export const processRefund = async (transactionId, reason, managerPin) => {
  const response = await axios.post(
    `${API_BASE_URL}/checkout/refund`,
    {
      transaction_id: transactionId,
      reason,
      manager_pin: managerPin
    },
    { headers: getAuthHeader() }
  )
  return response.data
}

export const voidTransaction = async (transactionId, reason, managerPin) => {
  const response = await axios.post(
    `${API_BASE_URL}/checkout/void`,
    {
      transaction_id: transactionId,
      reason,
      manager_pin: managerPin
    },
    { headers: getAuthHeader() }
  )
  return response.data
}
