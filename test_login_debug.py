import sqlite3
import sys
import os

# Check database
db_path = 'database/pos.db'
if not os.path.exists(db_path):
    print(f"ERROR: Database not found at {db_path}")
    sys.exit(1)

print(f"✓ Database found at {db_path}\n")

# Check users
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute('SELECT id, username, role, is_active FROM users')
users = cursor.fetchall()

print("Users in database:")
for user in users:
    print(f"  ID: {user[0]}, Username: {user[1]}, Role: {user[2]}, Active: {user[3]}")

if not users:
    print("\n⚠️ WARNING: No users in database! Run: python backend/init_db.py")
else:
    print(f"\n✓ Found {len(users)} users")

# Test login with admin credentials
print("\n" + "="*50)
print("Testing login logic...")
print("="*50)

cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = 'admin'")
admin = cursor.fetchone()

if admin:
    print(f"\n✓ Found admin user: {admin[1]} (role: {admin[3]})")
    print(f"  Password hash exists: {bool(admin[2])}")
    
    # Test password verification
    from werkzeug.security import check_password_hash
    password = 'admin123'
    is_valid = check_password_hash(admin[2], password)
    print(f"  Password 'admin123' valid: {is_valid}")
    
    if not is_valid:
        print("\n⚠️ WARNING: Password verification failed!")
        print("  This means the password hash is incorrect.")
        print("  Run: cd backend && python -m utils.db")
else:
    print("\n❌ Admin user not found!")

conn.close()

# Test API endpoint
print("\n" + "="*50)
print("Testing API endpoint...")
print("="*50)

import requests
import json

try:
    response = requests.post(
        'http://localhost:5000/api/auth/login',
        json={'username': 'admin', 'password': 'admin123'},
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"\nAPI Response Status: {response.status_code}")
    print(f"API Response Body: {response.text}")
    
    if response.status_code == 200:
        print("\n✅ LOGIN SUCCESS!")
    else:
        print("\n❌ LOGIN FAILED")
        
except requests.exceptions.ConnectionError:
    print("\n⚠️ Cannot connect to backend at http://localhost:5000")
    print("  Make sure the backend is running: cd backend && python app.py")
except Exception as e:
    print(f"\n❌ Error: {e}")
