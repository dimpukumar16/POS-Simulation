import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Loading from '../components/Loading'
import { getSalesHistory } from '../api/reports'
import { handleApiError } from '../api/config'

function Transactions({ user, onLogout }) {
  const [transactions, setTransactions] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [selectedTransaction, setSelectedTransaction] = useState(null)

  useEffect(() => {
    loadTransactions()
  }, [])

  const loadTransactions = async () => {
    setLoading(true)
    try {
      const data = await getSalesHistory()
      setTransactions(data.transactions || [])
      setError('')
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setLoading(false)
    }
  }

  const getStatusBadge = (status) => {
    const styles = {
      completed: 'bg-green-100 text-green-800',
      pending: 'bg-yellow-100 text-yellow-800',
      voided: 'bg-red-100 text-red-800',
      refund: 'bg-orange-100 text-orange-800'
    }
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-semibold ${styles[status] || 'bg-gray-100 text-gray-800'}`}>
        {status}
      </span>
    )
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar user={user} onLogout={onLogout} />

      <div className="container mx-auto p-4">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">💰 Transaction History</h1>
          <button
            onClick={loadTransactions}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 font-semibold"
          >
            🔄 Refresh
          </button>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {loading ? (
          <Loading message="Loading transactions..." />
        ) : (
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            {transactions.length === 0 ? (
              <div className="p-12 text-center text-gray-500">
                <p className="text-4xl mb-4">📝</p>
                <p className="text-xl">No transactions found</p>
                <p className="text-sm mt-2">Complete your first sale to see it here</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50 border-b">
                    <tr>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Transaction #</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Date</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Type</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Payment</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Items</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Total</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Status</th>
                      <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-200">
                    {transactions.map(tx => (
                      <tr key={tx.id} className="hover:bg-gray-50">
                        <td className="px-4 py-3 text-sm font-mono">{tx.transaction_number}</td>
                        <td className="px-4 py-3 text-sm">
                          {new Date(tx.created_at).toLocaleDateString()}<br/>
                          <span className="text-xs text-gray-500">
                            {new Date(tx.created_at).toLocaleTimeString()}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-sm capitalize">{tx.transaction_type}</td>
                        <td className="px-4 py-3 text-sm capitalize">{tx.payment_method}</td>
                        <td className="px-4 py-3 text-sm">{tx.items?.length || 0}</td>
                        <td className="px-4 py-3 text-sm font-bold text-green-600">
                          ${Math.abs(tx.total_amount).toFixed(2)}
                        </td>
                        <td className="px-4 py-3 text-sm">{getStatusBadge(tx.status)}</td>
                        <td className="px-4 py-3 text-sm">
                          <button
                            onClick={() => setSelectedTransaction(tx)}
                            className="text-blue-600 hover:text-blue-800 font-semibold"
                          >
                            View
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        )}

        {/* Transaction Details Modal */}
        {selectedTransaction && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="flex justify-between items-center p-4 border-b">
                <h2 className="text-xl font-bold">Transaction Details</h2>
                <button
                  onClick={() => setSelectedTransaction(null)}
                  className="text-gray-500 hover:text-gray-700 text-2xl"
                >
                  ×
                </button>
              </div>
              <div className="p-6 space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm text-gray-600">Transaction Number</p>
                    <p className="font-mono font-semibold">{selectedTransaction.transaction_number}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Date & Time</p>
                    <p className="font-semibold">
                      {new Date(selectedTransaction.created_at).toLocaleString()}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Payment Method</p>
                    <p className="font-semibold capitalize">{selectedTransaction.payment_method}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Status</p>
                    <p>{getStatusBadge(selectedTransaction.status)}</p>
                  </div>
                </div>

                <div className="border-t pt-4">
                  <h3 className="font-bold mb-3">Items</h3>
                  <div className="space-y-2">
                    {selectedTransaction.items?.map((item, idx) => (
                      <div key={idx} className="flex justify-between bg-gray-50 p-3 rounded">
                        <div>
                          <p className="font-semibold">{item.product_name || `Product #${item.product_id}`}</p>
                          <p className="text-sm text-gray-600">
                            {item.quantity} × ${item.unit_price}
                          </p>
                        </div>
                        <p className="font-bold">${item.line_total}</p>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border-t pt-4 space-y-2">
                  <div className="flex justify-between">
                    <span>Subtotal:</span>
                    <span>${selectedTransaction.subtotal}</span>
                  </div>
                  {selectedTransaction.discount_amount > 0 && (
                    <div className="flex justify-between text-green-600">
                      <span>Discount:</span>
                      <span>-${selectedTransaction.discount_amount}</span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span>Tax:</span>
                    <span>${selectedTransaction.tax_amount}</span>
                  </div>
                  <div className="flex justify-between text-lg font-bold border-t pt-2">
                    <span>Total:</span>
                    <span>${Math.abs(selectedTransaction.total_amount).toFixed(2)}</span>
                  </div>
                  {selectedTransaction.change_given > 0 && (
                    <div className="flex justify-between text-blue-600">
                      <span>Change Given:</span>
                      <span>${selectedTransaction.change_given}</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Transactions
