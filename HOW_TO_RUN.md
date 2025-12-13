# 🚀 How to Run POS Simulator

## Quickest Way (One Command)

### Option 1: Double-Click to Run
Simply **double-click** on `RUN.ps1` in the pos_simulator folder!

This will:
- ✅ Start the backend server (port 5000)
- ✅ Start the frontend server (port 5173)
- ✅ Open your browser automatically

---

### Option 2: Run from PowerShell
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator
.\RUN.ps1
```

---

## Manual Start (Step by Step)

### Step 1: Start Backend Server

Open a PowerShell terminal and run:
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\backend
python app.py
```

You should see:
```
✓ Database tables created successfully
 * Running on http://127.0.0.1:5000
```

**Keep this terminal open!**

---

### Step 2: Start Frontend Server

Open a **NEW** PowerShell terminal and run:
```powershell
cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\frontend
npm run dev
```

You should see:
```
VITE v5.4.20 ready in 899 ms
➜  Local:   http://localhost:5173/
```

**Keep this terminal open too!**

---

### Step 3: Open Browser

Go to: **http://localhost:5173**

---

## 🔐 Login Credentials

Once the login page appears, use these credentials:

| Role | Username | Password |
|------|----------|----------|
| 👨‍💼 Admin | `admin` | `admin123` |
| 👔 Manager | `manager` | `manager123` |
| 👨‍💻 Cashier | `cashier` | `cashier123` |

---

## 🛑 How to Stop

### Stop Servers:
1. Go to each PowerShell terminal
2. Press **Ctrl + C**
3. Confirm with **Y** if asked

### Using the Script:
Just close the terminal windows that opened.

---

## 🔧 Troubleshooting

### Port Already in Use?

**Backend (port 5000) in use:**
```powershell
# Find and kill the process
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process -Force
```

**Frontend (port 5173) in use:**
```powershell
# Find and kill the process
Get-Process -Id (Get-NetTCPConnection -LocalPort 5173).OwningProcess | Stop-Process -Force
```

---

### Backend Not Starting?

Make sure Python is installed:
```powershell
python --version
```

Should show: Python 3.11 or higher

---

### Frontend Not Starting?

Make sure Node.js is installed:
```powershell
node --version
```

Should show: v18 or higher

If packages aren't installed:
```powershell
cd frontend
npm install
```

---

## 📱 Access URLs

Once running, access these URLs:

- **Frontend (Main App):** http://localhost:5173
- **Backend API:** http://localhost:5000/api
- **API Health Check:** http://localhost:5000/api/products (requires login)

---

## ✅ Quick Test

After logging in:
1. Click **"POS"** from the dashboard
2. Scan or select a product
3. Add to cart
4. Click **"Checkout"**
5. Complete payment
6. Success! 🎉

---

## 📊 Test Features

### As Admin/Manager:
- ✅ View/Add/Edit/Delete Products
- ✅ Process Sales
- ✅ View Reports
- ✅ View Transactions

### As Cashier:
- ✅ Process Sales (POS)
- ✅ View Products (read-only)
- ❌ Cannot modify products

---

## 💡 Pro Tips

1. **Use Quick Login Buttons** - Click role badges on login page
2. **Barcode Scanning** - Type 8+ digits in POS to auto-search
3. **Keyboard Shortcuts** - Tab through forms quickly
4. **Multiple Tabs** - Open different roles in different browser tabs

---

## 📞 Need Help?

Check these files:
- `SYSTEM_HEALTH_CHECK.md` - System status
- `TEST_REPORT.md` - Detailed test results
- `COMPLETE_GUIDE.md` - Full documentation
- `FRONTEND_SETUP.md` - Frontend setup guide

---

**Ready to go! Just run `RUN.ps1` and start using your POS system! 🚀**
