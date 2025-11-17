# 🚀 POS Simulator - Frontend & Backend Setup Guide

## ✅ Prerequisites

- **Node.js 18+** (for frontend)
- **Python 3.11+** (for backend)
- **Git** (optional)

## 📦 Step 1: Backend Setup

### 1.1 Navigate to Backend Directory
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\backend
```

### 1.2 Activate Virtual Environment (if using)
```powershell
# If you have a venv:
..\venv\Scripts\Activate.ps1

# Or activate from Desktop:
cd C:\Users\naikm\OneDrive\Desktop
.\.venv\Scripts\Activate.ps1
```

### 1.3 Install Python Dependencies (if not already installed)
```powershell
pip install -r C:\Users\naikm\OneDrive\Desktop\pos_simulator\requirements.txt
```

### 1.4 Initialize Database (if not already done)
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\backend
python init_db.py
```

### 1.5 Start Backend Server
```powershell
python app.py
```

**Backend should now be running on:** `http://localhost:5000`

---

## 🎨 Step 2: Frontend Setup

### 2.1 Open New PowerShell Terminal

### 2.2 Navigate to Frontend Directory
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\frontend
```

### 2.3 Install Node Dependencies
```powershell
npm install
```

This will install:
- React 18
- React Router
- Axios
- TailwindCSS
- Vite
- And all other dependencies

### 2.4 Start Frontend Development Server
```powershell
npm run dev
```

**Frontend should now be running on:** `http://localhost:5173`

---

## 🌐 Step 3: Access the Application

1. **Open your browser** and go to: `http://localhost:5173`

2. **Login with default credentials:**

| Role | Username | Password | PIN |
|------|----------|----------|-----|
| **Admin** | admin | admin123 | 1111 |
| **Manager** | manager | manager123 | 2222 |
| **Cashier** | cashier | cashier123 | 3333 |

3. **Quick Login:** Click the colored buttons on the login page for instant access!

---

## 📋 Quick Start Commands (All-in-One)

### Terminal 1 (Backend):
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\backend
python app.py
```

### Terminal 2 (Frontend):
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\frontend
npm run dev
```

---

## 🧪 Testing the API

You can test the backend API directly:

```powershell
# Login
$login = Invoke-RestMethod -Uri http://localhost:5000/api/auth/login -Method POST -Body (@{username="admin"; password="admin123"} | ConvertTo-Json) -ContentType "application/json"
$token = $login.access_token

# Get Products
Invoke-RestMethod -Uri http://localhost:5000/api/products -Method GET -Headers @{Authorization="Bearer $token"}

# Get Cart
Invoke-RestMethod -Uri http://localhost:5000/api/cart -Method GET -Headers @{Authorization="Bearer $token"}
```

---

## 🎯 Application Features

### 1. **Point of Sale (POS)**
- Barcode scanning (type 8+ digit barcode to auto-add)
- Product search and filtering
- Real-time cart management
- Discount application
- Multiple payment methods (Cash, Card, UPI)
- Automatic change calculation

### 2. **Product Management** (Admin/Manager)
- Add/Edit/Delete products
- Track inventory levels
- Set reorder points
- Manage pricing and taxes

### 3. **Transaction History**
- View all completed sales
- Transaction details
- Payment method tracking

### 4. **Reports** (Manager/Admin)
- Sales reports with date ranges
- Inventory status reports
- Analytics and summaries

---

## 🔧 Troubleshooting

### Frontend not loading?
```powershell
# Clear node_modules and reinstall
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\frontend
Remove-Item -Recurse -Force node_modules
npm install
npm run dev
```

### Backend errors?
```powershell
# Reinitialize database
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\backend
python init_db.py
python app.py
```

### Port already in use?
```powershell
# Kill Python processes
Stop-Process -Name python -Force -ErrorAction SilentlyContinue

# Kill Node processes
Stop-Process -Name node -Force -ErrorAction SilentlyContinue
```

### CORS errors?
- Make sure backend is running on port 5000
- Check that `.env` file exists in backend directory
- Restart both frontend and backend

---

## 📁 Project Structure

```
pos_simulator/
├── backend/
│   ├── app.py                 # Flask application
│   ├── routes/                # API endpoints
│   ├── models/                # Database models
│   ├── utils/                 # Utilities
│   └── database/              # SQLite database
│
├── frontend/
│   ├── src/
│   │   ├── api/              # API client functions
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   ├── App.jsx           # Main app
│   │   └── main.jsx          # Entry point
│   ├── index.html
│   └── package.json
│
└── receipts/                  # Generated receipts
```

---

## 🎨 Frontend Technologies

- **React 18** - UI framework
- **Vite** - Build tool (fast HMR)
- **TailwindCSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client

## 🔐 Security Features

- JWT-based authentication
- Role-based access control (RBAC)
- Password encryption (bcrypt)
- Protected API routes
- Manager override for sensitive operations

---

## 📞 Support

If you encounter issues:

1. Check that both backend and frontend are running
2. Verify database is initialized
3. Check browser console for errors
4. Check terminal output for error messages
5. Ensure you're using the correct URLs:
   - Backend: `http://localhost:5000`
   - Frontend: `http://localhost:5173`

---

## 🚀 Ready to Go!

Your POS Simulator is now fully configured and ready to use. Enjoy! 🎉
