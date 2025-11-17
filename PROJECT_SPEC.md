# Project: POS Simulator — Final Implementation Specification

Project goal (one line)

Build a production-like POS Simulator with a responsive frontend, backend API, persistent database, authentication & RBAC, receipt generation, basic reporting, and CI/CD pipeline. Deliver a deployable Dockerized app with test coverage, integration tests, and documented APIs.

---

## 1. High-level architecture & tech stack (suggested)

Frontend: React (Vite or CRA), TypeScript, TailwindCSS (or Chakra/Material), Axios / react-query for API calls

Backend: Node.js + Express (TypeScript recommended) or Python (FastAPI) — choose one. (Below examples use Node + Express + TypeScript).

Database: PostgreSQL (relational), use Sequelize/TypeORM or Prisma ORM

Persisted files: receipts stored on disk or object store (local ./storage/receipts for project)

Auth: JWT access tokens + refresh tokens (or session cookies for simplicity)

DevOps: Docker + docker-compose, GitHub Actions for CI (lint, test, build)

Testing: Jest + supertest (backend), React Testing Library (frontend), Playwright optional for E2E

Documentation: OpenAPI/Swagger for backend APIs, PROJECT_SPEC.md and README.md


---

## 2. Epics (3)

Create these three epics in Jira (or use labels if no epics required).

EPIC-1: Cashier Operations
Goal: Core checkout flows used by cashiers.

EPIC-2: Manager & Admin Operations
Goal: Refunds, overrides, reporting, inventory management.

EPIC-3: Security, Performance & Delivery
Goal: Auth, RBAC, tests, CI/CD, deployment, monitoring.


---

## 3. Complete user stories (14) — copy into Jira

> Format: Summary, Description, Acceptance Criteria (AC), Priority, Story Points, Sprint


### Sprint 1 (Core cashier flow) — US-01 to US-06

US-01 — Add Product to Cart

Description: As a cashier, I want to add products to the cart using barcode or manual entry so I can quickly create a customer order.

AC:

1. Cashier can scan or paste barcode and product appears in cart with name, price, SKU, tax class.

2. Manual add UI accepts SKU or product name and shows suggestions.

3. Invalid SKU shows error and prevents add.

Priority: High — SP: 5 — Sprint 1


US-02 — Manage Cart & Quantities

Description: As a cashier, I want to maintain a cart with multiple items and quantities so I can handle multi-item orders.

AC:

1. Update quantity increments/decrements update subtotal instantly.

2. Remove item updates totals and UI.

3. Cart persists locally (session) until checkout completes.

Priority: High — SP: 3 — Sprint 1


US-03 — Tax & Discount Calculation

Description: As a cashier, I want automatic calculation of subtotal, discounts, and taxes so customers see accurate totals.

AC:

1. Item-level and order-level discounts supported.

2. Tax rules applied per item tax class; totals match business rules.

3. Calculations visible in UI and matching API responses.

Priority: Highest — SP: 8 — Sprint 1


US-04 — Stock Validation Before Checkout

Description: As a cashier, I want stock validated before checkout so I don’t sell out-of-stock items.

AC:

1. Checkout blocked if requested quantity > available stock.

2. On checkout success, stock is reduced in DB (transactional).

Priority: High — SP: 5 — Sprint 1


US-05 — Mock Payment Processing

Description: As a cashier, I want to process mock payments (cash, card, UPI) to complete sales.

AC:

1. Payment API accepts payment type and returns success/failure.

2. On success, sale is recorded and receipt generated.

3. On failure, rollback sale and show error to user.

Priority: Highest — SP: 8 — Sprint 1


US-06 — PDF Receipt Generation & Sale Recording

Description: As a cashier, I want to generate PDF receipt and record sale in DB so customers get proof of purchase.

AC:

1. On payment success, DB stores transaction with unique txn_id and line items.

2. PDF receipt generated and downloadable/printable with txn_id and store metadata.

Priority: Medium — SP: 5 — Sprint 1


---

### Sprint 2 (Admin / Manager / Security) — US-07 to US-14

US-07 — Refund & Void Transactions

Description: As a manager, I want to perform refunds and voids to correct erroneous sales.

AC:

1. Refund references original transaction id and updates DB.

2. Refund triggers inventory restock.

3. Access restricted to Manager role.

Priority: Medium — SP: 8 — Sprint 2


US-08 — Manager Override for Restricted Actions

Description: As a manager, I want to authorize restricted actions (e.g., large discounts).

AC:

1. System prompts for manager credential when restricted action attempted.

2. Action logs user id and timestamp.

Priority: Low — SP: 5 — Sprint 2


US-09 — Automatic Inventory Update

Description: As an admin, I want inventory updated after sale/refund to keep stock accurate.

AC:

1. Inventory read/write transactional behavior verified with tests.

2. API endpoints for inventory adjustment exist for admin.

Priority: High — SP: 5 — Sprint 2


US-10 — Reports & Sales History Search

Description: As a manager, I want daily reports and sales search to review performance.

AC:

1. Generate CSV and PDF reports by date range, cashier, and product.

2. Search API returns transactions filtered by date, cashier, amount.

Priority: Low — SP: 8 — Sprint 2


US-11 — Role-Based Access Control

Description: As an admin, I want RBAC to ensure only authorized actions are allowed.

AC:

1. Roles: Cashier, Manager, Admin. Each has permissions matrix.

2. APIs enforce permission checks; UI hides restricted actions.

Priority: High — SP: 5 — Sprint 2


US-12 — Secure Login & Credential Encryption

Description: As an admin, I want secure login, encrypted credentials, and logging of failed attempts.

AC:

1. Passwords hashed (bcrypt) in DB, login returns JWT.

2. Failed attempts logged; 5 fails -> lockout (configurable).

Priority: Highest — SP: 8 — Sprint 2


US-13 — Fast Checkout & Data Consistency

Description: As a cashier, I want fast and consistent checkout.

AC:

1. 90% of checkout ops < 2s under dev/staging load.

2. No data inconsistency across 100 scripted transactions.

Priority: High — SP: 5 — Sprint 2


US-14 — Simple & Intuitive UI

Description: As a cashier, I want a simple UI with tooltips.

AC:

1. Tooltips available for all key actions; UI passes basic usability test.

2. Accessibility checks basic (keyboard navigation, labels).

Priority: Medium — SP: 3 — Sprint 2


---

## 4. Developer tasks & subtasks (per story) — template

For each story, create these subtasks:

- Dev: implement feature (API + DB + frontend)
- Unit tests: add unit tests for business logic
- Integration tests: endpoint-level tests
- E2E/test script: Playwright or Cypress (optional)
- Code review / PR: create PR with description, link story
- Documentation: update README + API docs
- Demo: short screen recording or screenshots for acceptance


---

## 5. Database design (Postgres) — tables & fields (normalized)

Tables (minimal)

1. users

- id (uuid, pk)
- username (varchar, unique)
- password_hash (varchar)
- display_name (varchar)
- role (enum: cashier, manager, admin)
- created_at, updated_at


2. products

- id (uuid, pk)
- sku (varchar, unique)
- name (varchar)
- description (text)
- price_cents (int) — store in cents
- tax_rate (decimal) — e.g., 0.12
- stock_qty (int)
- created_at, updated_at


3. transactions

- id (uuid, pk)
- txn_ref (varchar) — human-friendly
- cashier_id (uuid -> users.id)
- total_amount_cents (int)
- payment_type (enum: cash, card, upi)
- payment_status (enum: pending, success, failed, refunded)
- created_at, updated_at


4. transaction_items

- id (uuid, pk)
- txn_id (uuid -> transactions.id)
- product_id (uuid -> products.id)
- unit_price_cents (int)
- quantity (int)
- discount_cents (int)
- tax_cents (int)


5. refunds

- id (uuid)
- txn_id (uuid -> transactions.id)
- amount_cents (int)
- refunded_by (uuid -> users.id)
- reason (text)
- created_at


6. audit_logs

- id (uuid)
- user_id (uuid)
- action (varchar)
- details (jsonb)
- created_at


7. settings (optional)

- key, value (for tax config, lockout thresholds)


Notes

- Use integer cents to avoid float issues.
- Put consistent indices on sku, txn_ref, created_at, and product_id.


---

## 6. Backend API contract (REST) — minimal endpoints (OpenAPI style)

Auth

- POST /api/auth/login
  - body: { "username": "string", "password": "string" }
  - returns: { "accessToken": "jwt", "refreshToken": "...", "user": { id, username, role } }

- POST /api/auth/refresh
  - body: { "refreshToken": "..." } → returns new access token


Products

- GET /api/products — query params ?q=&limit=&offset= → list
- GET /api/products/:id
- POST /api/products — admin only (create product)
- PUT /api/products/:id — admin
- PATCH /api/products/:id/stock — adjust stock (body: {delta: int})


Cart / Transactions

- POST /api/transactions/quote — optional, returns calculated totals & tax for cart payload
  - body: { items: [{ productId, qty, discountCents? }] }

- POST /api/transactions — create and process payment
  - body: { cart: [...], payment: { type: "cash" | "card" | "upi", amountCents } }
  - response: { txnId, paymentStatus, receiptUrl }

- GET /api/transactions/:id — get transaction + items
- GET /api/transactions — admin/manager list with filters ?from=&to=&cashierId=&productId=


Refunds

- POST /api/transactions/:id/refund — manager only
  - body: { amountCents, reason }


Reports

- GET /api/reports/sales?from=&to=&format=csv|pdf — manager only


Users

- GET /api/users — admin (list)
- POST /api/users — create user (admin)
- PATCH /api/users/:id/role — update role


Admin / Misc

- GET /api/health
- GET /api/settings / PATCH /api/settings


---

## 7. Backend implementation notes (behavioural)

All monetary operations use DB transactions. When creating a transaction:

1. Start DB transaction.
2. Validate stock for each item.
3. Reserve/decrement stock.
4. Persist transactions and transaction_items.
5. Process payment (mock) — if failed, rollback DB transaction and restore stock.
6. On success, commit and return receipt link.


Use optimistic locking or serializable isolation to avoid race conditions on stock.

Log critical operations to audit_logs.


---

## 8. Frontend design / components & pages

Main screens

- Login page
- Cashier dashboard
- Barcode input + manual search
- Cart pane (list line items, qty controls)
- Pricing summary (subtotal, discounts, tax, total)
- Payment pane (select payment type, process)
- Quick actions: hold cart, recall cart (optional)

- Receipt viewer (PDF preview)
- Manager dashboard
- Refund flow (search transaction by txn id)
- Reports page (date filters, export)

- Admin page
- Product list + edit
- User management + roles


UI components

- ProductSearch (autocomplete)
- CartItem (quantity controls, remove)
- SummaryBox (totals)
- PaymentModal
- Toast notifications & confirmation modals
- ProtectedRoute wrapper to enforce RBAC


Wireframe notes

- Cashier screen: left 60% product/search & result; right 40% cart & checkout widget.
- Big buttons for payment types; keyboard shortcuts (F1 = search, F2 = toggle payment).
- Tooltips: show for each control; small help overlay.


---

## 9. Example JSON flows

Cart request (quote):

{
  "items": [
    { "productId": "uuid-1", "quantity": 2 },
    { "productId": "uuid-2", "quantity": 1, "discountCents": 200 }
  ]
}

Transaction response:

{
  "txnId": "uuid-abc-123",
  "paymentStatus": "success",
  "receiptUrl": "/receipts/uuid-abc-123.pdf"
}


---

## 10. CI / CD — GitHub Actions example (basic)

Create .github/workflows/ci.yml (YAML outline):

name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: pos_app_test
        ports: ['5432:5432']
        options: >-
          --health-cmd "pg_isready -U postgres" --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Install deps
        run: |
          npm ci
      - name: Run backend tests
        run: |
          cd backend
          npm test
      - name: Run frontend tests
        run: |
          cd frontend
          npm test -- --watchAll=false
  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: |
          cd frontend && npm run build
          cd ../backend && npm run build

Add a deploy job only if your CI environment and secrets are ready.


---

## 11. Docker / docker-compose (dev)

docker-compose.yml skeleton:

version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: pos_db
    volumes:
      - db_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  backend:
    build: ./backend
    env_file: ./backend/.env.dev
    depends_on:
      - db
    ports:
      - "4000:4000"
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
volumes:
  db_data:7
