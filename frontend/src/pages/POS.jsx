import { useState, useEffect, useRef } from 'react'
import Navbar from '../components/Navbar'
import Modal from '../components/Modal'
import Loading from '../components/Loading'
import { getProducts } from '../api/products'
import { getCart, addToCart, updateCartItem, removeFromCart, clearCart, applyDiscount } from '../api/cart'
import { processCheckout } from '../api/checkout'
import { handleApiError } from '../api/config'

function POS({ user, onLogout }) {
  const [products, setProducts] = useState([])
  const [cart, setCart] = useState(null)
  const [search, setSearch] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [showCheckout, setShowCheckout] = useState(false)
  const [showDiscount, setShowDiscount] = useState(false)
  const [paymentMethod, setPaymentMethod] = useState('cash')
  const [amountPaid, setAmountPaid] = useState('')
  const [discountType, setDiscountType] = useState('percentage')
  const [discountAmount, setDiscountAmount] = useState('')
  const [processingPayment, setProcessingPayment] = useState(false)
  const searchInputRef = useRef(null)

  useEffect(() => {
    loadProducts()
    loadCart()
  }, [])

  const loadProducts = async () => {
    try {
      setLoading(true)
      const data = await getProducts({ active: 'true' })
      setProducts(data.products || [])
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setLoading(false)
    }
  }

  const loadCart = async () => {
    try {
      const data = await getCart()
      setCart(data.cart)
    } catch (err) {
      console.error('Failed to load cart:', err)
      setCart({ items: [], total: 0, subtotal: 0, tax_amount: 0, item_count: 0 })
    }
  }

  const handleAddToCart = async (product) => {
    try {
      const data = await addToCart(product.id, null, 1)
      setCart(data.cart)
      setError('')
    } catch (err) {
      setError(handleApiError(err))
    }
  }

  const handleUpdateQuantity = async (cartItemId, quantity) => {
    if (quantity < 0) return
    try {
      const data = await updateCartItem(cartItemId, quantity)
      setCart(data.cart)
      setError('')
    } catch (err) {
      setError(handleApiError(err))
    }
  }

  const handleRemoveItem = async (cartItemId) => {
    try {
      const data = await removeFromCart(cartItemId)
      setCart(data.cart)
      setError('')
    } catch (err) {
      setError(handleApiError(err))
    }
  }

  const handleClearCart = async () => {
    if (window.confirm('Clear entire cart? This cannot be undone.')) {
      try {
        await clearCart()
        await loadCart()
        setError('')
      } catch (err) {
        setError(handleApiError(err))
      }
    }
  }

  const handleApplyDiscount = async () => {
    if (!discountAmount || parseFloat(discountAmount) <= 0) {
      alert('Please enter a valid discount amount')
      return
    }

    try {
      const data = await applyDiscount(discountType, parseFloat(discountAmount), false)
      setCart(data.cart)
      setShowDiscount(false)
      setDiscountAmount('')
      setError('')
    } catch (err) {
      setError(handleApiError(err))
    }
  }

  const handleCheckout = async () => {
    if (!cart?.items?.length) {
      alert('Cart is empty')
      return
    }

    if (paymentMethod === 'cash' && !amountPaid) {
      alert('Please enter amount paid')
      return
    }

    setProcessingPayment(true)
    try {
      const paid = paymentMethod === 'cash' ? parseFloat(amountPaid) : cart.total
      const data = await processCheckout(paymentMethod, paid, null)
      
      alert(`✅ Payment Successful!\nTransaction: ${data.transaction.transaction_number}\nTotal: $${data.transaction.total_amount}\nChange: $${data.transaction.change_given || 0}`)
      
      setShowCheckout(false)
      setAmountPaid('')
      await loadCart()
      setError('')
    } catch (err) {
      setError(handleApiError(err))
    } finally {
      setProcessingPayment(false)
    }
  }

  const handleBarcodeSearch = (e) => {
    const value = e.target.value
    setSearch(value)
    
    // Auto-add product if exact barcode match
    if (value.length >= 8) {
      const product = products.find(p => p.barcode === value)
      if (product) {
        handleAddToCart(product)
        setSearch('')
        searchInputRef.current?.focus()
      }
    }
  }

  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    p.barcode.includes(search) ||
    (p.category && p.category.toLowerCase().includes(search.toLowerCase()))
  )

  const change = paymentMethod === 'cash' && amountPaid ? 
    (parseFloat(amountPaid) - (cart?.total || 0)).toFixed(2) : '0.00'

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar user={user} onLogout={onLogout} />

      <div className="container mx-auto p-4">
        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Products Section */}
          <div className="lg:col-span-2 bg-white rounded-xl shadow-md p-4">
            <div className="mb-4">
              <h2 className="text-2xl font-bold text-gray-800 mb-3">Products</h2>
              <input
                ref={searchInputRef}
                type="text"
                placeholder="🔍 Search by name, barcode, or category..."
                value={search}
                onChange={handleBarcodeSearch}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                autoFocus
              />
            </div>

            {loading ? (
              <Loading message="Loading products..." />
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[calc(100vh-280px)] overflow-y-auto pr-2">
                {filteredProducts.length === 0 ? (
                  <div className="col-span-2 text-center py-12 text-gray-500">
                    <p className="text-xl">📦 No products found</p>
                    <p className="text-sm mt-2">Try a different search term</p>
                  </div>
                ) : (
                  filteredProducts.map(product => (
                    <div
                      key={product.id}
                      className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-all cursor-pointer"
                      onClick={() => handleAddToCart(product)}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-lg text-gray-800">{product.name}</h3>
                        {product.stock_quantity <= product.reorder_level && (
                          <span className="bg-orange-100 text-orange-800 text-xs px-2 py-1 rounded">
                            Low Stock
                          </span>
                        )}
                      </div>
                      <p className="text-gray-500 text-sm mb-2">{product.barcode}</p>
                      {product.category && (
                        <p className="text-blue-600 text-xs mb-2">📁 {product.category}</p>
                      )}
                      <div className="flex justify-between items-center mt-3">
                        <p className="text-green-600 font-bold text-2xl">${product.price}</p>
                        <p className="text-gray-600 text-sm">
                          Stock: <span className="font-semibold">{product.stock_quantity}</span>
                        </p>
                      </div>
                      {product.stock_quantity === 0 && (
                        <div className="mt-2 bg-red-50 text-red-600 text-sm px-2 py-1 rounded text-center">
                          Out of Stock
                        </div>
                      )}
                    </div>
                  ))
                )}
              </div>
            )}
          </div>

          {/* Cart Section */}
          <div className="bg-white rounded-xl shadow-md p-4">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold text-gray-800">Cart</h2>
              {cart?.items?.length > 0 && (
                <button
                  onClick={handleClearCart}
                  className="text-red-500 hover:text-red-700 text-sm font-semibold"
                >
                  Clear All
                </button>
              )}
            </div>

            <div className="space-y-3 max-h-[calc(100vh-450px)] overflow-y-auto mb-4">
              {!cart?.items?.length ? (
                <div className="text-center py-12 text-gray-400">
                  <p className="text-4xl mb-2">🛒</p>
                  <p>Cart is empty</p>
                  <p className="text-sm mt-2">Add products to get started</p>
                </div>
              ) : (
                cart.items.map(item => (
                  <div key={item.cart_item_id} className="border-b pb-3">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1">
                        <h3 className="font-semibold text-gray-800">{item.name}</h3>
                        <p className="text-xs text-gray-500">${item.unit_price} each</p>
                      </div>
                      <button
                        onClick={() => handleRemoveItem(item.cart_item_id)}
                        className="text-red-500 hover:text-red-700 ml-2"
                      >
                        ✕
                      </button>
                    </div>
                    <div className="flex justify-between items-center">
                      <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
                        <button
                          onClick={() => handleUpdateQuantity(item.cart_item_id, item.quantity - 1)}
                          className="bg-white px-3 py-1 rounded hover:bg-gray-200 font-bold"
                        >
                          −
                        </button>
                        <span className="px-3 font-semibold">{item.quantity}</span>
                        <button
                          onClick={() => handleUpdateQuantity(item.cart_item_id, item.quantity + 1)}
                          className="bg-white px-3 py-1 rounded hover:bg-gray-200 font-bold"
                        >
                          +
                        </button>
                      </div>
                      <span className="font-bold text-lg">${item.line_total}</span>
                    </div>
                  </div>
                ))
              )}
            </div>

            {/* Cart Summary */}
            <div className="border-t pt-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Subtotal:</span>
                <span className="font-semibold">${cart?.subtotal || 0}</span>
              </div>
              {cart?.discount_amount > 0 && (
                <div className="flex justify-between text-sm text-green-600">
                  <span>Discount ({cart.discount_type}):</span>
                  <span className="font-semibold">-${cart.discount_amount}</span>
                </div>
              )}
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Tax:</span>
                <span className="font-semibold">${cart?.tax_amount || 0}</span>
              </div>
              <div className="flex justify-between text-lg font-bold border-t pt-2">
                <span>Total:</span>
                <span className="text-blue-600">${cart?.total || 0}</span>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-4 space-y-2">
              <button
                onClick={() => setShowDiscount(true)}
                disabled={!cart?.items?.length}
                className="w-full bg-yellow-500 text-white py-2 rounded-lg hover:bg-yellow-600 disabled:bg-gray-300 transition-all font-semibold"
              >
                Apply Discount
              </button>
              <button
                onClick={() => setShowCheckout(true)}
                disabled={!cart?.items?.length}
                className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-300 transition-all font-bold text-lg shadow-md"
              >
                💳 Checkout (${cart?.total || 0})
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Checkout Modal */}
      <Modal
        isOpen={showCheckout}
        onClose={() => !processingPayment && setShowCheckout(false)}
        title="Process Payment"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-gray-700 font-semibold mb-2">Payment Method</label>
            <div className="grid grid-cols-3 gap-2">
              {['cash', 'card', 'upi'].map(method => (
                <button
                  key={method}
                  onClick={() => setPaymentMethod(method)}
                  className={`py-3 rounded-lg font-semibold transition-all ${
                    paymentMethod === method
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {method === 'cash' && '💵'}
                  {method === 'card' && '💳'}
                  {method === 'upi' && '📱'}
                  <div className="text-xs mt-1 capitalize">{method}</div>
                </button>
              ))}
            </div>
          </div>

          {paymentMethod === 'cash' && (
            <div>
              <label className="block text-gray-700 font-semibold mb-2">Amount Paid</label>
              <input
                type="number"
                step="0.01"
                value={amountPaid}
                onChange={(e) => setAmountPaid(e.target.value)}
                className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Enter amount"
                autoFocus
              />
              {amountPaid && (
                <p className={`mt-2 text-sm ${parseFloat(change) < 0 ? 'text-red-600' : 'text-green-600'}`}>
                  Change: ${change}
                </p>
              )}
            </div>
          )}

          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="flex justify-between mb-2">
              <span className="text-gray-600">Total Amount:</span>
              <span className="font-bold text-xl">${cart?.total || 0}</span>
            </div>
          </div>

          <button
            onClick={handleCheckout}
            disabled={processingPayment || (paymentMethod === 'cash' && parseFloat(change) < 0)}
            className="w-full bg-green-600 text-white py-3 rounded-lg hover:bg-green-700 disabled:bg-gray-400 font-bold"
          >
            {processingPayment ? 'Processing...' : 'Confirm Payment'}
          </button>
        </div>
      </Modal>

      {/* Discount Modal */}
      <Modal
        isOpen={showDiscount}
        onClose={() => setShowDiscount(false)}
        title="Apply Discount"
      >
        <div className="space-y-4">
          <div>
            <label className="block text-gray-700 font-semibold mb-2">Discount Type</label>
            <div className="grid grid-cols-2 gap-2">
              <button
                onClick={() => setDiscountType('percentage')}
                className={`py-2 rounded-lg font-semibold ${
                  discountType === 'percentage'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                Percentage %
              </button>
              <button
                onClick={() => setDiscountType('fixed')}
                className={`py-2 rounded-lg font-semibold ${
                  discountType === 'fixed'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-100 text-gray-700'
                }`}
              >
                Fixed Amount $
              </button>
            </div>
          </div>

          <div>
            <label className="block text-gray-700 font-semibold mb-2">
              {discountType === 'percentage' ? 'Percentage (%)' : 'Amount ($)'}
            </label>
            <input
              type="number"
              step="0.01"
              value={discountAmount}
              onChange={(e) => setDiscountAmount(e.target.value)}
              className="w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500"
              placeholder={discountType === 'percentage' ? 'e.g., 10' : 'e.g., 5.00'}
            />
          </div>

          <button
            onClick={handleApplyDiscount}
            className="w-full bg-yellow-500 text-white py-3 rounded-lg hover:bg-yellow-600 font-bold"
          >
            Apply Discount
          </button>
        </div>
      </Modal>
    </div>
  )
}

export default POS
