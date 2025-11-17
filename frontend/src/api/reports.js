import axios from 'axios'
import { API_BASE_URL, getAuthHeader } from './config'

export const getSalesReport = async (startDate, endDate, filters = {}) => {
  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate,
    ...filters
  })
  const response = await axios.get(`${API_BASE_URL}/reports/sales?${params}`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const getInventoryReport = async () => {
  const response = await axios.get(`${API_BASE_URL}/reports/inventory`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const getSalesHistory = async (filters = {}) => {
  const params = new URLSearchParams(filters)
  const response = await axios.get(`${API_BASE_URL}/reports/history?${params}`, {
    headers: getAuthHeader()
  })
  return response.data
}

export const exportReport = async (reportType, format, filters = {}) => {
  const params = new URLSearchParams({
    type: reportType,
    format,
    ...filters
  })
  const response = await axios.get(`${API_BASE_URL}/reports/export?${params}`, {
    headers: getAuthHeader(),
    responseType: 'blob'
  })
  return response.data
}
