# Software Requirements Specification (SRS)
## Project: Point of Sale (POS) Simulator

**Version:** 1.0  
**Authors:** Narayana S, Mithun Naik, Dimpu Kumar, Darshan H V  
**Date:** 02-09-2025  
**Status:** Final  

---

## Revision History

| Version | Date | Author | Change Summary |
|---------|------|--------|----------------|
| 1.0 | 02-09-2025 | Narayana S, Mithun Naik, Dimpu Kumar, Darshan H V | Initial draft of SRS for POS Simulator |
| 1.1 | 16-11-2025 | Development Team | Updated with implementation details and verification |

---

## 1. Introduction

### 1.1 Purpose
This document provides the Software Requirements Specification (SRS) for a Point of Sale (POS) Simulator. It defines functional and non-functional requirements, interfaces, and acceptance criteria for the development of a software simulator that mimics a retail POS system for educational and testing purposes.

### 1.2 Scope
The POS Simulator covers cashier functions including product scanning, cart management, discounts, tax calculation, payment processing (mock cash, card, and UPI), receipt generation, and inventory updates. It will also support manager overrides, refunds, and reporting functions. The system excludes actual payment gateway integration and physical hardware interactions beyond mock interfaces.

**Key Features:**
- Product scanning and cart management
- Real-time tax and discount calculation
- Mock payment processing (Cash, Card, UPI)
- PDF receipt generation
- Inventory management with automatic updates
- Refund and void transactions
- Manager override with PIN verification
- Role-based access control (Cashier, Manager, Administrator)
- Sales reporting and history search
- Audit logging for all operations

### 1.3 Audience
- Developers
- QA Engineers
- SE Course Evaluators
- Students
- Project Reviewers

### 1.4 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|------------|
| POS | Point of Sale |
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| RTM | Requirements Traceability Matrix |
| RBAC | Role-Based Access Control |
| JWT | JSON Web Token |
| API | Application Programming Interface |
| PDF | Portable Document Format |
| UPI | Unified Payments Interface |
| SKU | Stock Keeping Unit |

---

## 2. Overall Description

### 2.1 Product Perspective
The POS Simulator is a software-only system designed for academic and demonstration use. It emulates cashier operations and backend data management typically found in retail POS terminals.

**System Context:**
- Web-based application with React frontend
- RESTful API backend using Python Flask
- SQLite database (development) / PostgreSQL (production)
- No external hardware dependencies
- Mock payment processing (no real financial transactions)

### 2.2 Major Product Functions

1. **Product Management**
   - Scan/add product by barcode or SKU
   - Manual product search with autocomplete
   - Stock validation before checkout
   - Inventory tracking and updates

2. **Cart Operations**
   - Add, update, remove items
   - Quantity management
   - Apply discounts (item-level and order-level)
   - Real-time tax calculation

3. **Payment Processing**
   - Mock payment methods: Cash, Card, UPI
   - Payment success/failure simulation
   - Transaction rollback on failure

4. **Receipt Management**
   - Automatic PDF receipt generation
   - Receipt download and print
   - Transaction history storage

5. **Refund and Void**
   - Manager-authorized refunds
   - Transaction void capability
   - Inventory restocking on refund

6. **Manager Functions**
   - Override restricted operations
   - PIN-based authorization
   - Approve large discounts

7. **Reporting**
   - Daily sales reports
   - Sales history search
   - CSV and PDF export
   - Audit log access

8. **Administration**
   - User management
   - Role assignment
   - Product configuration
   - Tax and discount rules

### 2.3 User Roles and Characteristics

| Role | Characteristics | Permissions |
|------|----------------|-------------|
| **Cashier** | Basic computer knowledge, performs daily sales | Product scanning, cart management, checkout, basic operations |
| **Manager** | Experienced user, supervises operations | All cashier permissions + refunds, overrides, reports access |
| **Administrator** | Technical knowledge, system configuration | Full system access including user management, product configuration |

### 2.4 Operating Environment

**Hardware Requirements:**
- Modern desktop or laptop computer
- Minimum 4GB RAM
- 10GB free disk space

**Software Requirements:**
- Operating System: Windows 10/11, Linux, or macOS
- Web Browser: Chrome, Firefox, Edge (latest versions)
- Python 3.11+ (for backend)
- Node.js 20+ (for frontend development)

**Network Requirements:**
- No internet connectivity required for core operations
- Local network access for database connectivity

### 2.5 Design and Implementation Constraints

1. **Mock Payments Only**: No integration with real payment gateways
2. **Educational Purpose**: Designed for learning and demonstration, not production retail use
3. **Offline-First**: System must function without internet connectivity
4. **Lab Environment**: Must run in computer lab settings without special hardware
5. **Database**: SQLite for development, PostgreSQL for production deployment
6. **Security**: Strong authentication required but simplified for educational context

### 2.6 Assumptions and Dependencies

**Assumptions:**
- Users have basic computer literacy
- System runs on reliable hardware
- Database backups are performed regularly
- Mock payment responses are sufficient for testing

**Dependencies:**
- Python Flask framework
- React frontend library
- SQLAlchemy ORM
- ReportLab for PDF generation
- JWT for authentication

---

## 3. External Interface Requirements

### 3.1 User Interfaces

**UI Components:**
1. **Login Screen**
   - Username and password fields
   - Role-based redirection after login
   - Error messages for invalid credentials

2. **Cashier Dashboard (POS Screen)**
   - Product search bar with barcode/SKU input
   - Product list with autocomplete
   - Cart display (right panel, 40% width)
   - Item quantity controls
   - Discount application controls
   - Total calculation display
   - Payment method selection
   - Checkout button

3. **Manager Dashboard**
   - Sales overview widgets
   - Quick access to reports
   - Refund management link
   - System status indicators

4. **Refunds Page**
   - Transaction search by number
   - Transaction details display
   - Refund reason input
   - Refund amount specification
   - Authorization controls

5. **Reports Page**
   - Date range selector
   - Report type selector (Sales, Inventory, Audit)
   - Export format options (CSV, PDF)
   - Filtering controls
   - Data visualization

6. **Products Management (Admin)**
   - Product list table
   - Add/Edit product forms
   - Stock adjustment controls
   - Product search and filters

**UI Design Principles:**
- Responsive design using TailwindCSS
- Clear visual hierarchy
- Tooltips for all major actions
- Error messages displayed prominently
- Confirmation dialogs for destructive actions
- Keyboard shortcuts for common operations

### 3.2 Hardware Interfaces

**Simulated Interfaces:**
1. **Barcode Scanner Input**
   - Simulated via text input field
   - Accepts barcode string input
   - Triggers product lookup on Enter key

2. **Receipt Printer**
   - Simulated via PDF generation
   - Download PDF to local filesystem
   - Print dialog triggered for physical printing

### 3.3 Software Interfaces

**Database Interface:**
- **System**: SQLite (dev) / PostgreSQL (prod)
- **ORM**: SQLAlchemy 2.0+
- **Connection**: Persistent connection pool
- **Transactions**: ACID-compliant operations

**Backend API:**
- **Protocol**: RESTful HTTP/HTTPS
- **Format**: JSON request/response bodies
- **Authentication**: JWT Bearer tokens
- **Base URL**: `http://localhost:5000/api`

**External Libraries:**
- **ReportLab**: PDF receipt generation
- **bcrypt**: Password hashing
- **Flask-JWT-Extended**: JWT token management
- **Axios**: HTTP client (frontend)

### 3.4 Communications Interfaces

**API Communication:**
- HTTP methods: GET, POST, PUT, PATCH, DELETE
- Content-Type: application/json
- Authorization header: Bearer {token}
- Error responses: Standard HTTP status codes

**Internal APIs:** (No external network required)
- Frontend ↔ Backend: REST API
- Backend ↔ Database: SQLAlchemy ORM
- No external internet dependencies for core functionality

---

## 4. System Features

### 4.1 Functional Requirements

#### FR-001: Product Scanning and Addition

**Req ID:** POS-F-001  
**Priority:** High  
**Source:** Cashier  

**Description:** The system shall allow adding products by barcode or manual entry.

**Inputs:**
- Barcode string or SKU code
- Manual product search query

**Processing:**
- Validate barcode/SKU exists in database
- Check product availability
- Retrieve product details (name, price, tax rate, stock)

**Outputs:**
- Product added to cart
- Cart updated with item details
- Error message if product not found or out of stock

**Acceptance Criteria:**
- AC-001.1: Product appears in cart immediately after valid barcode entry
- AC-001.2: Invalid barcode shows error message within 1 second
- AC-001.3: Manual search shows autocomplete suggestions
- AC-001.4: Out-of-stock products cannot be added

**Test Case:** TC-001

---

#### FR-002: Cart Management

**Req ID:** POS-F-002  
**Priority:** High  
**Source:** Cashier  

**Description:** The system shall maintain a cart with multiple items and quantities.

**Functional Details:**
- Add items to cart
- Update item quantities (increment/decrement)
- Remove items from cart
- Clear entire cart
- Persist cart state during session

**Acceptance Criteria:**
- AC-002.1: Cart displays all items with quantities
- AC-002.2: Quantity changes update subtotal immediately
- AC-002.3: Remove button deletes item from cart
- AC-002.4: Cart state persists until checkout or clear

**Test Case:** TC-002

---

#### FR-003: Tax and Discount Calculation

**Req ID:** POS-F-003  
**Priority:** High  
**Source:** Cashier/Manager  

**Description:** The system shall calculate subtotal, taxes, and discounts in real time.

**Calculation Rules:**
- Subtotal = Σ(item_price × quantity)
- Discount = Item discount + Order discount
- Tax = (Subtotal - Discount) × tax_rate
- Total = Subtotal - Discount + Tax

**Acceptance Criteria:**
- AC-003.1: Calculations update within 200ms of cart changes
- AC-003.2: Tax rate applied per product tax class
- AC-003.3: Discounts correctly reduce total
- AC-003.4: Display breakdown: Subtotal, Discount, Tax, Total

**Test Case:** TC-003

---

#### FR-004: Discount Application

**Req ID:** POS-F-004  
**Priority:** Medium  
**Source:** Manager  

**Description:** The system shall support item-level and order-level discounts.

**Discount Types:**
- Item-level: Percentage or fixed amount per item
- Order-level: Percentage or fixed amount on total
- Manager override required for discounts > 50%

**Acceptance Criteria:**
- AC-004.1: Item discount applies only to specific item
- AC-004.2: Order discount applies to entire cart
- AC-004.3: Manager PIN required for large discounts
- AC-004.4: Discount validation prevents negative totals

**Test Case:** TC-004

---

#### FR-005: Stock Validation

**Req ID:** POS-F-005  
**Priority:** High  
**Source:** Cashier/Admin  

**Description:** The system shall validate stock availability before checkout.

**Validation Rules:**
- Check requested quantity ≤ available stock
- Block checkout if insufficient stock
- Real-time stock checking during cart operations

**Acceptance Criteria:**
- AC-005.1: Checkout prevented if any item exceeds stock
- AC-005.2: Clear error message indicating which item is out of stock
- AC-005.3: Stock levels updated immediately after successful checkout

**Test Case:** TC-005

---

#### FR-006: Payment Processing

**Req ID:** POS-F-006  
**Priority:** High  
**Source:** Cashier  

**Description:** The system shall process mock payments via cash, card, and UPI.

**Payment Methods:**
- Cash: Accept amount, calculate change
- Card: Mock approval/decline response
- UPI: Mock transaction ID generation

**Processing Flow:**
1. Select payment method
2. Enter payment details
3. Process payment (mock API call)
4. Handle success/failure response
5. Rollback on failure

**Acceptance Criteria:**
- AC-006.1: All three payment methods available
- AC-006.2: Success creates transaction record
- AC-006.3: Failure rolls back and shows error
- AC-006.4: Change calculated correctly for cash payments

**Test Case:** TC-006

---

#### FR-007: Receipt Generation

**Req ID:** POS-F-007  
**Priority:** Medium  
**Source:** Cashier  

**Description:** The system shall generate receipts in PDF format.

**Receipt Contents:**
- Store name and details
- Transaction ID and timestamp
- Cashier name
- Itemized list with prices
- Subtotal, discount, tax, total
- Payment method
- Footer message

**Acceptance Criteria:**
- AC-007.1: PDF generated automatically on successful payment
- AC-007.2: Receipt downloadable/printable
- AC-007.3: All transaction details included
- AC-007.4: Receipt stored in database for retrieval

**Test Case:** TC-007

---

#### FR-008: Transaction Recording

**Req ID:** POS-F-008  
**Priority:** High  
**Source:** Admin  

**Description:** The system shall record each sale transaction in the database.

**Transaction Data:**
- Unique transaction ID
- Transaction number (human-readable)
- Cashier ID
- Timestamp
- Items and quantities
- Amounts (subtotal, discount, tax, total)
- Payment method and status
- Receipt reference

**Acceptance Criteria:**
- AC-008.1: Every successful checkout creates transaction record
- AC-008.2: Transaction atomic (all or nothing)
- AC-008.3: No data loss on system failure
- AC-008.4: Transaction retrievable by ID or number

**Test Case:** TC-008

---

#### FR-009: Refund and Void Operations

**Req ID:** POS-F-009  
**Priority:** Medium  
**Source:** Manager  

**Description:** The system shall support refund and void operations.

**Refund Process:**
1. Search original transaction
2. Verify transaction eligible for refund
3. Manager authorization (PIN)
4. Specify refund amount and reason
5. Process refund
6. Restock inventory
7. Generate refund receipt

**Void Process:**
- Cancel transaction before completion
- Restore inventory
- No receipt generated

**Acceptance Criteria:**
- AC-009.1: Only managers can process refunds
- AC-009.2: Refund creates new transaction record
- AC-009.3: Inventory restored on refund
- AC-009.4: Partial refunds supported
- AC-009.5: Refund reason required

**Test Case:** TC-009

---

#### FR-010: Manager Override

**Req ID:** POS-F-010  
**Priority:** Medium  
**Source:** Manager  

**Description:** The system shall allow manager override for restricted actions.

**Restricted Actions:**
- Discounts > 50%
- Price modifications
- Refunds
- Transaction voids
- System configuration changes

**Override Process:**
1. Cashier attempts restricted action
2. System prompts for manager PIN
3. Manager enters 4-digit PIN
4. System validates PIN and role
5. Action authorized or denied
6. Override logged to audit trail

**Acceptance Criteria:**
- AC-010.1: Manager PIN required for restricted actions
- AC-010.2: Invalid PIN prevents action
- AC-010.3: All overrides logged with manager ID
- AC-010.4: Override authorization expires after action

**Test Case:** TC-010

---

#### FR-011: Inventory Management

**Req ID:** POS-F-011  
**Priority:** High  
**Source:** Admin  

**Description:** The system shall update inventory after each sale or refund.

**Inventory Operations:**
- Decrement stock on successful sale
- Increment stock on refund
- Manual stock adjustments (admin only)
- Inventory audit trail

**Update Rules:**
- Transactional updates (atomic)
- Optimistic locking to prevent race conditions
- Stock cannot go negative
- All changes logged

**Acceptance Criteria:**
- AC-011.1: Stock reduced immediately after checkout
- AC-011.2: Stock restored on refund
- AC-011.3: All inventory changes logged
- AC-011.4: No stock inconsistencies after 100 transactions

**Test Case:** TC-011

---

#### FR-012: Sales Reporting

**Req ID:** POS-F-012  
**Priority:** Medium  
**Source:** Manager/Admin  

**Description:** The system shall generate daily sales reports.

**Report Types:**
1. Sales Summary
   - Total sales amount
   - Number of transactions
   - Payment method breakdown
   - Top selling products

2. Inventory Report
   - Current stock levels
   - Low stock alerts
   - Inventory movements

3. Audit Report
   - User actions log
   - Failed login attempts
   - Manager overrides

**Report Formats:**
- PDF for printing
- CSV for data analysis

**Acceptance Criteria:**
- AC-012.1: Reports generated for any date range
- AC-012.2: Reports exportable as PDF and CSV
- AC-012.3: Reports match transaction data
- AC-012.4: Report generation < 5 seconds

**Test Case:** TC-012

---

#### FR-013: Sales History Search

**Req ID:** POS-F-013  
**Priority:** Low  
**Source:** Manager/Admin  

**Description:** The system shall allow searching sales history.

**Search Criteria:**
- Transaction number
- Date range
- Cashier
- Amount range
- Product
- Payment method
- Status

**Search Results:**
- Transaction list with key details
- Pagination (50 per page)
- Sort by date, amount, etc.
- Click to view full details

**Acceptance Criteria:**
- AC-013.1: Search returns matching transactions
- AC-013.2: Multiple filters combinable
- AC-013.3: Search results displayed within 1 second
- AC-013.4: Export search results to CSV

**Test Case:** TC-013

---

#### FR-014: Role-Based Access Control

**Req ID:** POS-F-014  
**Priority:** High  
**Source:** All Users  

**Description:** The system shall support user roles (cashier, manager, admin).

**Roles and Permissions:**

| Permission | Cashier | Manager | Admin |
|------------|---------|---------|-------|
| Product scanning | ✓ | ✓ | ✓ |
| Cart management | ✓ | ✓ | ✓ |
| Checkout | ✓ | ✓ | ✓ |
| Apply discounts (<50%) | ✓ | ✓ | ✓ |
| Apply large discounts | ✗ | ✓ | ✓ |
| Process refunds | ✗ | ✓ | ✓ |
| View reports | ✗ | ✓ | ✓ |
| User management | ✗ | ✗ | ✓ |
| Product management | ✗ | ✗ | ✓ |
| System configuration | ✗ | ✗ | ✓ |

**Acceptance Criteria:**
- AC-014.1: Role assigned at user creation
- AC-014.2: Permissions enforced in API and UI
- AC-014.3: Unauthorized access blocked with error message
- AC-014.4: Role changes take effect immediately

**Test Case:** TC-014

---

#### FR-015: Error Handling

**Req ID:** POS-F-015  
**Priority:** High  
**Source:** All Users  

**Description:** The system shall provide error messages for failed operations.

**Error Categories:**
- Validation errors (invalid input)
- Authentication errors (login failed)
- Authorization errors (permission denied)
- Business logic errors (insufficient stock)
- System errors (database unavailable)

**Error Response Format:**
```json
{
  "error": "Short error message",
  "message": "Detailed explanation",
  "code": "ERROR_CODE",
  "timestamp": "2025-11-16T10:30:00Z"
}
```

**Acceptance Criteria:**
- AC-015.1: All errors display user-friendly messages
- AC-015.2: Technical details logged but not shown to users
- AC-015.3: Error messages guide users to corrective action
- AC-015.4: System remains stable after errors

**Test Case:** TC-015

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

#### NFR-001: Checkout Response Time

**Req ID:** POS-NF-001  
**Priority:** High  
**Metric:** Response time < 2 seconds for 90% of checkout operations

**Acceptance Criteria:**
- AC-NF-001.1: Average checkout time ≤ 1.5 seconds
- AC-NF-001.2: 90th percentile ≤ 2 seconds
- AC-NF-001.3: No timeout errors under normal load

**Test Case:** TC-Perf-01  
**Measurement Method:** Performance testing with 100 transactions

---

#### NFR-002: System Availability

**Req ID:** POS-NF-002  
**Priority:** High  
**Metric:** 99% uptime in lab environment

**Acceptance Criteria:**
- AC-NF-002.1: System operational 99% of test period
- AC-NF-002.2: Graceful degradation on component failure
- AC-NF-002.3: Auto-recovery from transient errors

**Test Case:** TC-Avail-01  
**Measurement Method:** 24-hour uptime monitoring

---

### 5.2 Data Integrity Requirements

#### NFR-003: Data Consistency

**Req ID:** POS-NF-003  
**Priority:** High  

**Description:** The system shall maintain data consistency across sales and inventory records.

**Consistency Rules:**
- Inventory changes match transaction records
- Financial totals accurate to the cent
- No orphaned records
- Referential integrity enforced

**Acceptance Criteria:**
- AC-NF-003.1: Zero data mismatches after 100 test transactions
- AC-NF-003.2: Database constraints prevent invalid data
- AC-NF-003.3: Transaction rollback on any failure

**Test Case:** TC-Data-01  
**Measurement Method:** Automated consistency checker after stress test

---

### 5.3 Auditability Requirements

#### NFR-004: Audit Logging

**Req ID:** POS-NF-004  
**Priority:** Medium  

**Description:** The system shall provide audit logs of user operations.

**Logged Events:**
- User login/logout
- Failed login attempts
- Transaction creation
- Refund processing
- Manager overrides
- Product/user modifications
- Settings changes

**Log Format:**
- Timestamp (ISO 8601)
- User ID and username
- Action type
- Details (JSON)
- IP address
- Result (success/failure)

**Acceptance Criteria:**
- AC-NF-004.1: All critical operations logged
- AC-NF-004.2: Logs tamper-evident
- AC-NF-004.3: Log retention for 90 days minimum
- AC-NF-004.4: Logs searchable by date, user, action

**Test Case:** TC-Audit-01

---

### 5.4 Usability Requirements

#### NFR-005: User Interface Simplicity

**Req ID:** POS-NF-005  
**Priority:** Medium  

**Description:** The system shall be usable by beginners with a simple UI and tooltips.

**Usability Features:**
- Intuitive navigation
- Clear visual hierarchy
- Tooltips on all major controls
- Keyboard shortcuts
- Responsive feedback
- Error prevention (confirmations)

**Acceptance Criteria:**
- AC-NF-005.1: New users complete training transaction in < 5 minutes
- AC-NF-005.2: Usability survey score ≥ 80% satisfaction
- AC-NF-005.3: All critical actions accessible within 3 clicks
- AC-NF-005.4: Mobile responsive design

**Test Case:** TC-UI-01  
**Measurement Method:** User testing with 5+ participants

---

## 6. Security Requirements

### SR-001: Authentication

**Req ID:** POS-SR-001  
**Priority:** High  

**Description:** The system shall require login with username and password/PIN.

**Authentication Mechanism:**
- Username and password for login
- JWT tokens for session management
- 4-digit PIN for manager overrides
- Token expiry after 8 hours
- Refresh tokens for extended sessions

**Acceptance Criteria:**
- AC-SR-001.1: No access without valid credentials
- AC-SR-001.2: Invalid credentials show error message
- AC-SR-001.3: Sessions expire after timeout
- AC-SR-001.4: Logout clears session immediately

**Test Case:** TC-Login-01

---

### SR-002: Authorization (RBAC)

**Req ID:** POS-SR-002  
**Priority:** High  

**Description:** The system shall enforce role-based access control for different operations.

**Implementation:**
- Roles stored in user record
- JWT token contains role claim
- API endpoints check permissions
- UI hides unauthorized actions

**Acceptance Criteria:**
- AC-SR-002.1: Cashier blocked from manager operations
- AC-SR-002.2: Manager blocked from admin operations
- AC-SR-002.3: API returns 403 Forbidden for unauthorized requests
- AC-SR-002.4: UI dynamically adjusts based on role

**Test Case:** TC-Role-01

---

### SR-003: Credential Encryption

**Req ID:** POS-SR-003  
**Priority:** High  

**Description:** The system shall encrypt stored user credentials.

**Encryption Standards:**
- Passwords hashed with bcrypt (cost factor 12)
- PINs hashed separately
- No plaintext storage
- Secure random salt generation

**Acceptance Criteria:**
- AC-SR-003.1: Passwords not readable in database
- AC-SR-003.2: Hash verification succeeds for valid passwords
- AC-SR-003.3: Rainbow table attacks ineffective
- AC-SR-003.4: Database dump reveals no credentials

**Test Case:** TC-Encrypt-01

---

### SR-004: Operation Restrictions

**Req ID:** POS-SR-004  
**Priority:** Medium  

**Description:** The system shall restrict refunds and overrides to managers only.

**Restricted Operations:**
- Process refunds
- Void transactions
- Approve large discounts
- Modify prices
- Access audit logs

**Acceptance Criteria:**
- AC-SR-004.1: Cashier refund attempt blocked
- AC-SR-004.2: Manager PIN required for authorization
- AC-SR-004.3: Invalid PIN prevents action
- AC-SR-004.4: All attempts logged

**Test Case:** TC-Refund-01

---

### SR-005: Login Attempt Logging

**Req ID:** POS-SR-005  
**Priority:** Medium  

**Description:** The system shall log all failed login attempts.

**Logged Information:**
- Username attempted
- Timestamp
- IP address
- Failure reason
- User agent

**Security Measures:**
- Account lockout after 5 failed attempts
- 15-minute lockout duration
- Admin notification on repeated failures

**Acceptance Criteria:**
- AC-SR-005.1: Failed logins recorded in database
- AC-SR-005.2: Lockout prevents brute force attacks
- AC-SR-005.3: Admin can unlock accounts
- AC-SR-005.4: Audit trail complete

**Test Case:** TC-Log-01

---

## 7. Quality Attributes & Acceptance Tests

### 7.1 Test Coverage Requirements

**Minimum Coverage:**
- Unit tests: ≥ 70% code coverage
- Integration tests: All API endpoints
- Functional tests: All user stories
- Security tests: All authentication/authorization paths

### 7.2 Acceptance Testing Strategy

**Testing Phases:**
1. **Unit Testing**: Individual functions and methods
2. **Integration Testing**: API endpoints and database operations
3. **System Testing**: End-to-end user scenarios
4. **User Acceptance Testing**: Real user validation
5. **Performance Testing**: Load and stress tests
6. **Security Testing**: Penetration testing basics

### 7.3 Test Environment

**Requirements:**
- Isolated test database
- Test user accounts (all roles)
- Sample product data (100+ items)
- Mock payment responses
- Automated test execution

---

## 8. System Architecture

### 8.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Web Browser                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │         React Frontend (Port 5173)                │  │
│  │  - POS Interface  - Reports  - Admin Panel       │  │
│  └────────────────┬─────────────────────────────────┘  │
└───────────────────┼─────────────────────────────────────┘
                    │ REST API (JSON)
                    │
┌───────────────────▼─────────────────────────────────────┐
│            Flask Backend (Port 5000)                     │
│  ┌──────────┬──────────┬──────────┬──────────────────┐ │
│  │  Auth    │  Cart    │ Checkout │  Reports         │ │
│  │  Routes  │  Routes  │  Routes  │  Routes          │ │
│  └──────────┴──────────┴──────────┴──────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │            Business Logic Layer                     │ │
│  │  - Payment Processing  - Tax Calculation           │ │
│  │  - Inventory Management  - PDF Generation          │ │
│  └────────────────────┬───────────────────────────────┘ │
└────────────────────────┼───────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────┐
│              SQLAlchemy ORM                             │
│  ┌──────────┬──────────┬──────────┬──────────────────┐ │
│  │  User    │ Product  │Transaction│  Refund          │ │
│  │  Model   │  Model   │  Model    │  Model           │ │
│  └──────────┴──────────┴──────────┴──────────────────┘ │
└────────────────────────┬───────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────┐
│         Database (SQLite/PostgreSQL)                    │
│  - users  - products  - transactions  - refunds        │
│  - transaction_items  - audit_logs  - settings         │
└─────────────────────────────────────────────────────────┘
```

### 8.2 Technology Stack

**Frontend:**
- React 18
- Vite (build tool)
- TailwindCSS (styling)
- Axios (HTTP client)
- React Router (navigation)

**Backend:**
- Python 3.11
- Flask 3.0
- Flask-JWT-Extended (authentication)
- SQLAlchemy 2.0 (ORM)
- ReportLab (PDF generation)

**Database:**
- SQLite (development)
- PostgreSQL 15 (production)

**DevOps:**
- Docker & Docker Compose
- GitHub Actions (CI/CD)

---

## 9. UML Use Case Diagram

The system includes two primary use case diagrams:

### 9.1 Cashier Operations
- Scan or Add product
- Manage cart
- Print and give receipt
- Take payments
- Calculate taxes
- Apply standard discounts

### 9.2 Manager Operations
- Authorize refunds or voids
- Approve or apply discounts
- Override restricted operations
- Generate reports

**Actors:**
- Cashier (Primary)
- Manager (Supervisory)

**System Boundary:** POS Simulation

*(See attached UML diagram image)*

---

## 10. Requirements Traceability Matrix (RTM)

A complete RTM document has been created separately: **RTM.csv**

The RTM maps:
- Requirement ID → Design Specification → Module → Test Cases
- All 25 requirements (15 FR + 5 NFR + 5 SR)
- Test case references
- Implementation status

---

## 11. Appendices

### Appendix A: Test Cases Reference
See **TEST_CASES.md** for detailed test case documentation.

### Appendix B: Project Test Plan
See **PROJECT_TEST_PLAN.md** for comprehensive testing strategy.

### Appendix C: Software Architecture Document
See **SOFTWARE_ARCHITECTURE.md** for detailed architecture design.

### Appendix D: Software Design Document
See **SOFTWARE_DESIGN.md** for low-level design details.

---

## 12. Approval

**Prepared by:**
- Narayana S (Developer)
- Mithun Naik (Developer)
- Dimpu Kumar (Developer)
- Darshan H V (Developer)

**Review Status:** ✅ Approved  
**Implementation Status:** ✅ Complete  
**Verification Status:** ✅ Verified  

---

**Document Control:**
- Location: `/docs/SRS.md`
- Classification: Internal
- Distribution: Project Team, Evaluators
- Next Review: Post-implementation review

---

*End of Software Requirements Specification*
