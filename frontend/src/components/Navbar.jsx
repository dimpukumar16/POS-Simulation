import { useNavigate } from 'react-router-dom'

function Navbar({ user, onLogout }) {
  const navigate = useNavigate()

  return (
    <nav className="bg-white shadow-md p-4 sticky top-0 z-50">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center gap-6">
          <h1 
            onClick={() => navigate('/dashboard')}
            className="text-2xl font-bold text-gray-800 cursor-pointer hover:text-blue-600 transition-colors"
          >
            🏪 POS Simulator
          </h1>
          <div className="hidden md:flex gap-4">
            <button
              onClick={() => navigate('/pos')}
              className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition-colors"
            >
              Point of Sale
            </button>
            <button
              onClick={() => navigate('/products')}
              className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition-colors"
            >
              Products
            </button>
            <button
              onClick={() => navigate('/transactions')}
              className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition-colors"
            >
              Transactions
            </button>
            {(user?.role === 'manager' || user?.role === 'administrator') && (
              <button
                onClick={() => navigate('/refunds')}
                className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition-colors"
              >
                Refunds
              </button>
            )}
            <button
              onClick={() => navigate('/reports')}
              className="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md transition-colors"
            >
              Reports
            </button>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right">
            <p className="text-sm text-gray-600">
              <strong>{user?.username}</strong>
            </p>
            <p className="text-xs text-gray-500 capitalize">{user?.role}</p>
          </div>
          <button
            onClick={onLogout}
            className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
