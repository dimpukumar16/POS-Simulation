# POS Simulator - Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### Issue: "python is not recognized"
**Solution:**
1. Install Python from https://www.python.org/
2. During installation, check "Add Python to PATH"
3. Restart your terminal/PowerShell
4. Verify: `python --version`

#### Issue: "cannot be loaded because running scripts is disabled"
**Problem:** PowerShell execution policy prevents script execution

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Issue: "pip install fails with permission error"
**Solution:**
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\Activate.ps1

# If still failing, try:
pip install -r requirements.txt --user
```

#### Issue: "Module not found" errors when running app
**Solution:**
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

### Database Issues

#### Issue: "Database is locked"
**Solution:**
1. Close all applications accessing the database
2. Delete the database file: `database/pos.db`
3. Reinitialize: `python -m utils.db`

#### Issue: "No such table" errors
**Solution:**
```powershell
cd backend
# Reset database
python -c "from utils.db import reset_database; from app import app; reset_database(app)"
```

#### Issue: "Integrity constraint violation"
**Solution:**
- Check for duplicate barcodes when creating products
- Ensure referenced IDs exist (user_id, product_id, etc.)
- Reset database if corrupted (see above)

---

### Authentication Issues

#### Issue: "Invalid credentials" but password is correct
**Solution:**
1. Check if account is locked (5 failed attempts)
2. Check database for user:
```python
from app import app
from models.user import db, User
with app.app_context():
    user = User.query.filter_by(username='cashier').first()
    print(f"Active: {user.is_active}, Failed attempts: {user.failed_login_attempts}")
```

3. Reset user:
```python
user.is_active = True
user.failed_login_attempts = 0
db.session.commit()
```

#### Issue: "Token has expired"
**Solution:**
- Login again to get a new token
- Tokens expire after 8 hours by default
- Update JWT_ACCESS_TOKEN_EXPIRES in app.py if needed

#### Issue: "Authorization token is missing"
**Solution:**
- Ensure you're including the Authorization header:
```
Authorization: Bearer <your-token-here>
```

---

### API Issues

#### Issue: "Connection refused" or "Cannot connect to server"
**Solution:**
1. Verify server is running: `http://localhost:5000/health`
2. Check if port 5000 is in use by another application
3. Change port in app.py or via environment variable:
```powershell
$env:PORT = "5001"
python app.py
```

#### Issue: "404 Not Found" for all endpoints
**Solution:**
- Check if you're using the correct base URL: `http://localhost:5000/api/`
- Verify server started without errors
- Check Flask output for registered blueprints

#### Issue: "CORS errors" when testing from browser
**Solution:**
- CORS is already configured in app.py
- If still having issues, verify CORS settings:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

---

### Payment Issues

#### Issue: "Payment always fails"
**Solution:**
- Mock payment has realistic failure rates
- Card payments: 95% success rate
- UPI payments: 92% success rate
- Try multiple times or use cash (100% success)

#### Issue: "Insufficient stock" error
**Solution:**
1. Check product stock:
```http
GET http://localhost:5000/api/products/{barcode}
```

2. Update stock if needed:
```http
PUT http://localhost:5000/api/products/{id}
{
  "stock_quantity": 100
}
```

#### Issue: "Cart is empty" when trying to checkout
**Solution:**
- Add items to cart first:
```http
POST http://localhost:5000/api/cart/add
{
  "barcode": "1234567890",
  "quantity": 1
}
```

---

### Receipt Generation Issues

#### Issue: "Receipt PDF not generated"
**Solution:**
1. Check if receipts folder exists: `mkdir receipts`
2. Verify ReportLab is installed: `pip install reportlab`
3. Check write permissions on receipts folder
4. Review server logs for PDF generation errors

#### Issue: "Cannot open PDF file"
**Solution:**
- Install a PDF reader (Adobe Reader, Edge, Chrome)
- Check file path in server response
- File is saved as: `receipts/receipt_{transaction_number}.pdf`

---

### Testing Issues

#### Issue: "No module named 'pytest'"
**Solution:**
```powershell
pip install pytest pytest-flask pytest-cov
```

#### Issue: "Tests fail with database errors"
**Solution:**
- Tests use in-memory database (SQLite :memory:)
- Ensure test fixtures are properly set up
- Check if models are imported correctly in test files

#### Issue: "Import errors in tests"
**Solution:**
```python
# Add this at the top of test files
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
```

---

### Performance Issues

#### Issue: "Slow API responses"
**Solution:**
1. Check database size: `dir database\pos.db`
2. If large, consider:
   - Adding database indexes
   - Implementing query optimization
   - Using pagination for large datasets

#### Issue: "High memory usage"
**Solution:**
- Clear cart storage periodically
- Implement cart expiration
- Use Redis for cart storage in production

---

### Data Issues

#### Issue: "No products in database"
**Solution:**
```powershell
cd backend
# Reseed database
python -m utils.db
```

#### Issue: "Want to add more test data"
**Solution:**
```powershell
cd backend
python tests/generate_test_data.py
# Follow prompts to generate users, products, transactions
```

#### Issue: "Database is corrupted"
**Solution:**
```powershell
cd backend
# Backup first (if needed)
Copy-Item database/pos.db database/pos.db.backup

# Reset database
python -c "from utils.db import reset_database; from app import app; reset_database(app)"
```

---

### Frontend Issues (When Implemented)

#### Issue: "npm install fails"
**Solution:**
1. Ensure Node.js is installed: `node --version`
2. Clear npm cache: `npm cache clean --force`
3. Delete node_modules and package-lock.json
4. Run `npm install` again

#### Issue: "Cannot connect to backend"
**Solution:**
- Check backend is running: `http://localhost:5000/health`
- Verify API URL in frontend config
- Check CORS settings in backend

---

### Development Issues

#### Issue: "Changes not reflecting"
**Solution:**
- Restart the Flask server (Ctrl+C, then `python app.py`)
- Flask auto-reload should work in debug mode
- Clear browser cache for frontend changes

#### Issue: "Import errors after adding new files"
**Solution:**
- Ensure `__init__.py` files exist if needed
- Check Python path configuration
- Restart Python interpreter/server

---

## Debugging Tips

### Enable Debug Mode
```python
# In app.py
app.run(debug=True)
```

### Check Server Logs
Look at the terminal where `python app.py` is running for error messages.

### Test Individual Components

**Test Database Connection:**
```python
from app import app
from models.user import db
with app.app_context():
    db.session.execute('SELECT 1')
    print("Database OK")
```

**Test User Creation:**
```python
from app import app
from models.user import db, User
with app.app_context():
    user = User.query.first()
    print(f"Found user: {user.username if user else 'None'}")
```

**Test Product Query:**
```python
from app import app
from models.product import Product
with app.app_context():
    products = Product.query.all()
    print(f"Found {len(products)} products")
```

### Use Python Interactive Shell
```powershell
cd backend
python
>>> from app import app
>>> with app.app_context():
...     from models.user import User
...     users = User.query.all()
...     for u in users: print(u.username, u.role)
```

---

## Getting Help

### Check Documentation
1. `README.md` - Project overview
2. `SETUP_GUIDE.md` - Installation steps
3. `API_DOCUMENTATION.md` - API reference
4. `RTM.csv` - Requirements mapping

### Check Test Files
Test files in `backend/tests/` show working examples of API usage.

### Health Check
```http
GET http://localhost:5000/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "healthy"
}
```

---

## Reset Everything

If all else fails, complete reset:

```powershell
# Stop server (Ctrl+C)

# Delete virtual environment
Remove-Item -Recurse -Force venv

# Delete database
Remove-Item -Recurse -Force database

# Start fresh
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd backend
python -m utils.db
python app.py
```

---

## Still Having Issues?

1. **Check error messages carefully** - They usually indicate the problem
2. **Review recent changes** - What changed before it broke?
3. **Check file paths** - Ensure you're in the correct directory
4. **Verify dependencies** - All packages installed correctly?
5. **Test with curl/Postman** - Isolate if it's a client issue

---

## Quick Diagnostic Commands

```powershell
# Check Python
python --version

# Check pip
pip --version

# Check installed packages
pip list

# Check virtual environment
python -c "import sys; print(sys.prefix)"

# Test Flask app
cd backend
python -c "from app import app; print('Flask app OK')"

# Test database
python -c "from app import app; from models.user import db; app.app_context().push(); db.session.execute('SELECT 1'); print('Database OK')"

# Check server accessibility
Invoke-WebRequest -Uri "http://localhost:5000/health"
```

---

**Remember:** Most issues are related to:
1. Virtual environment not activated
2. Dependencies not installed
3. Database not initialized
4. Port conflicts
5. Missing authorization tokens

Check these first!
