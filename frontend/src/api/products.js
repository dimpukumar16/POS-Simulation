import axios from 'axios'
import { API_BASE_URL, getAuthHeader } from './config'

export const getProducts = async (filters = {}) => {
  const params = new URLSearchParams(filters)
  const response = await axios.get(`${API_BASE_URL}/products?${params}`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const getProductByBarcode = async (barcode) => {
  const response = await axios.get(`${API_BASE_URL}/products/${barcode}`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const getProductById = async (productId) => {
  const response = await axios.get(`${API_BASE_URL}/products/id/${productId}`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const createProduct = async (productData) => {
  const response = await axios.post(`${API_BASE_URL}/products`, productData, {
    headers: getAuthHeader()
  })
  return response.data
}

export const updateProduct = async (productId, productData) => {
  const response = await axios.put(`${API_BASE_URL}/products/${productId}`, productData, {
    headers: getAuthHeader()
  })
  return response.data
}

export const deleteProduct = async (productId) => {
  const response = await axios.delete(`${API_BASE_URL}/products/${productId}`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const getCategories = async () => {
  const response = await axios.get(`${API_BASE_URL}/products/categories`, {
    headers: getAuthHeader()
  })
  return response.data
}
