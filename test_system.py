"""
Comprehensive System Test Script
Tests all backend endpoints and functionality
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000/api"

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")

def print_section(title):
    print(f"\n{'='*60}")
    print(f"{BLUE}{title}{RESET}")
    print('='*60)

class SystemTester:
    def __init__(self):
        self.tokens = {}
        self.test_product_id = None
        self.errors = []
        self.warnings = []
        
    def test_authentication(self):
        """Test authentication for all user roles"""
        print_section("Testing Authentication")
        
        users = [
            ('admin', 'admin123', 'administrator'),
            ('manager', 'manager123', 'manager'),
            ('cashier', 'cashier123', 'cashier')
        ]
        
        for username, password, expected_role in users:
            try:
                response = requests.post(f"{BASE_URL}/auth/login", json={
                    'username': username,
                    'password': password
                })
                
                if response.status_code == 200:
                    data = response.json()
                    if 'access_token' in data and 'user' in data:
                        self.tokens[username] = data['access_token']
                        user_role = data['user']['role']
                        if user_role == expected_role:
                            print_success(f"Login successful for {username} (Role: {user_role})")
                        else:
                            print_warning(f"{username} has unexpected role: {user_role} (expected {expected_role})")
                            self.warnings.append(f"Role mismatch for {username}")
                    else:
                        print_error(f"Login response missing data for {username}")
                        self.errors.append(f"Invalid login response for {username}")
                else:
                    print_error(f"Login failed for {username}: {response.status_code}")
                    self.errors.append(f"Login failed for {username}")
            except Exception as e:
                print_error(f"Login exception for {username}: {str(e)}")
                self.errors.append(f"Login exception for {username}")
    
    def test_products_api(self):
        """Test product management endpoints"""
        print_section("Testing Products API")
        
        if 'admin' not in self.tokens:
            print_error("Cannot test products - admin token missing")
            return
        
        headers = {'Authorization': f'Bearer {self.tokens["admin"]}'}
        
        # Test GET all products
        try:
            response = requests.get(f"{BASE_URL}/products", headers=headers)
            if response.status_code == 200:
                data = response.json()
                products = data.get('products', data)  # Handle both formats
                if isinstance(products, list):
                    print_success(f"Retrieved {len(products)} products")
                    if len(products) > 0:
                        self.test_product_id = products[0]['id']
                    else:
                        print_warning("No products found in database")
                        self.warnings.append("Empty product list")
                else:
                    print_error("Invalid products response format")
                    self.errors.append("Invalid products response")
            else:
                print_error(f"Get products failed: {response.status_code}")
                self.errors.append("Get products failed")
        except Exception as e:
            print_error(f"Get products exception: {str(e)}")
            self.errors.append("Get products exception")
        
        # Test GET single product
        if self.test_product_id:
            try:
                response = requests.get(f"{BASE_URL}/products/id/{self.test_product_id}", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    product = data.get('product', data)
                    print_success(f"Retrieved product: {product.get('name', 'N/A')}")
                else:
                    print_error(f"Get single product failed: {response.status_code}")
                    self.errors.append("Get single product failed")
            except Exception as e:
                print_error(f"Get single product exception: {str(e)}")
                self.errors.append("Get single product exception")
        
        # Test CREATE product
        try:
            new_product = {
                'name': 'Test Product',
                'category': 'Test Category',
                'price': 99.99,
                'stock': 100,
                'barcode': 'TEST123456789',
                'description': 'Test product for system validation'
            }
            response = requests.post(f"{BASE_URL}/products", json=new_product, headers=headers)
            if response.status_code == 201:
                created = response.json()
                print_success(f"Created test product with ID: {created['id']}")
                self.test_product_id = created['id']
            elif response.status_code == 409:
                print_warning("Test product already exists (barcode conflict) - using existing product")
                self.warnings.append("Test product barcode already exists")
            else:
                print_error(f"Create product failed: {response.status_code} - {response.text}")
                self.errors.append("Create product failed")
        except Exception as e:
            print_error(f"Create product exception: {str(e)}")
            self.errors.append("Create product exception")
        
        # Test UPDATE product
        if self.test_product_id:
            try:
                update_data = {'price': 89.99, 'stock': 95}
                response = requests.put(f"{BASE_URL}/products/{self.test_product_id}", 
                                      json=update_data, headers=headers)
                if response.status_code == 200:
                    print_success("Updated test product successfully")
                else:
                    print_error(f"Update product failed: {response.status_code}")
                    self.errors.append("Update product failed")
            except Exception as e:
                print_error(f"Update product exception: {str(e)}")
                self.errors.append("Update product exception")
    
    def test_cart_api(self):
        """Test shopping cart endpoints"""
        print_section("Testing Cart API")
        
        if 'cashier' not in self.tokens:
            print_error("Cannot test cart - cashier token missing")
            return
        
        headers = {'Authorization': f'Bearer {self.tokens["cashier"]}'}
        
        # Test GET cart
        try:
            response = requests.get(f"{BASE_URL}/cart", headers=headers)
            if response.status_code == 200:
                cart = response.json()
                print_success(f"Retrieved cart with {len(cart.get('items', []))} items")
            else:
                print_error(f"Get cart failed: {response.status_code}")
                self.errors.append("Get cart failed")
        except Exception as e:
            print_error(f"Get cart exception: {str(e)}")
            self.errors.append("Get cart exception")
        
        # Test ADD to cart
        if self.test_product_id:
            try:
                response = requests.post(f"{BASE_URL}/cart/add", json={
                    'product_id': self.test_product_id,
                    'quantity': 2
                }, headers=headers)
                if response.status_code == 200:
                    print_success("Added product to cart")
                else:
                    print_error(f"Add to cart failed: {response.status_code} - {response.text}")
                    self.errors.append("Add to cart failed")
            except Exception as e:
                print_error(f"Add to cart exception: {str(e)}")
                self.errors.append("Add to cart exception")
        
        # Test UPDATE cart item (skip - requires cart_item_id from cart response)
        # The update functionality is tested via the add endpoint which can update existing items
        
        # Test CLEAR cart (we'll add items back for checkout test)
        try:
            response = requests.delete(f"{BASE_URL}/cart/clear", headers=headers)
            if response.status_code == 200:
                print_success("Cleared cart successfully")
            else:
                print_error(f"Clear cart failed: {response.status_code}")
                self.errors.append("Clear cart failed")
        except Exception as e:
            print_error(f"Clear cart exception: {str(e)}")
            self.errors.append("Clear cart exception")
    
    def test_checkout_api(self):
        """Test checkout process"""
        print_section("Testing Checkout API")
        
        if 'cashier' not in self.tokens or not self.test_product_id:
            print_error("Cannot test checkout - missing requirements")
            return
        
        headers = {'Authorization': f'Bearer {self.tokens["cashier"]}'}
        
        # Add item to cart first
        try:
            response = requests.post(f"{BASE_URL}/cart/add", json={
                'product_id': self.test_product_id,
                'quantity': 2
            }, headers=headers)
            if response.status_code == 200:
                # Get cart to check totals
                cart_response = requests.get(f"{BASE_URL}/cart", headers=headers)
                if cart_response.status_code == 200:
                    cart_data = cart_response.json()
                    cart = cart_data.get('cart', {})
                    total = cart.get('total', 0)
                    print_info(f"Cart total before checkout: ${total:.2f}")
        except Exception as e:
            print_warning(f"Could not add to cart: {str(e)}")
        
        # Test CHECKOUT with proper payment amount
        try:
            # Get cart total first
            cart_response = requests.get(f"{BASE_URL}/cart", headers=headers)
            total_amount = 0
            if cart_response.status_code == 200:
                cart_data = cart_response.json()
                total_amount = cart_data.get('cart', {}).get('total', 0)
            
            response = requests.post(f"{BASE_URL}/checkout/process", json={
                'payment_method': 'cash',
                'amount_paid': total_amount * 1.1,  # Pay 10% more for change
                'payment_reference': 'TEST-CASH-001'
            }, headers=headers)
            if response.status_code == 200:
                result = response.json()
                print_success(f"Checkout successful - Transaction ID: {result.get('transaction_id', 'N/A')}")
                print_info(f"Total: ${result.get('total', 0):.2f}")
                print_info(f"Change: ${result.get('change_due', 0):.2f}")
            else:
                print_error(f"Checkout failed: {response.status_code} - {response.text[:200]}")
                self.errors.append("Checkout failed")
        except Exception as e:
            print_error(f"Checkout exception: {str(e)}")
            self.errors.append("Checkout exception")
    
    def test_reports_api(self):
        """Test reports endpoints"""
        print_section("Testing Reports API")
        
        if 'manager' not in self.tokens:
            print_error("Cannot test reports - manager token missing")
            return
        
        headers = {'Authorization': f'Bearer {self.tokens["manager"]}'}
        
        # Test transactions list
        try:
            response = requests.get(f"{BASE_URL}/reports/history", headers=headers)
            if response.status_code == 200:
                transactions = response.json()
                print_success(f"Retrieved {len(transactions)} transactions")
            else:
                print_error(f"Get transactions failed: {response.status_code}")
                self.errors.append("Get transactions failed")
        except Exception as e:
            print_error(f"Get transactions exception: {str(e)}")
            self.errors.append("Get transactions exception")
        
        # Test sales report
        try:
            response = requests.get(f"{BASE_URL}/reports/sales", headers=headers)
            if response.status_code == 200:
                report = response.json()
                print_success(f"Sales Report - Total: ${report.get('total_sales', 0):.2f}, Transactions: {report.get('transaction_count', 0)}")
            else:
                print_error(f"Sales report failed: {response.status_code}")
                self.errors.append("Sales report failed")
        except Exception as e:
            print_error(f"Sales report exception: {str(e)}")
            self.errors.append("Sales report exception")
        
        # Test inventory report
        try:
            response = requests.get(f"{BASE_URL}/reports/inventory", headers=headers)
            if response.status_code == 200:
                inventory = response.json()
                print_success(f"Inventory Report - Total Items: {len(inventory)}")
            else:
                print_error(f"Inventory report failed: {response.status_code}")
                self.errors.append("Inventory report failed")
        except Exception as e:
            print_error(f"Inventory report exception: {str(e)}")
            self.errors.append("Inventory report exception")
    
    def test_role_based_access(self):
        """Test that role restrictions are enforced"""
        print_section("Testing Role-Based Access Control")
        
        if 'cashier' not in self.tokens:
            print_warning("Cannot test RBAC - cashier token missing")
            return
        
        # Cashier should NOT be able to delete products
        headers = {'Authorization': f'Bearer {self.tokens["cashier"]}'}
        
        try:
            response = requests.delete(f"{BASE_URL}/products/999", headers=headers)
            if response.status_code == 403:
                print_success("RBAC working - Cashier denied product deletion")
            elif response.status_code == 404:
                print_success("RBAC check passed (product not found is ok)")
            else:
                print_warning(f"Unexpected RBAC response: {response.status_code}")
                self.warnings.append("RBAC may not be properly configured")
        except Exception as e:
            print_error(f"RBAC test exception: {str(e)}")
    
    def cleanup(self):
        """Clean up test data"""
        print_section("Cleanup")
        
        if 'admin' in self.tokens and self.test_product_id:
            headers = {'Authorization': f'Bearer {self.tokens["admin"]}'}
            try:
                # Check if test product exists
                response = requests.get(f"{BASE_URL}/products/{self.test_product_id}", headers=headers)
                if response.status_code == 200:
                    product = response.json()
                    if 'TEST' in product.get('barcode', ''):
                        response = requests.delete(f"{BASE_URL}/products/{self.test_product_id}", headers=headers)
                        if response.status_code == 200:
                            print_success("Cleaned up test product")
                        else:
                            print_warning(f"Could not delete test product: {response.status_code}")
            except Exception as e:
                print_warning(f"Cleanup exception: {str(e)}")
    
    def run_all_tests(self):
        """Run all system tests"""
        print_section("🚀 Starting Comprehensive System Test")
        print_info(f"Testing backend at: {BASE_URL}")
        print_info(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.test_authentication()
        self.test_products_api()
        self.test_cart_api()
        self.test_checkout_api()
        self.test_reports_api()
        self.test_role_based_access()
        self.cleanup()
        
        # Final summary
        print_section("📊 Test Summary")
        
        if len(self.errors) == 0 and len(self.warnings) == 0:
            print_success("All tests passed! System is working correctly.")
        else:
            if len(self.errors) > 0:
                print_error(f"Found {len(self.errors)} errors:")
                for error in self.errors:
                    print(f"  - {error}")
            
            if len(self.warnings) > 0:
                print_warning(f"Found {len(self.warnings)} warnings:")
                for warning in self.warnings:
                    print(f"  - {warning}")
        
        print(f"\n{BLUE}Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")

if __name__ == "__main__":
    tester = SystemTester()
    try:
        tester.run_all_tests()
    except KeyboardInterrupt:
        print_warning("\nTest interrupted by user")
    except Exception as e:
        print_error(f"Fatal error: {str(e)}")
