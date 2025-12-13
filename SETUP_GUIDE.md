# POS Simulator - Complete Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (Download from https://www.python.org/)
- **Node.js 16+** and npm (Download from https://nodejs.org/)
- **Git** (Optional, for version control)

## 🚀 Quick Start

### Step 1: Backend Setup

1. **Navigate to the project directory:**
   ```powershell
   cd C:\Users\naikm\OneDrive\Desktop\pos_simulator
   ```

2. **Create a Python virtual environment:**
   ```powershell
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
   
   If you get an execution policy error, run:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

4. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Initialize the database:**
   ```powershell
   cd backend
   python -m utils.db
   ```

6. **Start the backend server:**
   ```powershell
   python app.py
   ```

   The backend should now be running at `http://localhost:5000`

### Step 2: Frontend Setup (Optional)

1. **Open a new terminal and navigate to the frontend directory:**
   ```powershell
   cd C:\Users\naikm\OneDrive\Desktop\pos_simulator\frontend
   ```

2. **Install Node.js dependencies:**
   ```powershell
   npm install
   ```

3. **Start the frontend development server:**
   ```powershell
   npm run dev
   ```

   The frontend should now be running at `http://localhost:5173`

## 🧪 Testing the Backend

You can test the backend using curl, Postman, or the included test suite.

### Run Automated Tests

```powershell
cd backend
pytest tests/ -v
```

### Test with curl (in PowerShell)

1. **Login:**
   ```powershell
   $response = Invoke-WebRequest -Uri "http://localhost:5000/api/auth/login" -Method POST -ContentType "application/json" -Body '{"username":"cashier","password":"cashier123"}'
   $token = ($response.Content | ConvertFrom-Json).access_token
   ```

2. **Get Products:**
   ```powershell
   Invoke-WebRequest -Uri "http://localhost:5000/api/products" -Headers @{"Authorization"="Bearer $token"}
   ```

## 📚 API Testing with Examples

### 1. User Authentication

**Login:**
```http
POST http://localhost:5000/api/auth/login
Content-Type: application/json

{
  "username": "cashier",
  "password": "cashier123"
}
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 3,
    "username": "cashier",
    "role": "cashier",
    "full_name": "John Cashier"
  }
}
```

### 2. Product Operations

**Get all products:**
```http
GET http://localhost:5000/api/products
Authorization: Bearer {token}
```

**Search product by barcode:**
```http
GET http://localhost:5000/api/products/1234567890
Authorization: Bearer {token}
```

### 3. Cart Operations

**Add item to cart:**
```http
POST http://localhost:5000/api/cart/add
Authorization: Bearer {token}
Content-Type: application/json

{
  "barcode": "1234567890",
  "quantity": 2
}
```

**Get cart:**
```http
GET http://localhost:5000/api/cart
Authorization: Bearer {token}
```

### 4. Checkout

**Process payment:**
```http
POST http://localhost:5000/api/checkout/process
Authorization: Bearer {token}
Content-Type: application/json

{
  "payment_method": "cash",
  "amount_paid": 50.00
}
```

### 5. Reports

**Get sales report:**
```http
GET http://localhost:5000/api/reports/sales?start_date=2025-01-01&end_date=2025-12-31
Authorization: Bearer {token}
```

## 🔑 Default User Credentials

| Role | Username | Password | PIN |
|------|----------|----------|-----|
| Administrator | admin | admin123 | 1111 |
| Manager | manager | manager123 | 2222 |
| Cashier | cashier | cashier123 | 3333 |
| Cashier 2 | cashier2 | cashier123 | 4444 |

## 📦 Sample Products

The database is seeded with 10 sample products:

1. Laptop - Dell XPS 13 (Barcode: 1234567890) - $999.99
2. Wireless Mouse (Barcode: 2345678901) - $29.99
3. USB-C Cable 2m (Barcode: 3456789012) - $14.99
4. Mechanical Keyboard (Barcode: 4567890123) - $89.99
5. Office Chair (Barcode: 5678901234) - $249.99
6. Monitor 24" (Barcode: 6789012345) - $179.99
7. Desk Lamp LED (Barcode: 7890123456) - $39.99
8. Notebook A4 (Barcode: 8901234567) - $4.99
9. Pen Set (Barcode: 9012345678) - $7.99
10. Water Bottle 1L (Barcode: 0123456789) - $24.99

## 🗂️ Project Structure

```
pos_simulator/
│
├── backend/
│   ├── app.py              # Main Flask application
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── utils/              # Utilities (DB, PDF, payments)
│   └── tests/              # Unit and integration tests
│
├── frontend/               # React application
│   ├── src/
│   └── package.json
│
├── database/               # SQLite database files
├── receipts/               # Generated PDF receipts
├── requirements.txt        # Python dependencies
├── RTM.csv                # Requirements Traceability Matrix
└── README.md              # Main documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DEBUG=True
PORT=5000
```

### Using MySQL (Optional)

To use MySQL instead of SQLite:

1. Install MySQL connector:
   ```powershell
   pip install pymysql
   ```

2. Set the MySQL URI in `.env`:
   ```env
   MYSQL_URI=mysql+pymysql://username:password@localhost/pos_db
   ```

## 📊 Viewing Reports

Generated reports and receipts are saved in the `receipts/` directory as PDF files.

## 🐛 Troubleshooting

### Database Issues

If you encounter database errors, reset the database:

```powershell
cd backend
python -c "from utils.db import reset_database; from app import app; reset_database(app)"
```

### Port Already in Use

If port 5000 is already in use, change it in the `.env` file:

```env
PORT=5001
```

### Import Errors

Make sure you're in the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

## 📈 Performance Testing

The system is designed to complete checkout operations in ≤ 2 seconds for 90% of cases (POS-NF-001).

To test performance:

```powershell
cd backend
pytest tests/ -v --durations=10
```

## 🔐 Security Features

- Password hashing using Werkzeug's security utilities
- JWT-based authentication with 8-hour expiration
- Role-Based Access Control (RBAC)
- Failed login attempt tracking
- Account lockout after 5 failed attempts
- Audit logging for all operations
- Manager authorization for sensitive operations

## 📝 Development Workflow

1. **Make changes to the code**
2. **Run tests:**
   ```powershell
   pytest tests/ -v
   ```
3. **Check for errors:**
   ```powershell
   python app.py
   ```
4. **Test API endpoints** using curl or Postman

## 📖 Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **React Documentation:** https://react.dev/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **ReportLab Documentation:** https://www.reportlab.com/docs/reportlab-userguide.pdf

## 💡 Tips

1. **Keep the terminal open** while running the backend
2. **Use separate terminals** for backend and frontend
3. **Check the `receipts/` folder** for generated PDFs
4. **Review `RTM.csv`** for requirements traceability
5. **Refer to test files** for API usage examples

## 🎯 Next Steps

1. Test all API endpoints using the provided examples
2. Explore the generated PDF receipts in the `receipts/` folder
3. Review the audit logs in the database
4. Generate and view sales reports
5. Test manager override functionality for refunds
6. Implement the React frontend (optional)

## 📧 Support

For issues or questions, refer to:
- `README.md` - Main documentation
- `RTM.csv` - Requirements mapping
- Test files in `backend/tests/` - Usage examples

---

**Happy Testing! 🚀**
