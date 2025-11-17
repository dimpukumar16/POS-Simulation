# POS Simulator - API Documentation

## Base URL
```
http://localhost:5000/api
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Authentication Endpoints

### POST /auth/login
Login with username/password or PIN.

**Request Body:**
```json
{
  "username": "cashier",
  "password": "cashier123",
  "pin": "3333"  // Optional, alternative to password
}
```

**Response (200):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 3,
    "username": "cashier",
    "role": "cashier",
    "full_name": "John Cashier",
    "email": "cashier@pos.com"
  }
}
```

### POST /auth/verify-pin
Verify manager PIN for override operations.

**Request Body:**
```json
{
  "pin": "2222",
  "action": "Process refund"
}
```

**Response (200):**
```json
{
  "authorized": true,
  "override_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "authorizer": { /* user object */ }
}
```

### POST /auth/logout
Logout current user.

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

### GET /auth/me
Get current user information.

**Response (200):**
```json
{
  "user": { /* user object */ }
}
```

---

## Product Endpoints

### GET /products
Get all products with optional filtering.

**Query Parameters:**
- `category` (optional): Filter by category
- `active` (optional, default: true): Show only active products
- `search` (optional): Search by name, barcode, or description
- `low_stock` (optional): Show only low stock items

**Response (200):**
```json
{
  "products": [
    {
      "id": 1,
      "barcode": "1234567890",
      "name": "Laptop - Dell XPS 13",
      "price": 999.99,
      "stock_quantity": 25,
      "tax_rate": 0.18,
      "needs_reorder": false
    }
  ],
  "count": 1
}
```

### GET /products/{barcode}
Get product by barcode.

**Response (200):**
```json
{
  "product": { /* product object */ }
}
```

### POST /products
Create new product (Admin/Manager only).

**Request Body:**
```json
{
  "barcode": "NEW12345",
  "name": "New Product",
  "description": "Product description",
  "category": "Electronics",
  "price": 99.99,
  "cost": 60.00,
  "stock_quantity": 50,
  "reorder_level": 10,
  "tax_rate": 0.18
}
```

**Response (201):**
```json
{
  "message": "Product created successfully",
  "product": { /* product object */ }
}
```

### PUT /products/{product_id}
Update product (Admin/Manager only).

### DELETE /products/{product_id}
Delete product (Admin only). This is a soft delete.

---

## Cart Endpoints

### GET /cart
Get current user's cart.

**Response (200):**
```json
{
  "cart": {
    "items": [
      {
        "cart_item_id": 1,
        "product_id": 1,
        "name": "Laptop - Dell XPS 13",
        "unit_price": 999.99,
        "quantity": 2,
        "tax_amount": 359.99,
        "line_total": 2359.98
      }
    ],
    "subtotal": 1999.98,
    "discount_amount": 0,
    "tax_amount": 359.99,
    "total": 2359.97,
    "item_count": 1
  }
}
```

### POST /cart/add
Add item to cart.

**Request Body:**
```json
{
  "barcode": "1234567890",  // OR "product_id": 1
  "quantity": 2
}
```

**Response (200):**
```json
{
  "message": "Item added to cart",
  "cart": { /* cart object */ }
}
```

### PUT /cart/update
Update cart item quantity.

**Request Body:**
```json
{
  "cart_item_id": 1,
  "quantity": 5
}
```

### DELETE /cart/remove/{cart_item_id}
Remove item from cart.

### POST /cart/discount
Apply discount to cart.

**Request Body:**
```json
{
  "type": "percentage",  // or "fixed"
  "amount": 10,
  "manager_override": true  // Required for discounts > 20%
}
```

### DELETE /cart/clear
Clear all items from cart.

---

## Checkout Endpoints

### POST /checkout/process
Process payment and complete checkout.

**Request Body:**
```json
{
  "payment_method": "cash",  // "cash", "card", or "upi"
  "amount_paid": 50.00,
  "payment_reference": "optional-reference"
}
```

**Response (200):**
```json
{
  "message": "Payment successful",
  "transaction": {
    "id": 1,
    "transaction_number": "TXN-20251014120000",
    "status": "completed",
    "total_amount": 45.50,
    "payment_method": "cash",
    "change_given": 4.50
  },
  "payment_result": {
    "success": true,
    "status": "approved",
    "reference": "CASH-20251014120000-123456"
  },
  "receipt_path": "receipts/receipt_TXN-20251014120000.pdf"
}
```

### POST /checkout/refund
Process refund (Manager authorization required).

**Request Body:**
```json
{
  "transaction_id": 1,
  "reason": "Customer requested refund",
  "manager_pin": "2222"
}
```

**Response (200):**
```json
{
  "message": "Refund processed successfully",
  "refund_transaction": { /* transaction object */ },
  "refund_result": { /* payment result */ }
}
```

### POST /checkout/void
Void a transaction (Manager authorization required).

**Request Body:**
```json
{
  "transaction_id": 1,
  "reason": "Transaction error",
  "manager_pin": "2222"
}
```

---

## Report Endpoints

### GET /reports/sales
Generate sales report.

**Query Parameters:**
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `cashier_id` (optional): Filter by cashier
- `category` (optional): Filter by product category

**Response (200):**
```json
{
  "report": {
    "period": {
      "start": "2025-01-01T00:00:00",
      "end": "2025-12-31T23:59:59"
    },
    "summary": {
      "total_transactions": 150,
      "sales_count": 145,
      "refunds_count": 5,
      "total_sales": 15000.50,
      "total_refunds": 250.00,
      "net_sales": 14750.50,
      "average_transaction": 103.45
    },
    "payment_methods": {
      "cash": { "count": 50, "total": 5000.00 },
      "card": { "count": 60, "total": 6500.00 },
      "upi": { "count": 35, "total": 3500.50 }
    },
    "top_products": [ /* array of products */ ],
    "cashier_performance": [ /* array of cashier stats */ ]
  }
}
```

### GET /reports/inventory
Generate inventory report.

**Query Parameters:**
- `category` (optional): Filter by category
- `low_stock` (optional): Show only low stock items

**Response (200):**
```json
{
  "report": {
    "summary": {
      "total_products": 100,
      "total_inventory_value": 50000.00,
      "low_stock_items": 5,
      "out_of_stock_items": 2
    },
    "categories": { /* category breakdown */ },
    "products": [ /* array of products */ ]
  }
}
```

### GET /reports/history
Get sales history with search and filtering.

**Query Parameters:**
- `search` (optional): Search transaction number or product name
- `start_date` (optional): YYYY-MM-DD
- `end_date` (optional): YYYY-MM-DD
- `status` (optional): Filter by status
- `limit` (optional, default: 50): Number of results
- `offset` (optional, default: 0): Pagination offset

**Response (200):**
```json
{
  "transactions": [ /* array of transactions */ ],
  "pagination": {
    "total": 150,
    "limit": 50,
    "offset": 0,
    "has_more": true
  }
}
```

### POST /reports/export
Export report as PDF or CSV.

**Request Body:**
```json
{
  "report_type": "sales",  // or "inventory"
  "format": "pdf",  // or "csv"
  "start_date": "2025-01-01",
  "end_date": "2025-12-31"
}
```

**Response (200):**
```json
{
  "message": "Report generated",
  "filepath": "receipts/sales_report_20251014_120000.pdf"
}
```

### GET /reports/audit-log
Get audit log entries (Admin/Manager only).

**Query Parameters:**
- `limit` (optional, default: 100): Number of results
- `user_id` (optional): Filter by user
- `action` (optional): Filter by action type

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Missing required field: barcode"
}
```

### 401 Unauthorized
```json
{
  "error": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
  "error": "Insufficient privileges"
}
```

### 404 Not Found
```json
{
  "error": "Product not found"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, consider implementing rate limiting for security.

## Pagination

For endpoints that return large datasets (like `/reports/history`), use the `limit` and `offset` parameters for pagination.

---

## Testing

Use the included test suite or tools like Postman, curl, or Insomnia to test the API.

**Run tests:**
```bash
cd backend
pytest tests/ -v
```

---

## Security Notes

1. **Always use HTTPS in production**
2. **Change default secret keys**
3. **Implement rate limiting**
4. **Regular security audits**
5. **Keep dependencies updated**

---

For more information, see:
- `SETUP_GUIDE.md` - Complete setup instructions
- `RTM.csv` - Requirements traceability matrix
- `README.md` - Project overview
