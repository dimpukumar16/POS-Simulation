# POS Simulator

A comprehensive Point of Sale (POS) Simulator built with modern technologies and production-ready features. Fully implements the requirements specified in PROJECT_SPEC.md with 14 user stories across 3 epics.

## 🚀 Quick Start

**Option 1: Docker (Recommended)**
```bash
docker-compose up -d
# Access at http://localhost:5173
```
See [DOCKER_GUIDE.md](DOCKER_GUIDE.md) for details.

**Option 2: Local Development**
```powershell
.\start-full.ps1  # Windows PowerShell
```

## 🔹 Features

### Core Functionality (Sprint 1)
- ✅ **Product Management**: Barcode/SKU search, autocomplete, stock validation
- ✅ **Cart Management**: Real-time updates, quantity controls, session persistence
- ✅ **Tax & Discounts**: Item-level and order-level discounts with configurable tax rates
- ✅ **Stock Validation**: Pre-checkout inventory verification
- ✅ **Mock Payments**: Cash, Card, and UPI payment simulation with rollback
- ✅ **Receipt Generation**: Automatic PDF receipt generation with transaction details

### Advanced Features (Sprint 2)
- ✅ **Refunds & Voids**: Manager-authorized refund operations with inventory restock
- ✅ **Manager Override**: PIN-based authorization for restricted actions
- ✅ **Inventory Management**: Automatic stock updates with transactional integrity
- ✅ **Enhanced Reporting**: Sales reports with CSV/PDF export, advanced filters
- ✅ **RBAC**: Role-based access control (Cashier, Manager, Administrator)
- ✅ **Secure Authentication**: JWT + refresh tokens, bcrypt encryption, account lockout
- ✅ **Performance**: Fast checkout (<2s), data consistency guarantees
- ✅ **UI/UX**: Tooltips, loading states, responsive design

### Additional Features
- ✅ **Audit Logging**: Complete audit trail of all system operations
- ✅ **Settings Management**: Configurable system settings (admin only)
- ✅ **Docker Support**: Full containerization with PostgreSQL
- ✅ **CI/CD Pipeline**: GitHub Actions for automated testing and deployment

## � Documentation

- **[PROJECT_SPEC.md](PROJECT_SPEC.md)** - Complete implementation specification (epics, stories, DB schema, APIs)
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker deployment and operations guide
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - REST API reference
- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - Local development setup
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions

## �🔹 Tech Stack

- **Backend**: Python 3.11 + Flask + SQLAlchemy
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: React 18 + Vite + TailwindCSS
- **Authentication**: JWT + Refresh Tokens
- **PDF Generation**: ReportLab
- **Testing**: Pytest (backend), Jest (frontend)
- **DevOps**: Docker + Docker Compose, GitHub Actions

## 🔹 Installation

### Backend Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
cd backend
python -m utils.db
```

3. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will run on `http://localhost:5173`

### Quick Start (Both Servers)

Run both backend and frontend with a single command:

```powershell
# From the project root
.\start-full.ps1
```

Or manually in separate terminals:

**Terminal 1 (Backend):**
```powershell
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```powershell
cd frontend
npm run dev
```

Then open your browser to `http://localhost:5173`

## 🔹 Default Users

The system comes with pre-configured test users:

| Username | Password | Role | PIN |
|----------|----------|------|-----|
| admin | admin123 | Administrator | 1111 |
| manager | manager123 | Manager | 2222 |
| cashier | cashier123 | Cashier | 3333 |

## 🔹 Project Structure

```
pos_simulator/
│
├── backend/
│   ├── app.py                  # Main Flask application
│   ├── routes/                 # API route handlers
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── cart.py            # Cart management
│   │   ├── products.py        # Product CRUD operations
│   │   ├── checkout.py        # Checkout and payment
│   │   └── reports.py         # Reports and analytics
│   ├── models/                 # Database models
│   │   ├── user.py            # User model
│   │   ├── product.py         # Product model
│   │   ├── transaction.py     # Transaction model
│   │   └── inventory.py       # Inventory model
│   ├── utils/                  # Utility modules
│   │   ├── db.py              # Database initialization
│   │   ├── pdf_generator.py  # PDF generation
│   │   ├── payment_simulator.py # Mock payment API
│   │   └── logger.py          # Audit logging
│   └── tests/                  # Test suite
│
├── frontend/                   # React application
├── database/                   # SQLite database files
├── receipts/                   # Generated PDF receipts
└── README.md
```

## 🔹 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/verify-pin` - Verify manager PIN

### Products
- `GET /api/products` - List all products
- `GET /api/products/<barcode>` - Get product by barcode
- `POST /api/products` - Create new product (Admin only)
- `PUT /api/products/<id>` - Update product (Admin only)
- `DELETE /api/products/<id>` - Delete product (Admin only)

### Cart
- `POST /api/cart/add` - Add item to cart
- `PUT /api/cart/update` - Update cart item quantity
- `DELETE /api/cart/remove/<item_id>` - Remove item from cart
- `GET /api/cart` - Get current cart
- `DELETE /api/cart/clear` - Clear cart

### Checkout
- `POST /api/checkout/process` - Process payment
- `POST /api/checkout/refund` - Process refund (Manager only)
- `POST /api/checkout/void` - Void transaction (Manager only)

### Reports
- `GET /api/reports/sales` - Generate sales report
- `GET /api/reports/inventory` - Generate inventory report
- `GET /api/reports/history` - Get sales history
- `GET /api/reports/export` - Export report as PDF/CSV

## 🔹 Testing

Run the test suite:

```bash
cd backend
pytest tests/ -v --cov
```

## 🔹 Performance Requirements

- Checkout operations complete in ≤ 2 seconds (90% of cases)
- 99% availability in lab usage conditions
- Absolute data consistency between sales and inventory

## 🔹 Security Features

- Password encryption using bcrypt
- JWT-based authentication
- Role-Based Access Control (RBAC)
- Audit logging for all operations
- Manager override for sensitive operations

## 🔹 Requirements Traceability

See `RTM.csv` for complete mapping of requirements to code modules and test cases.

## 🔹 License

Educational project for Software Engineering course.

## 🔹 Authors

- Team: 802, 803, 179, 171
