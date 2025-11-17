import { useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'

function Dashboard({ user, onLogout }) {
  const navigate = useNavigate()

  const cards = [
    {
      icon: '🛒',
      title: 'Point of Sale',
      description: 'Process sales and manage transactions',
      path: '/pos',
      color: 'bg-blue-500',
      hoverColor: 'hover:bg-blue-600',
    },
    {
      icon: '📦',
      title: 'Products',
      description: 'Manage inventory and product catalog',
      path: '/products',
      color: 'bg-green-500',
      hoverColor: 'hover:bg-green-600',
      adminOnly: true,
    },
    {
      icon: '💰',
      title: 'Transactions',
      description: 'View transaction history and details',
      path: '/transactions',
      color: 'bg-purple-500',
      hoverColor: 'hover:bg-purple-600',
    },
    {
      icon: '📊',
      title: 'Reports',
      description: 'Sales and inventory analytics',
      path: '/reports',
      color: 'bg-orange-500',
      hoverColor: 'hover:bg-orange-600',
      managerOnly: true,
    },
  ]

  const isAuthorized = (card) => {
    if (card.adminOnly && user?.role !== 'administrator' && user?.role !== 'manager') {
      return false
    }
    if (card.managerOnly && user?.role !== 'administrator' && user?.role !== 'manager') {
      return false
    }
    return true
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar user={user} onLogout={onLogout} />

      <div className="container mx-auto p-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-gray-600">
            Role: <span className="font-semibold capitalize">{user?.role}</span>
          </p>
        </div>

        {/* Quick Actions Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {cards.map((card, index) => {
            const authorized = isAuthorized(card)
            return (
              <div
                key={index}
                onClick={() => authorized && navigate(card.path)}
                className={`
                  ${authorized ? 'cursor-pointer' : 'opacity-50 cursor-not-allowed'}
                  bg-white rounded-xl shadow-md hover:shadow-xl transition-all transform hover:-translate-y-1 overflow-hidden
                `}
              >
                <div className={`${card.color} p-4 text-white text-center`}>
                  <div className="text-5xl mb-2">{card.icon}</div>
                </div>
                <div className="p-6">
                  <h2 className="text-xl font-bold mb-2 text-gray-800">{card.title}</h2>
                  <p className="text-gray-600 text-sm">{card.description}</p>
                  {!authorized && (
                    <p className="mt-3 text-xs text-red-500">
                      🔒 Restricted Access
                    </p>
                  )}
                </div>
              </div>
            )
          })}
        </div>

        {/* Quick Stats */}
        <div className="bg-white rounded-xl shadow-md p-6">
          <h2 className="text-2xl font-bold mb-6 text-gray-800">Quick Stats</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-blue-50 rounded-lg">
              <p className="text-4xl font-bold text-blue-600 mb-2">$0.00</p>
              <p className="text-gray-600">Today's Sales</p>
            </div>
            <div className="text-center p-6 bg-green-50 rounded-lg">
              <p className="text-4xl font-bold text-green-600 mb-2">0</p>
              <p className="text-gray-600">Transactions</p>
            </div>
            <div className="text-center p-6 bg-orange-50 rounded-lg">
              <p className="text-4xl font-bold text-orange-600 mb-2">0</p>
              <p className="text-gray-600">Products in Stock</p>
            </div>
          </div>
        </div>

        {/* System Info */}
        <div className="mt-8 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl shadow-md p-6">
          <h3 className="text-xl font-bold mb-2">🎯 System Status</h3>
          <p className="text-blue-100">
            All systems operational. Backend connected to <code>http://localhost:5000</code>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
