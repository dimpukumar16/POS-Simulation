"""
Quick validation script to check new features
Run this after starting the backend to verify everything works
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_login():
    """Test login with refresh token"""
    print("🔐 Testing Login...")
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": "manager",
        "password": "manager123"
    })
    if response.status_code == 200:
        data = response.json()
        print("✅ Login successful")
        print(f"   Access Token: {data['access_token'][:20]}...")
        print(f"   Refresh Token: {data.get('refresh_token', 'N/A')[:20]}...")
        return data
    else:
        print(f"❌ Login failed: {response.text}")
        return None

def test_refresh_token(refresh_token):
    """Test refresh token endpoint"""
    print("\n🔄 Testing Refresh Token...")
    response = requests.post(f"{BASE_URL}/auth/refresh", json={
        "refresh_token": refresh_token
    })
    if response.status_code == 200:
        print("✅ Token refresh successful")
        return response.json()
    else:
        print(f"❌ Token refresh failed: {response.text}")
        return None

def test_settings(token):
    """Test settings endpoint"""
    print("\n⚙️  Testing Settings...")
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all settings
    response = requests.get(f"{BASE_URL}/settings", headers=headers)
    if response.status_code == 200:
        settings = response.json()
        print(f"✅ Retrieved {settings.get('count', 0)} settings")
        for setting in settings.get('settings', [])[:3]:
            print(f"   - {setting['key']}: {setting['value']}")
    else:
        print(f"❌ Get settings failed: {response.text}")

def test_verify_pin(token):
    """Test manager PIN verification"""
    print("\n🔑 Testing Manager PIN Verification...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/auth/verify-pin", 
        headers=headers,
        json={"pin": "2222", "action": "Test override action"}
    )
    if response.status_code == 200:
        print("✅ PIN verification successful")
        return response.json()
    else:
        print(f"❌ PIN verification failed: {response.text}")
        return None

def test_refunds_api(token):
    """Test refunds API (read-only)"""
    print("\n💰 Testing Refunds API...")
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{BASE_URL}/refunds", headers=headers)
    if response.status_code == 200:
        refunds = response.json()
        print(f"✅ Retrieved {refunds.get('count', 0)} refunds")
    else:
        print(f"❌ Get refunds failed: {response.text}")

def test_health():
    """Test health endpoint"""
    print("\n🏥 Testing Health Endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        print(f"   {response.json()}")
    else:
        print(f"❌ Health check failed")

def main():
    print("=" * 60)
    print("POS Simulator - New Features Validation")
    print("=" * 60)
    
    # Test health first
    test_health()
    
    # Test login
    login_data = test_login()
    if not login_data:
        print("\n⚠️  Cannot continue without login. Please check backend.")
        return
    
    access_token = login_data.get('access_token')
    refresh_token = login_data.get('refresh_token')
    
    # Test refresh token
    if refresh_token:
        test_refresh_token(refresh_token)
    
    # Test settings
    test_settings(access_token)
    
    # Test PIN verification
    test_verify_pin(access_token)
    
    # Test refunds API
    test_refunds_api(access_token)
    
    print("\n" + "=" * 60)
    print("✅ All validation tests completed!")
    print("=" * 60)
    print("\n📝 Next steps:")
    print("   1. Start frontend: cd frontend && npm run dev")
    print("   2. Open browser: http://localhost:5173")
    print("   3. Login as manager: manager / manager123")
    print("   4. Test Refunds page in the UI")
    print("   5. Test manager override functionality")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to backend.")
        print("   Please start the backend first:")
        print("   cd backend && python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
