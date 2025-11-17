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
        const response = await getSalesReport(start, end)
        // Backend returns data wrapped in 'report' key
        setSalesData(response.report || response)
        setInventoryData(null)
      } else if (reportType === 'inventory') {
        const response = await getInventoryReport()
        // Backend returns data wrapped in 'report' key
        setInventoryData(response.report || response)
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
                <p className="text-sm text-gray-600 mb-1">Net Sales</p>
                <p className="text-2xl font-bold text-blue-600">
                  ${salesData.summary?.net_sales?.toFixed(2) || '0.00'}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Transactions</p>
                <p className="text-2xl font-bold text-green-600">
                  {salesData.summary?.sales_count || 0}
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Average Transaction</p>
                <p className="text-2xl font-bold text-purple-600">
                  ${salesData.summary?.average_transaction?.toFixed(2) || '0.00'}
                </p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Refunds</p>
                <p className="text-2xl font-bold text-orange-600">
                  ${salesData.summary?.total_refunds?.toFixed(2) || '0.00'}
                </p>
              </div>
            </div>

            {/* Payment Methods */}
            {salesData.payment_methods && Object.keys(salesData.payment_methods).length > 0 && (
              <div className="mb-6">
                <h3 className="font-bold mb-3">Payment Methods</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {Object.entries(salesData.payment_methods).map(([method, data]) => (
                    <div key={method} className="bg-gray-50 p-4 rounded-lg">
                      <p className="text-sm text-gray-600 capitalize">{method}</p>
                      <p className="text-xl font-bold">${data.total?.toFixed(2)}</p>
                      <p className="text-xs text-gray-500">{data.count} transactions</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Top Products */}
            {salesData.top_products?.length > 0 && (
              <div>
                <h3 className="font-bold mb-3">Top Products</h3>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50 border-b">
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Product</th>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Quantity Sold</th>
                        <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Revenue</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y">
                      {salesData.top_products.slice(0, 10).map((product, idx) => (
                        <tr key={idx} className="hover:bg-gray-50">
                          <td className="px-4 py-2 text-sm font-semibold">{product.name}</td>
                          <td className="px-4 py-2 text-sm">{product.quantity}</td>
                          <td className="px-4 py-2 text-sm font-bold text-green-600">${product.revenue?.toFixed(2)}</td>
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
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Products</p>
                <p className="text-2xl font-bold text-blue-600">
                  {inventoryData.summary?.total_products || 0}
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Total Inventory Value</p>
                <p className="text-2xl font-bold text-green-600">
                  ${inventoryData.summary?.total_inventory_value?.toFixed(2) || '0.00'}
                </p>
              </div>
              <div className="bg-orange-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Low Stock Items</p>
                <p className="text-2xl font-bold text-orange-600">
                  {inventoryData.summary?.low_stock_items || 0}
                </p>
              </div>
              <div className="bg-red-50 p-4 rounded-lg">
                <p className="text-sm text-gray-600 mb-1">Out of Stock</p>
                <p className="text-2xl font-bold text-red-600">
                  {inventoryData.summary?.out_of_stock_items || 0}
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
                      <th className="px-4 py-2 text-left text-xs font-semibold text-gray-600">Category</th>
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
                        <td className="px-4 py-2 text-sm">{product.category || 'N/A'}</td>
                        <td className="px-4 py-2 text-sm">
                          <span className={product.stock_quantity <= product.reorder_level ? 'text-orange-600 font-semibold' : ''}>
                            {product.stock_quantity}
                          </span>
                        </td>
                        <td className="px-4 py-2 text-sm">{product.reorder_level}</td>
                        <td className="px-4 py-2 text-sm font-bold text-green-600">${product.price?.toFixed(2)}</td>
                        <td className="px-4 py-2 text-sm">
                          {product.stock_quantity === 0 ? (
                            <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-semibold">
                              Out of Stock
                            </span>
                          ) : product.stock_quantity <= product.reorder_level ? (
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
