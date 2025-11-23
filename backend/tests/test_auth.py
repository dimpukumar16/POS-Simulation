import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from models.user import db, User
from models.product import Product


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test-secret-key'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            seed_test_data()
        yield client


def seed_test_data():
    """Seed test data"""
    # Create test user only if doesn't exist
    existing_user = User.query.filter_by(username='testcashier').first()
    if not existing_user:
        user = User(
            username='testcashier',
            role='cashier',
            email='test@pos.com',
            full_name='Test Cashier'
        )
        user.set_password('test123')
        db.session.add(user)
    
    # Create test product only if doesn't exist
    existing_product = Product.query.filter_by(barcode='TEST123').first()
    if not existing_product:
        product = Product(
            barcode='TEST123',
            name='Test Product',
            price=10.99,
            stock_quantity=100,
            tax_rate=0.18
        )
        db.session.add(product)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        # Ignore duplicate errors since we're checking anyway
        pass


def test_login_success(client):
    """Test successful login"""
    response = client.post('/api/auth/login', json={
        'username': 'testcashier',
        'password': 'test123'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert data['user']['username'] == 'testcashier'


def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login', json={
        'username': 'testcashier',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data


def test_login_missing_username(client):
    """Test login without username"""
    response = client.post('/api/auth/login', json={
        'password': 'test123'
    })
    
    assert response.status_code == 400


def get_auth_headers(client):
    """Helper function to get authorization headers"""
    response = client.post('/api/auth/login', json={
        'username': 'testcashier',
        'password': 'test123'
    })
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_get_current_user(client):
    """Test get current user endpoint"""
    headers = get_auth_headers(client)
    
    response = client.get('/api/auth/me', headers=headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['username'] == 'testcashier'


def test_unauthorized_access(client):
    """Test accessing protected endpoint without token"""
    response = client.get('/api/auth/me')
    
    assert response.status_code == 401
