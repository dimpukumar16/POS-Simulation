import { useState, useEffect } from 'react'
import Navbar from '../components/Navbar'
import Loading from '../components/Loading'
import ManagerOverride from '../components/ManagerOverride'
import { getTransactions, processRefund as processRefundAPI } from '../api/checkout'
import { getRefunds } from '../api/refunds'
import { verifyPin } from '../api/auth'
import { handleApiError } from '../api/config'

function Refunds({ user, onLogout }) {
  const [transactions, setTransactions] = useState([])
  const [refunds, setRefunds] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [searchTxn, setSearchTxn] = useState('')
  const [selectedTransaction, setSelectedTransaction] = useState(null)
  const [refundReason, setRefundReason] = useState('')
  const [refundAmount, setRefundAmount] = useState('')
  const [processing, setProcessing] = useState(false)
  const [showOverride, setShowOverride] = useState(false)
  const [pendingRefund, setPendingRefund] = useState(null)
  const [overrideToken, setOverrideToken] = useState(null)
  const [activeTab, setActiveTab] = useState('search') // 'search' or 'history'

  useEffect(() => {
    loadRefundHistory()
  }, [])

  const loadRefundHistory = async () => {
    try {
      setLoading(true)
      // Get transactions with type='refund'
      const data = await getTransactions({ limit: 100 })
      // Filter for refund transactions
      const refundTransactions = data.transactions?.filter(tx => tx.transaction_type === 'refund') || []
      setRefunds(refundTransactions)
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setLoading(false)
    }
  }

  const searchTransaction = async () => {
    if (!searchTxn) {
      setError('Please enter a transaction number')
      return
    }

    try {
      setLoading(true)
      setError('')
      const data = await getTransactions({ transaction_number: searchTxn })
      
      if (data.transactions && data.transactions.length > 0) {
        const txn = data.transactions[0]
        
        // Check if transaction can be refunded
        if (txn.status === 'voided') {
          setError('Cannot refund a voided transaction')
          return
        }
        
        if (txn.status === 'refunded') {
          setError('Transaction has already been fully refunded')
          return
        }
        
        setSelectedTransaction(txn)
        setRefundAmount(txn.total_amount.toString())
      } else {
        setError('Transaction not found')
        setSelectedTransaction(null)
      }
    } catch (err) {
      setError(handleApiError(err))
      setSelectedTransaction(null)
    } finally {
      setLoading(false)
    }
  }

  const handleRefundRequest = () => {
    if (!selectedTransaction) {
      setError('No transaction selected')
      return
    }

    if (!refundReason) {
      setError('Please enter a refund reason')
      return
    }

    const amountCents = Math.round(parseFloat(refundAmount || selectedTransaction.total_amount) * 100)
    
    const refundData = {
      transactionId: selectedTransaction.id,
      reason: refundReason,
      amount_cents: amountCents
    }

    setPendingRefund(refundData)

    // Check if user has manager/admin role
    if (user.role === 'manager' || user.role === 'administrator') {
      // Manager/Admin can use their own PIN
      // Show override modal to get their PIN
      setShowOverride(true)
    } else {
      // Cashier requires manager override
      setShowOverride(true)
    }
  }

  const handleManagerAuthorize = async (pin) => {
    try {
      // Process the pending refund with manager PIN
      if (pendingRefund) {
        await processRefund(pendingRefund, pin)
      }
      
      setShowOverride(false)
    } catch (err) {
      throw new Error(handleApiError(err))
    }
  }

  const processRefund = async (refundData, managerPin = null) => {
    try {
      setProcessing(true)
      setError('')

      // Use the checkout refund endpoint which expects manager_pin
      const response = await processRefundAPI(
        refundData.transactionId,
        refundData.reason,
        managerPin || user.pin // Use manager PIN from override or current user's PIN
      )

      alert(`✅ Refund Processed Successfully!\n\nTransaction: ${response.refund_transaction.transaction_number}\nAmount: $${Math.abs(response.refund_transaction.total_amount).toFixed(2)}\n\nInventory has been restocked.`)

      // Reset form
      setSelectedTransaction(null)
      setSearchTxn('')
      setRefundReason('')
      setRefundAmount('')
      setPendingRefund(null)
      
      // Refresh refund history
      loadRefundHistory()
      setActiveTab('history')
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setProcessing(false)
    }
  }

  if (loading && refunds.length === 0) return <Loading />

  // Check permissions
  if (user.role !== 'manager' && user.role !== 'administrator') {
    return (
      <div className="min-h-screen bg-gray-50">
        <Navbar user={user} onLogout={onLogout} />
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <svg className="mx-auto h-12 w-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h3 className="mt-2 text-lg font-medium text-red-800">Access Denied</h3>
            <p className="mt-1 text-sm text-red-600">You do not have permission to access refunds. Manager or Administrator role required.</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar user={user} onLogout={onLogout} />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Refund Management</h1>
          <p className="mt-2 text-sm text-gray-600">Process refunds and view refund history</p>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow mb-6">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('search')}
                className={`py-4 px-6 font-medium text-sm border-b-2 ${
                  activeTab === 'search'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Process Refund
              </button>
              <button
                onClick={() => setActiveTab('history')}
                className={`py-4 px-6 font-medium text-sm border-b-2 ${
                  activeTab === 'history'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Refund History ({refunds.length})
              </button>
            </nav>
          </div>

          <div className="p-6">
            {activeTab === 'search' ? (
              <div>
                {/* Search Transaction */}
                <div className="mb-6">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Transaction Number
                  </label>
                  <div className="flex space-x-2">
                    <input
                      type="text"
                      value={searchTxn}
                      onChange={(e) => setSearchTxn(e.target.value.toUpperCase())}
                      onKeyPress={(e) => e.key === 'Enter' && searchTransaction()}
                      placeholder="TXN-20231027123456"
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    />
                    <button
                      onClick={searchTransaction}
                      disabled={loading}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                    >
                      {loading ? 'Searching...' : 'Search'}
                    </button>
                  </div>
                </div>

                {/* Transaction Details */}
                {selectedTransaction && (
                  <div className="border border-gray-200 rounded-lg p-6 mb-6 bg-gray-50">
                    <h3 className="text-lg font-semibold mb-4">Transaction Details</h3>
                    <div className="grid grid-cols-2 gap-4 mb-4">
                      <div>
                        <p className="text-sm text-gray-600">Transaction Number</p>
                        <p className="font-semibold">{selectedTransaction.transaction_number}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Date</p>
                        <p className="font-semibold">
                          {new Date(selectedTransaction.created_at).toLocaleString()}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Cashier</p>
                        <p className="font-semibold">{selectedTransaction.cashier || 'Unknown'}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-600">Total Amount</p>
                        <p className="font-semibold text-lg">${selectedTransaction.total_amount.toFixed(2)}</p>
                      </div>
                    </div>

                    {/* Items */}
                    {selectedTransaction.items && selectedTransaction.items.length > 0 && (
                      <div className="mt-4">
                        <p className="text-sm font-medium text-gray-700 mb-2">Items</p>
                        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden">
                          <table className="min-w-full">
                            <thead className="bg-gray-50">
                              <tr>
                                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500">Product</th>
                                <th className="px-4 py-2 text-center text-xs font-medium text-gray-500">Qty</th>
                                <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">Price</th>
                                <th className="px-4 py-2 text-right text-xs font-medium text-gray-500">Total</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-gray-200">
                              {selectedTransaction.items.map((item, idx) => (
                                <tr key={idx}>
                                  <td className="px-4 py-2 text-sm">{item.product_name}</td>
                                  <td className="px-4 py-2 text-sm text-center">{item.quantity}</td>
                                  <td className="px-4 py-2 text-sm text-right">${item.unit_price.toFixed(2)}</td>
                                  <td className="px-4 py-2 text-sm text-right font-semibold">${item.line_total.toFixed(2)}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </div>
                    )}

                    {/* Refund Form */}
                    <div className="mt-6 pt-6 border-t border-gray-200">
                      <h4 className="text-md font-semibold mb-4">Refund Details</h4>
                      
                      <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Refund Amount
                        </label>
                        <input
                          type="number"
                          step="0.01"
                          value={refundAmount}
                          onChange={(e) => setRefundAmount(e.target.value)}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          placeholder="0.00"
                        />
                        <p className="mt-1 text-xs text-gray-500">Leave empty for full refund</p>
                      </div>

                      <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Reason for Refund <span className="text-red-500">*</span>
                        </label>
                        <textarea
                          value={refundReason}
                          onChange={(e) => setRefundReason(e.target.value)}
                          rows={3}
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                          placeholder="Enter reason for refund..."
                        />
                      </div>

                      <button
                        onClick={handleRefundRequest}
                        disabled={processing || !refundReason}
                        className="w-full px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
                      >
                        {processing ? 'Processing Refund...' : 'Process Refund'}
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              /* Refund History */
              <div>
                {refunds.length === 0 ? (
                  <div className="text-center py-12">
                    <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <h3 className="mt-2 text-sm font-medium text-gray-900">No refunds found</h3>
                    <p className="mt-1 text-sm text-gray-500">No refunds have been processed yet.</p>
                  </div>
                ) : (
                  <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Transaction #
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Reason
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Amount
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Processed By
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Date
                          </th>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Status
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {refunds.map((refund) => (
                          <tr key={refund.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                              {refund.transaction_number}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {refund.refund_reason || 'N/A'}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm font-semibold text-red-600">
                              ${Math.abs(refund.total_amount).toFixed(2)}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {refund.cashier_name || 'Unknown'}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                              {new Date(refund.created_at).toLocaleString()}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                refund.status === 'completed'
                                  ? 'bg-green-100 text-green-800'
                                  : refund.status === 'pending'
                                  ? 'bg-yellow-100 text-yellow-800'
                                  : 'bg-red-100 text-red-800'
                              }`}>
                                {refund.status}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Manager Override Modal */}
      <ManagerOverride
        isOpen={showOverride}
        onClose={() => setShowOverride(false)}
        onAuthorize={handleManagerAuthorize}
        action={`Refund transaction ${selectedTransaction?.transaction_number}`}
      />
    </div>
  )
}

export default Refunds
