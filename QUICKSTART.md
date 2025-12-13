# POS Simulator - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Option 1: Docker (Easiest - Recommended)

1. **Install Docker Desktop** (if not already installed)
   - Windows/Mac: Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Linux: `sudo apt install docker.io docker-compose`

2. **Clone and Start**
   ```bash
   git clone <repository-url>
   cd pos_simulator
   docker-compose up -d
   ```

3. **Access the Application**
   - Open browser: http://localhost:5173
   - Login: `manager` / `manager123`

That's it! 🎉

---

### Option 2: Local Development

**Prerequisites:**
- Python 3.11+
- Node.js 20+
- Git

**Steps:**

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd pos_simulator
   ```

2. **Install Backend**
   ```bash
   pip install -r requirements.txt
   cd backend
   python init_db.py
   python app.py
   ```

3. **Install Frontend** (in new terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access Application**
   - Open browser: http://localhost:5173
   - Login: `manager` / `manager123`

---

## 👤 Default Users

| Role | Username | Password | PIN | Permissions |
|------|----------|----------|-----|-------------|
| Administrator | `admin` | `admin123` | `1111` | Full access |
| Manager | `manager` | `manager123` | `2222` | Refunds, reports, sales |
| Cashier | `cashier` | `cashier123` | `3333` | Sales only |

⚠️ **Change these credentials in production!**

---

## 🎯 Quick Feature Tour

### 1. Point of Sale (All Users)
- Go to **Point of Sale** tab
- Scan or enter barcode: `1234567890`
- Click product to add to cart
- Adjust quantities
- Click **Checkout**
- Select payment method
- Complete purchase

### 2. Refunds (Manager/Admin Only)
- Go to **Refunds** tab
- Enter transaction number (e.g., `TXN-20251027123456`)
- Click **Search**
- Enter refund reason
- Click **Process Refund**
- Inventory automatically restocked

### 3. Reports (All Users)
- Go to **Reports** tab
- Select date range
- Click **Generate Report**
- Export as CSV or PDF

### 4. Products (All Users)
- Go to **Products** tab
- Add/edit/delete products
- Manage inventory levels
- Set tax rates and pricing

---

## 🔧 Common Tasks

### Add a New Product
1. Go to **Products** page
2. Click **Add Product**
3. Fill in details (barcode, name, price, stock)
4. Click **Save**

### Process a Sale
1. Go to **POS** page
2. Add items to cart
3. Apply discount (optional)
4. Click **Checkout**
5. Select payment method
6. Print/download receipt

### Process a Refund
1. Go to **Refunds** page (manager only)
2. Search transaction by number
3. Enter refund reason
4. Confirm refund
5. Stock automatically updated

### Generate Sales Report
1. Go to **Reports** page
2. Select date range
3. Filter by cashier/category (optional)
4. Click **Generate**
5. Export as CSV/PDF

---

## 🆘 Troubleshooting

### Backend not starting?
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Try different port
set FLASK_RUN_PORT=5001
python app.py
```

### Frontend not starting?
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Database errors?
```bash
# Reset database
rm database/pos.db
python backend/init_db.py
```

### Docker issues?
```bash
# Reset everything
docker-compose down -v
docker-compose up -d --build
```

---

## 📚 Learn More

- **[PROJECT_SPEC.md](PROJECT_SPEC.md)** - Full specification with user stories
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - What was implemented
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker deployment guide
- **[DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)** - Production deployment steps
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - REST API reference

---

## 🎨 Screenshots

### Point of Sale
![POS Screen](screenshots/pos.png)

### Refunds Management
![Refunds Screen](screenshots/refunds.png)

### Sales Reports
![Reports Screen](screenshots/reports.png)

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📞 Support

- **Issues**: [GitHub Issues](repository-url/issues)
- **Documentation**: See `/docs` folder
- **Email**: support@example.com

---

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

---

## ⭐ Features at a Glance

✅ Full RBAC (Role-Based Access Control)  
✅ JWT Authentication with Refresh Tokens  
✅ Real-time Inventory Management  
✅ Refunds with Manager Override  
✅ PDF Receipt Generation  
✅ Advanced Reporting (CSV/PDF Export)  
✅ Audit Logging  
✅ Docker Support  
✅ CI/CD Pipeline (GitHub Actions)  
✅ PostgreSQL & SQLite Support  
✅ Responsive UI (TailwindCSS)  
✅ RESTful API  
✅ Configurable Settings  

---

**Built with ❤️ for modern retail operations**
