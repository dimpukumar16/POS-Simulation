import axios from 'axios'
import { API_BASE_URL, getAuthHeader } from './config'

export const getCart = async () => {
  const response = await axios.get(`${API_BASE_URL}/cart`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const addToCart = async (productId, barcode, quantity = 1) => {
  const body = {}
  if (productId) body.product_id = productId
  if (barcode) body.barcode = barcode
  body.quantity = quantity

  const response = await axios.post(
    `${API_BASE_URL}/cart/add`,
    body,
    { headers: getAuthHeader() }
  )
  return response.data
}

export const updateCartItem = async (cartItemId, quantity) => {
  const response = await axios.put(
    `${API_BASE_URL}/cart/update`,
    { cart_item_id: cartItemId, quantity },
    { headers: getAuthHeader() }
  )
  return response.data
}

export const removeFromCart = async (cartItemId) => {
  const response = await axios.delete(`${API_BASE_URL}/cart/remove/${cartItemId}`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const clearCart = async () => {
  const response = await axios.delete(`${API_BASE_URL}/cart/clear`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const applyDiscount = async (type, amount, managerOverride = false) => {
  const response = await axios.post(
    `${API_BASE_URL}/cart/discount`,
    { type, amount, manager_override: managerOverride },
    { headers: getAuthHeader() }
  )
  return response.data
}
