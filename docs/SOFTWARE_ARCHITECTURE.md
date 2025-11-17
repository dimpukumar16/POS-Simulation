# Software Architecture Document (SAD)
## POS Simulator Application

**Version:** 1.0  
**Date:** November 16, 2025  
**Project:** Point of Sale (POS) Simulator  
**Authors:** Narayana S, Mithun Naik, Dimpu Kumar, Darshan H V  

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Architectural Goals and Constraints](#2-architectural-goals-and-constraints)
3. [System Overview](#3-system-overview)
4. [Architectural Patterns](#4-architectural-patterns)
5. [Component Architecture](#5-component-architecture)
6. [Data Architecture](#6-data-architecture)
7. [Deployment Architecture](#7-deployment-architecture)
8. [Security Architecture](#8-security-architecture)
9. [Quality Attributes](#9-quality-attributes)

---

## 1. Introduction

### 1.1 Purpose
This document describes the software architecture of the POS Simulator application, providing a comprehensive view of the system's structure, components, and design decisions.

### 1.2 Scope
Covers all architectural aspects including system decomposition, component interaction, data flow, deployment model, and quality attribute strategies.

### 1.3 Target Audience
- Software Developers
- System Architects
- QA Engineers
- Project Evaluators
- Maintenance Teams

---

## 2. Architectural Goals and Constraints

### 2.1 Business Goals
- Educational tool for learning POS systems
- Demonstrate software engineering practices
- Production-quality codebase
- Easy deployment and maintenance

### 2.2 Technical Goals
- **Maintainability:** Clear separation of concerns
- **Testability:** High test coverage possible
- **Scalability:** Handle multiple concurrent users
- **Security:** Protect user data and transactions
- **Performance:** Fast response times (<2s checkout)

### 2.3 Constraints
- **Technology Stack:** Python/Flask backend, React frontend
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Deployment:** Docker containerization
- **No External Dependencies:** Offline-first design
- **Mock Payments:** No real payment integration

---

## 3. System Overview

### 3.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT TIER                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Web Browser (Chrome, Firefox, Edge)                     │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  React 18 Single Page Application (SPA)            │  │   │
│  │  │  - React Router (Navigation)                       │  │   │
│  │  │  - Axios (HTTP Client)                             │  │   │
│  │  │  - TailwindCSS (Styling)                           │  │   │
│  │  │  - State Management (React Hooks)                  │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTPS/HTTP
                           │ REST API (JSON)
┌──────────────────────────▼──────────────────────────────────────┐
│                    APPLICATION TIER                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Flask 3.0 Web Application (Python 3.11)                 │   │
│  │  ┌────────────────────────────────────────────────────┐  │   │
│  │  │  API Layer (RESTful Endpoints)                     │  │   │
│  │  │  - Auth Routes    - Cart Routes                    │  │   │
│  │  │  - Checkout Routes - Product Routes                │  │   │
│  │  │  - Refund Routes  - Report Routes                  │  │   │
│  │  │  - Settings Routes                                 │  │   │
│  │  ├────────────────────────────────────────────────────┤  │   │
│  │  │  Business Logic Layer                              │  │   │
│  │  │  - Payment Processing   - Tax Calculation          │  │   │
│  │  │  - Inventory Management - PDF Generation           │  │   │
│  │  │  - Authorization Logic  - Audit Logging            │  │   │
│  │  ├────────────────────────────────────────────────────┤  │   │
│  │  │  Data Access Layer (ORM)                           │  │   │
│  │  │  - SQLAlchemy 2.0 Models                           │  │   │
│  │  │  - Database Session Management                     │  │   │
│  │  │  - Query Optimization                              │  │   │
│  │  └────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ SQL
┌──────────────────────────▼──────────────────────────────────────┐
│                      DATA TIER                                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Database Server                                         │   │
│  │  - SQLite 3.x (Development)                             │   │
│  │  - PostgreSQL 15 (Production)                           │   │
│  │                                                          │   │
│  │  Tables: users, products, transactions,                 │   │
│  │          transaction_items, refunds, refresh_tokens,    │   │
│  │          settings, audit_logs, inventory_logs           │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    FILE SYSTEM                                   │
│  - PDF Receipts (./receipts/)                                    │
│  - Application Logs (./logs/)                                    │
│  - Database File (./database/pos.db) - Dev only                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 System Context Diagram

```
┌──────────────┐         ┌──────────────────┐         ┌─────────────┐
│              │         │                  │         │             │
│   Cashier    │────────▶│  POS Simulator   │◀────────│   Manager   │
│              │         │                  │         │             │
└──────────────┘         └────────┬─────────┘         └─────────────┘
                                  │
                                  │
                         ┌────────▼─────────┐
                         │                  │
                         │  Administrator   │
                         │                  │
                         └──────────────────┘

External Systems (Mock):
┌──────────────────┐
│  Payment Gateway │  ────▶  Mock Implementation
└──────────────────┘

┌──────────────────┐
│  Receipt Printer │  ────▶  PDF Generation
└──────────────────┘

┌──────────────────┐
│ Barcode Scanner  │  ────▶  Text Input Field
└──────────────────┘
```

---

## 4. Architectural Patterns

### 4.1 Overall Architecture Pattern: **Three-Tier Architecture**

**Presentation Tier (Frontend):**
- React SPA for user interface
- Client-side rendering
- State management with React hooks
- Responsive design

**Application Tier (Backend):**
- Flask RESTful API
- Business logic processing
- Authentication and authorization
- Data validation

**Data Tier:**
- Relational database (SQLite/PostgreSQL)
- Persistent data storage
- Transaction management

**Benefits:**
- Clear separation of concerns
- Independent scaling of tiers
- Technology flexibility
- Easier maintenance and testing

---

### 4.2 Backend Pattern: **Layered Architecture**

```
┌────────────────────────────────────────┐
│         API/Presentation Layer         │  ← Flask Routes (Blueprints)
│  - Request handling                    │
│  - Response formatting                 │
│  - Input validation                    │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│         Business Logic Layer           │  ← Services/Utilities
│  - Domain logic                        │
│  - Business rules                      │
│  - Calculations                        │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│         Data Access Layer              │  ← SQLAlchemy Models
│  - ORM operations                      │
│  - Database queries                    │
│  - Transaction management              │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│            Database                    │  ← SQLite/PostgreSQL
└────────────────────────────────────────┘
```

**Benefits:**
- Clear responsibility assignment
- Testability at each layer
- Reusable business logic
- Database independence

---

### 4.3 Frontend Pattern: **Component-Based Architecture**

```
App (Root Component)
│
├── Router
│   ├── Public Routes
│   │   └── Login
│   │
│   └── Protected Routes (Authenticated)
│       ├── Dashboard
│       ├── POS
│       │   ├── ProductSearch
│       │   ├── CartView
│       │   │   └── CartItem
│       │   ├── SummaryBox
│       │   └── PaymentModal
│       ├── Refunds (Manager+)
│       │   ├── TransactionSearch
│       │   ├── RefundForm
│       │   └── ManagerOverride
│       ├── Reports (Manager+)
│       ├── Products (Admin)
│       └── Transactions
│
└── Shared Components
    ├── Navbar
    ├── Loading
    ├── Modal
    └── ErrorBoundary
```

---

### 4.4 API Design Pattern: **RESTful Architecture**

**Principles:**
- Resource-based URLs
- HTTP verbs for operations (GET, POST, PUT, DELETE)
- Stateless communication
- JSON data format
- Standard HTTP status codes

**Example Routes:**
```
GET    /api/products          - List products
GET    /api/products/:id      - Get product
POST   /api/products          - Create product (admin)
PUT    /api/products/:id      - Update product (admin)
DELETE /api/products/:id      - Delete product (admin)

POST   /api/cart/add          - Add to cart
PUT    /api/cart/update       - Update cart item
DELETE /api/cart/remove/:id   - Remove from cart

POST   /api/checkout/process  - Process checkout
POST   /api/refunds           - Create refund
```

---

### 4.5 Security Pattern: **JWT Token-Based Authentication**

```
1. Login
   Client ──POST /api/auth/login──▶ Server
          ◀─── JWT Token ──────────

2. Authenticated Request
   Client ──GET /api/protected──▶ Server
          Authorization: Bearer {token}
          
3. Token Validation
   Server validates:
   - Token signature
   - Token expiration
   - User role/permissions
```

---

## 5. Component Architecture

### 5.1 Backend Components

#### 5.1.1 API Layer (Routes/Blueprints)

**Purpose:** Handle HTTP requests and responses

**Components:**
1. **auth_bp** (`routes/auth.py`)
   - Login, logout, token refresh
   - PIN verification
   - User authentication

2. **cart_bp** (`routes/cart.py`)
   - Add/update/remove cart items
   - Cart calculations
   - Discount application

3. **checkout_bp** (`routes/checkout.py`)
   - Process checkout
   - Payment processing
   - Receipt generation

4. **product_bp** (`routes/products.py`)
   - Product CRUD operations
   - Stock management
   - Product search

5. **refund_bp** (`routes/refunds.py`)
   - Refund creation
   - Refund cancellation
   - Refund history

6. **reports_bp** (`routes/reports.py`)
   - Sales reports
   - Inventory reports
   - Export functionality

7. **settings_bp** (`routes/settings.py`)
   - System configuration
   - Setting CRUD operations

**Responsibilities:**
- Request validation
- Authentication/authorization checks
- Response formatting
- Error handling

---

#### 5.1.2 Business Logic Layer

**Purpose:** Implement business rules and domain logic

**Components:**

1. **Payment Simulator** (`utils/payment_simulator.py`)
   - Mock payment processing
   - Success/failure simulation
   - Payment method handling

2. **PDF Generator** (`utils/pdf_generator.py`)
   - Receipt template rendering
   - PDF creation with ReportLab
   - Receipt storage

3. **Logger** (`utils/logger.py`)
   - Application logging
   - Audit trail creation
   - Error logging

4. **DB Utils** (`utils/db.py`)
   - Database initialization
   - Data seeding
   - Helper functions

**Responsibilities:**
- Business rule enforcement
- Complex calculations
- External service integration
- Utility functions

---

#### 5.1.3 Data Access Layer (Models)

**Purpose:** Database interaction and data persistence

**Models:**

1. **User** (`models/user.py`)
   - Attributes: username, password_hash, role, PIN
   - Methods: set_password(), check_password()

2. **Product** (`models/product.py`)
   - Attributes: SKU, name, price_cents, stock_qty, tax_rate
   - Methods: to_dict(), check_stock()

3. **Transaction** (`models/transaction.py`)
   - Attributes: transaction_number, cashier_id, total_amount_cents, status
   - Relationships: transaction_items, cashier

4. **TransactionItem** (`models/transaction.py`)
   - Attributes: product_id, quantity, unit_price_cents, discount_cents
   - Relationships: transaction, product

5. **Refund** (`models/refund.py`)
   - Attributes: refund_number, transaction_id, amount_cents, reason
   - Methods: process_refund(), restock_inventory()

6. **RefreshToken** (`models/refresh_token.py`)
   - Attributes: token, user_id, expires_at, is_revoked
   - Methods: generate_token(), is_valid()

7. **Setting** (`models/settings.py`)
   - Attributes: key, value, value_type
   - Methods: get_value(), set_value()

**Responsibilities:**
- Database schema definition
- CRUD operations
- Relationships management
- Data validation

---

### 5.2 Frontend Components

#### 5.2.1 Page Components

1. **Login.jsx**
   - User authentication form
   - Role-based redirection

2. **Dashboard.jsx**
   - Overview widgets
   - Quick access links

3. **POS.jsx**
   - Product search and selection
   - Cart management
   - Checkout processing

4. **Refunds.jsx**
   - Transaction search
   - Refund processing
   - Refund history

5. **Reports.jsx**
   - Report generation
   - Data visualization
   - Export functionality

6. **Products.jsx**
   - Product management
   - Stock adjustments

7. **Transactions.jsx**
   - Transaction history
   - Transaction details

---

#### 5.2.2 Shared Components

1. **Navbar.jsx**
   - Navigation menu
   - Role-based menu items
   - User profile

2. **ManagerOverride.jsx**
   - PIN verification modal
   - Authorization workflow

3. **Loading.jsx**
   - Loading indicators

4. **Modal.jsx**
   - Reusable modal component

---

#### 5.2.3 API Integration Layer

**Purpose:** Frontend-backend communication

**Modules:**

1. **config.js**
   - API base URL
   - Axios instance configuration
   - Request/response interceptors

2. **auth.js**
   - Login, logout
   - Token refresh
   - PIN verification

3. **cart.js**
   - Cart operations
   - Discount application

4. **checkout.js**
   - Checkout processing
   - Transaction retrieval

5. **products.js**
   - Product CRUD
   - Product search

6. **refunds.js**
   - Refund operations

7. **reports.js**
   - Report generation
   - Data export

---

## 6. Data Architecture

### 6.1 Database Schema

```sql
-- Core Tables

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    display_name VARCHAR(100),
    role VARCHAR(20) NOT NULL, -- cashier, manager, administrator
    pin VARCHAR(255),
    failed_login_attempts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price_cents INTEGER NOT NULL,
    tax_rate DECIMAL(5,4) DEFAULT 0.0000,
    stock_qty INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    transaction_number VARCHAR(50) UNIQUE NOT NULL,
    cashier_id INTEGER NOT NULL,
    total_amount_cents INTEGER NOT NULL,
    subtotal_cents INTEGER NOT NULL,
    discount_cents INTEGER DEFAULT 0,
    tax_cents INTEGER DEFAULT 0,
    payment_method VARCHAR(20),
    payment_status VARCHAR(20),
    status VARCHAR(20) DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cashier_id) REFERENCES users(id)
);

CREATE TABLE transaction_items (
    id INTEGER PRIMARY KEY,
    transaction_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    discount_cents INTEGER DEFAULT 0,
    tax_cents INTEGER DEFAULT 0,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE refunds (
    id INTEGER PRIMARY KEY,
    refund_number VARCHAR(50) UNIQUE NOT NULL,
    transaction_id INTEGER NOT NULL,
    amount_cents INTEGER NOT NULL,
    refunded_by INTEGER NOT NULL,
    reason TEXT,
    refund_method VARCHAR(20),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id),
    FOREIGN KEY (refunded_by) REFERENCES users(id)
);

-- Security Tables

CREATE TABLE refresh_tokens (
    id INTEGER PRIMARY KEY,
    token VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Configuration Tables

CREATE TABLE settings (
    id INTEGER PRIMARY KEY,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    value_type VARCHAR(20),
    category VARCHAR(50),
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE,
    updated_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Audit Tables

CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE inventory_logs (
    id INTEGER PRIMARY KEY,
    product_id INTEGER NOT NULL,
    quantity_change INTEGER NOT NULL,
    reason VARCHAR(100),
    reference_type VARCHAR(50),
    reference_id INTEGER,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

### 6.2 Entity Relationship Diagram

```
┌──────────────┐
│    users     │
│──────────────│
│ PK id        │
│    username  │
│    role      │
│    pin       │
└──────┬───────┘
       │
       │ 1:N (cashier)
       │
┌──────▼───────────┐     1:N     ┌──────────────────┐
│  transactions    │─────────────▶│ transaction_items│
│──────────────────│              │──────────────────│
│ PK id            │              │ PK id            │
│ FK cashier_id    │              │ FK transaction_id│
│    transaction_# │              │ FK product_id    │
│    payment_method│              │    quantity      │
│    status        │              │    unit_price    │
└──────┬───────────┘              └──────────────────┘
       │                                    │
       │ 1:N                                │
       │                                    │ N:1
┌──────▼───────┐                  ┌────────▼──────┐
│   refunds    │                  │   products    │
│──────────────│                  │───────────────│
│ PK id        │                  │ PK id         │
│ FK trans_id  │                  │    sku        │
│ FK refunded_by│                 │    name       │
│    amount    │                  │    price_cents│
│    reason    │                  │    stock_qty  │
└──────────────┘                  └───────────────┘

┌────────────────┐
│ refresh_tokens │
│────────────────│
│ PK id          │
│ FK user_id     │
│    token       │
│    expires_at  │
└────────────────┘

┌──────────────┐
│  settings    │
│──────────────│
│ PK id        │
│    key       │
│    value     │
│    value_type│
└──────────────┘

┌──────────────┐
│ audit_logs   │
│──────────────│
│ PK id        │
│ FK user_id   │
│    action    │
│    details   │
└──────────────┘

┌────────────────┐
│ inventory_logs │
│────────────────│
│ PK id          │
│ FK product_id  │
│    qty_change  │
│    reason      │
└────────────────┘
```

### 6.3 Data Flow

**Checkout Process Data Flow:**
```
1. User adds product to cart
   ↓
2. Frontend sends POST /api/cart/add
   ↓
3. Backend validates product & stock
   ↓
4. Cart stored in session
   ↓
5. Frontend displays cart
   ↓
6. User initiates checkout
   ↓
7. Frontend sends POST /api/checkout/process
   ↓
8. Backend starts database transaction
   ↓
9. Validate stock availability
   ↓
10. Create Transaction record
    ↓
11. Create TransactionItem records
    ↓
12. Update product stock (decrement)
    ↓
13. Create InventoryLog entries
    ↓
14. Process payment (mock)
    ↓
15. Generate PDF receipt
    ↓
16. Commit transaction
    ↓
17. Return success + receipt URL
    ↓
18. Frontend displays confirmation
```

---

## 7. Deployment Architecture

### 7.1 Development Environment

```
Developer Workstation
├── Backend (Port 5000)
│   ├── Python 3.11
│   ├── venv (Virtual Environment)
│   ├── Flask Development Server
│   └── SQLite Database
│
├── Frontend (Port 5173)
│   ├── Node.js 20
│   ├── Vite Dev Server
│   └── Hot Module Replacement
│
└── Tools
    ├── VS Code / IDE
    ├── Git
    └── Postman
```

### 7.2 Docker Deployment

```
Docker Host
│
├── pos_network (Bridge Network)
│
├── Container: postgres
│   ├── Image: postgres:15-alpine
│   ├── Port: 5432
│   ├── Volume: postgres_data
│   └── Environment: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
│
├── Container: backend
│   ├── Build: ./backend/Dockerfile
│   ├── Port: 5000
│   ├── Volumes: ./backend, ./receipts, ./database
│   ├── Depends on: postgres
│   └── Environment: DATABASE_URL, FLASK_ENV
│
└── Container: frontend
    ├── Build: ./frontend/Dockerfile
    ├── Port: 5173
    ├── Volume: node_modules
    ├── Depends on: backend
    └── Environment: VITE_API_BASE_URL
```

**docker-compose.yml Structure:**
```yaml
version: '3.8'
services:
  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=pos_db
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
  
  backend:
    build: ./backend
    depends_on:
      db:
        condition: service_healthy
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/pos_db
  
  frontend:
    build: ./frontend
    depends_on:
      - backend
    environment:
      - VITE_API_BASE_URL=http://backend:5000/api

volumes:
  postgres_data:
```

### 7.3 CI/CD Pipeline

```
GitHub Repository
│
├── Push to branch
│   ↓
├── GitHub Actions Workflow
│   ├── Job: backend-test
│   │   ├── Setup Python
│   │   ├── Install dependencies
│   │   ├── Run pytest
│   │   └── Generate coverage
│   │
│   ├── Job: frontend-test
│   │   ├── Setup Node.js
│   │   ├── Install dependencies
│   │   ├── Run linter
│   │   └── Run tests
│   │
│   ├── Job: docker-build
│   │   ├── Build backend image
│   │   └── Build frontend image
│   │
│   ├── Job: security-scan
│   │   └── Trivy vulnerability scan
│   │
│   └── Job: deploy (main branch only)
│       └── Deploy to environment
│
└── Deployment Success
```

---

## 8. Security Architecture

### 8.1 Authentication Flow

```
┌──────────┐                                  ┌──────────┐
│  Client  │                                  │  Server  │
└────┬─────┘                                  └────┬─────┘
     │                                             │
     │  1. POST /api/auth/login                   │
     │    {username, password}                    │
     ├────────────────────────────────────────────▶
     │                                             │
     │              2. Verify credentials          │
     │              3. Generate JWT tokens         │
     │                                             │
     │  4. Return tokens                           │
     │    {access_token, refresh_token, user}     │
     ◀────────────────────────────────────────────┤
     │                                             │
     │  5. Store tokens in localStorage            │
     │                                             │
     │  6. Authenticated requests                  │
     │    Authorization: Bearer {access_token}    │
     ├────────────────────────────────────────────▶
     │                                             │
     │              7. Validate token              │
     │              8. Check role/permissions      │
     │                                             │
     │  9. Return response                         │
     ◀────────────────────────────────────────────┤
     │                                             │
```

### 8.2 Authorization (RBAC)

**Role Hierarchy:**
```
Administrator (Full Access)
    │
    ├── All Manager Permissions
    └── + User Management
        + Product Management
        + System Configuration

Manager (Supervisory Access)
    │
    ├── All Cashier Permissions
    └── + Process Refunds
        + View Reports
        + Manager Override
        + Audit Log Access

Cashier (Basic Access)
    │
    └── Product Scanning
        Cart Management
        Checkout Processing
        View Own Transactions
```

**Permission Matrix:**

| Operation | Cashier | Manager | Admin |
|-----------|---------|---------|-------|
| Login | ✓ | ✓ | ✓ |
| Scan Products | ✓ | ✓ | ✓ |
| Manage Cart | ✓ | ✓ | ✓ |
| Checkout | ✓ | ✓ | ✓ |
| Apply Discount (<50%) | ✓ | ✓ | ✓ |
| Apply Large Discount | ✗ | ✓ | ✓ |
| Process Refund | ✗ | ✓ | ✓ |
| View Reports | ✗ | ✓ | ✓ |
| Manage Products | ✗ | ✗ | ✓ |
| Manage Users | ✗ | ✗ | ✓ |
| System Settings | ✗ | ✗ | ✓ |

### 8.3 Security Measures

1. **Password Security**
   - bcrypt hashing (cost factor 12)
   - No plaintext storage
   - Secure random salt

2. **Token Security**
   - JWT with signature verification
   - Access token: 8-hour expiry
   - Refresh token: 30-day expiry
   - Token revocation support

3. **Session Security**
   - Account lockout after 5 failed attempts
   - IP address logging
   - User agent tracking

4. **API Security**
   - CORS configuration
   - Rate limiting (planned)
   - Input validation
   - SQL injection prevention (ORM)
   - XSS prevention

5. **Audit Logging**
   - All sensitive operations logged
   - User actions tracked
   - Failed login attempts recorded

---

## 9. Quality Attributes

### 9.1 Performance

**Requirements:**
- Checkout < 2 seconds (90% of requests)
- API response < 500ms for simple queries
- Database queries optimized with indexes

**Strategies:**
- Database connection pooling
- Query optimization
- Appropriate indexing
- Efficient data structures

**Monitoring:**
- Response time logging
- Performance profiling
- Database query analysis

---

### 9.2 Scalability

**Current Scale:**
- 50 concurrent users
- 1000 transactions/day
- Single server deployment

**Scaling Strategy:**
- Horizontal scaling: Load balancer + multiple app servers
- Vertical scaling: Increase server resources
- Database: Read replicas for reporting
- Caching: Redis for session/cart data

---

### 9.3 Availability

**Target:** 99% uptime

**Strategies:**
- Error handling and recovery
- Database connection retry logic
- Health check endpoint
- Graceful degradation

**Monitoring:**
- Uptime monitoring
- Health checks
- Error rate tracking

---

### 9.4 Maintainability

**Code Organization:**
- Clear separation of concerns
- Modular design
- Consistent coding standards
- Comprehensive documentation

**Testing:**
- Unit tests (70%+ coverage)
- Integration tests
- API tests
- Automated test execution

**Documentation:**
- Inline code comments
- API documentation
- Architecture documentation
- Deployment guides

---

### 9.5 Security

**Requirements:**
- Secure authentication
- Role-based access control
- Data encryption (passwords)
- Audit logging

**Implementation:**
- See Section 8 (Security Architecture)

---

## 10. Technology Stack Summary

### 10.1 Backend Stack
- **Language:** Python 3.11
- **Framework:** Flask 3.0
- **ORM:** SQLAlchemy 2.0
- **Authentication:** Flask-JWT-Extended
- **PDF:** ReportLab
- **Testing:** pytest

### 10.2 Frontend Stack
- **Framework:** React 18
- **Build Tool:** Vite
- **Styling:** TailwindCSS
- **HTTP Client:** Axios
- **Routing:** React Router

### 10.3 Database
- **Development:** SQLite 3
- **Production:** PostgreSQL 15

### 10.4 DevOps
- **Containerization:** Docker & Docker Compose
- **CI/CD:** GitHub Actions
- **Version Control:** Git/GitHub

---

## 11. Design Decisions

### 11.1 Key Architectural Decisions

| Decision | Rationale | Trade-offs |
|----------|-----------|------------|
| Three-tier architecture | Clear separation, scalability | More complex than monolith |
| React SPA | Modern UX, fast client-side | SEO limitations |
| RESTful API | Standard, well-understood | Less efficient than GraphQL |
| JWT authentication | Stateless, scalable | Token revocation complexity |
| SQLAlchemy ORM | Database independence, productivity | Some performance overhead |
| Docker deployment | Consistent environments, easy setup | Additional complexity |

---

## 12. Future Architecture Considerations

### 12.1 Potential Enhancements

**Microservices:**
- Split into Auth, Cart, Checkout, Reporting services
- Independent scaling and deployment
- Service-to-service communication

**Caching Layer:**
- Redis for session management
- Cache frequently accessed data
- Improve performance

**Message Queue:**
- Asynchronous receipt generation
- Background report processing
- Event-driven architecture

**API Gateway:**
- Centralized request routing
- Rate limiting
- API versioning

---

## 13. Conclusion

The POS Simulator architecture provides a solid foundation for:
- Educational demonstration of software engineering practices
- Production-quality codebase structure
- Clear separation of concerns
- Maintainable and testable code
- Secure and performant system

**Strengths:**
- Well-organized component structure
- Clear data flow
- Comprehensive security measures
- Production-ready deployment

**Areas for Future Enhancement:**
- Microservices architecture
- Advanced caching
- Real-time features
- Enhanced monitoring

---

**Document Status:** ✅ Final  
**Last Updated:** November 16, 2025  
**Approved By:** Development Team  

---

*End of Software Architecture Document*
