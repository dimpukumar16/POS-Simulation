import { useState } from 'react'
import Navbar from '../components/Navbar'
import Loading from '../components/Loading'
import { getSalesReport, getInventoryReport } from '../api/reports'
import { handleApiError } from '../api/config'

function Reports({ user, onLogout }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [reportType, setReportType] = useState('sales')
  const [salesData, setSalesData] = useState(null)
  const [inventoryData, setInventoryData] = useState(null)
  const [startDate, setStartDate] = useState('')
  const [endDate, setEndDate] = useState('')

  const handleGenerateReport = async () => {
    setLoading(true)
    setError('')
    try {
      if (reportType === 'sales') {
        const start = startDate || new Date().toISOString().split('T')[0]
        const end = endDate || new Date().toISOString().split('T')[0]
        const data = await getSalesReport(start, end)
        setSalesData(data)
        setInventoryData(null)
      } else if (reportType === 'inventory') {
        const data = await getInventoryReport()
        setInventoryData(data)
        setSalesData(null)
      }
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar user={user} onLogout={onLogout} />

      <div className="container mx-auto p-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-6">📊 Reports & Analytics</h1>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Report Generator */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Generate Report</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Report Type</label>
              <select
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="sales">Sales Report</option>
                <option value="inventory">Inventory Report</option>
              </select>
            </div>

            {reportType === 'sales' && (
              <>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">Start Date</label>
                  <input
                    type="date"
                    value={startDate}
                    onChange={(e) => setStartDate(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-2">End Date</label>
                  <input
                    type="date"
                    value={endDate}
                    onChange={(e) => setEndDate(e.target.value)}
                    className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                  />
                </div>
              </>
            )}

            <div className="flex items-end">
              <button
                onClick={handleGenerateReport}
                disabled={loading}
                className="w-full bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 font-semibold disabled:bg-gray-400"
              >
                {loading ? 'Generating...' : 'Generate Report'}
              </button>
            </div>
          </div>
        </div>

        {/* Sales Report */}
        {salesData && (
          <div className="bg-white rounded-xl shadow-md p-6 mb-6">
            <h2 className="text-2xl font-bold mb-6">Sales Report</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Sales</p>
                <p className="text-2xl font-bold text-blue-600">
                  ${salesData.summary?.total_sales || 0}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Transactions</p>
                <p className="text-2xl font-bold text-green-600">
                  {salesData.summary?.total_transactions || 0}
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Average Sale</p>
                <p className="text-2xl font-bold text-purple-600">
                  ${salesData.summary?.average_sale || 0}
                </p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Items Sold</p>
                <p className="text-2xl font-bold text-orange-600">
                  {salesData.summary?.items_sold || 0}
                </p>
              </div>
            </div>

            {salesData.transactions?.length > 0 && (
              <div>
                <h3 className="font-bold mb-3">Recent Transactions</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50 border-b">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Transaction #</th>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Date</th>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Payment</th>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Total</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {salesData.transactions.map(tx => (
                        <tr key={tx.id} className="hover:bg-gray-50">
                          <td className="px-4 py-2 text-sm font-mono">{tx.transaction_number}</td>
                          <td className="px-4 py-2 text-sm">{new Date(tx.created_at).toLocaleString()}</td>
                          <td className="px-4 py-2 text-sm capitalize">{tx.payment_method}</td>
                          <td className="px-4 py-2 text-sm font-bold text-green-600">${tx.total_amount}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Inventory Report */}
        {inventoryData && (
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-2xl font-bold mb-6">Inventory Report</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Products</p>
                <p className="text-2xl font-bold text-blue-600">
                  {inventoryData.summary?.total_products || 0}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Stock Value</p>
                <p className="text-2xl font-bold text-green-600">
                  ${inventoryData.summary?.total_value || 0}
                </p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Low Stock Items</p>
                <p className="text-2xl font-bold text-orange-600">
                  {inventoryData.summary?.low_stock_count || 0}
                </p>
              </div>
            </div>

            {inventoryData.products?.length > 0 && (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b">
                    <tr>
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Product</th>
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Barcode</th>
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Stock</th>
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Reorder Level</th>
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Price</th>
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y">
                    {inventoryData.products.map(product => (
                      <tr key={product.id} className="hover:bg-gray-50">
                        <td className="px-4 py-2 text-sm font-semibold">{product.name}</td>
                        <td className="px-4 py-2 text-sm font-mono">{product.barcode}</td>
                        <td className="px-4 py-2 text-sm">
                          <span className={product.stock_quantity <= product.reorder_level ? 'text-orange-600 font-semibold' : ''}>
                            {product.stock_quantity}
                          </span>
                        </td>
                        <td className="px-4 py-2 text-sm">{product.reorder_level}</td>
                        <td className="px-4 py-2 text-sm font-bold text-green-600">${product.price}</td>
                        <td className="px-4 py-2 text-sm">
                          {product.stock_quantity <= product.reorder_level ? (
                            <span className="bg-orange-100 text-orange-800 px-2 py-1 rounded-full text-xs font-semibold">
                              Low Stock
                            </span>
                          ) : (
                            <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-semibold">
                              In Stock
                            </span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {!salesData && !inventoryData && !loading && (
          <div className="bg-white rounded-xl shadow-md p-12 text-center text-gray-500">
            <p className="text-4xl mb-4">📈</p>
            <p className="text-xl">Generate a report to view analytics</p>
            <p className="text-sm mt-2">Select report type and click Generate Report</p>
          </div>
        )}

        {loading && <Loading message="Generating report..." />}
      </div>
    </div>
  )
}

export default Reports
