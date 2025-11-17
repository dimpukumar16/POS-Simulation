# POS Simulator API Test Script
# Run this script to test all major API endpoints

Write-Host "`n========================================"
Write-Host "  POS Simulator API Test Suite"
Write-Host "========================================`n"

$baseUrl = "http://localhost:5000"
$ErrorActionPreference = "Stop"

# Test 1: Root endpoint
Write-Host "[1/7] Testing root endpoint..."
try {
    $root = Invoke-RestMethod -Uri "$baseUrl/" -Method GET
    Write-Host "  [SUCCESS] Root endpoint working"
    Write-Host "    Version: $($root.version)"
} catch {
    Write-Host "  [FAILED] Root endpoint failed"
    Write-Host "    Make sure the server is running!"
    exit 1
}

# Test 2: Health check
Write-Host "`n[2/7] Testing health endpoint..."
try {
    $health = Invoke-RestMethod -Uri "$baseUrl/health" -Method GET
    Write-Host "  [SUCCESS] Health: $($health.status)"
    Write-Host "    Database: $($health.database)"
} catch {
    Write-Host "  [FAILED] Health check failed: $_"
}

# Test 3: Login
Write-Host "`n[3/7] Testing login (admin)..."
try {
    $loginBody = @{
        username = "admin"
        password = "admin123"
    } | ConvertTo-Json

    $login = Invoke-RestMethod -Uri "$baseUrl/api/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
    $token = $login.access_token
    Write-Host "  [SUCCESS] Login successful"
    Write-Host "    User: $($login.user.username)"
    Write-Host "    Role: $($login.user.role)"
    Write-Host "    Email: $($login.user.email)"
} catch {
    Write-Host "  [FAILED] Login failed: $_"
    Write-Host "`nStopping tests - authentication required"
    exit 1
}

# Test 4: Get products
Write-Host "`n[4/7] Testing product listing..."
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    $products = Invoke-RestMethod -Uri "$baseUrl/api/products" -Method GET -Headers $headers
    Write-Host "  [SUCCESS] Retrieved $($products.count) products"
    
    if ($products.count -gt 0) {
        Write-Host "`n  Product List:"
        $products.products | Select-Object -First 5 | ForEach-Object {
            Write-Host "    - $($_.name): `$$($_.price) (Stock: $($_.stock_quantity))"
        }
    }
} catch {
    Write-Host "  [FAILED] Get products failed: $_"
}

# Test 5: Get cart
Write-Host "`n[5/7] Testing cart retrieval..."
try {
    $headers = @{
        "Authorization" = "Bearer $token"
    }
    $cart = Invoke-RestMethod -Uri "$baseUrl/api/cart" -Method GET -Headers $headers
    Write-Host "  [SUCCESS] Cart retrieved"
    Write-Host "    Items: $($cart.cart.item_count)"
    Write-Host "    Total: `$$($cart.cart.total)"
} catch {
    Write-Host "  [FAILED] Get cart failed: $_"
}

# Test 6: Add item to cart
Write-Host "`n[6/7] Testing add to cart..."
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $firstProduct = $products.products[0]
    
    $addBody = @{
        product_id = $firstProduct.id
        quantity = 2
    } | ConvertTo-Json

    $addResult = Invoke-RestMethod -Uri "$baseUrl/api/cart/add" -Method POST -Body $addBody -Headers $headers
    Write-Host "  [SUCCESS] Item added to cart"
    Write-Host "    Product: $($firstProduct.name)"
    Write-Host "    Quantity: 2"
    Write-Host "    Cart total: `$$($addResult.cart.total)"
} catch {
    Write-Host "  [FAILED] Add to cart failed: $_"
}

# Test 7: Complete checkout
Write-Host "`n[7/7] Testing checkout process..."
try {
    $headers = @{
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
    
    $checkoutBody = @{
        payment_method = "cash"
        amount_paid = 100.00
    } | ConvertTo-Json

    $checkout = Invoke-RestMethod -Uri "$baseUrl/api/checkout/process" -Method POST -Body $checkoutBody -Headers $headers
    Write-Host "  [SUCCESS] Checkout successful"
    Write-Host "    Transaction: $($checkout.transaction.transaction_number)"
    Write-Host "    Total: `$$($checkout.transaction.total_amount)"
    Write-Host "    Change: `$$($checkout.transaction.change_given)"
    Write-Host "    Receipt: $($checkout.receipt_path)"
} catch {
    Write-Host "  [FAILED] Checkout failed: $_"
}

# Summary
Write-Host "`n========================================"
Write-Host "  Test Suite Complete!"
Write-Host "========================================`n"
Write-Host "POS Simulator API is operational!`n"
Write-Host "Next steps:"
Write-Host "  - View API docs: API_DOCUMENTATION.md"
Write-Host "  - Run unit tests: pytest tests/ -v"
Write-Host "  - Build frontend UI"
Write-Host ""
