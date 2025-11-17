import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.user import db, User
from models.product import Product
from models.transaction import Transaction, TransactionItem
from models.inventory import AuditLog, InventoryLog
from models.refund import Refund
from models.refresh_token import RefreshToken
from models.settings import Setting, DEFAULT_SETTINGS


def init_db(app):
    """Initialize database with app context"""
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✓ Database tables created successfully")


def seed_database(app):
    """Populate database with initial data"""
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("⚠ Database already contains data. Skipping seed.")
            return
        
        print("🌱 Seeding database...")
        
        # Create default users
        users = [
            {
                'username': 'admin',
                'password': 'admin123',
                'pin': '1111',
                'role': 'administrator',
                'email': 'admin@pos.com',
                'full_name': 'System Administrator'
            },
            {
                'username': 'manager',
                'password': 'manager123',
                'pin': '2222',
                'role': 'manager',
                'email': 'manager@pos.com',
                'full_name': 'Store Manager'
            },
            {
                'username': 'cashier',
                'password': 'cashier123',
                'pin': '3333',
                'role': 'cashier',
                'email': 'cashier@pos.com',
                'full_name': 'John Cashier'
            },
            {
                'username': 'cashier2',
                'password': 'cashier123',
                'pin': '4444',
                'role': 'cashier',
                'email': 'cashier2@pos.com',
                'full_name': 'Jane Cashier'
            }
        ]
        
        for user_data in users:
            user = User(
                username=user_data['username'],
                pin=user_data['pin'],
                role=user_data['role'],
                email=user_data['email'],
                full_name=user_data['full_name']
            )
            user.set_password(user_data['password'])
            db.session.add(user)
        
        print("✓ Created default users")
        
        # Create sample products
        products = [
            {
                'barcode': '1234567890',
                'name': 'Laptop - Dell XPS 13',
                'description': '13-inch laptop with Intel i7 processor',
                'category': 'Electronics',
                'price': 999.99,
                'cost': 750.00,
                'stock_quantity': 25,
                'reorder_level': 5,
                'tax_rate': 0.18
            },
            {
                'barcode': '2345678901',
                'name': 'Wireless Mouse',
                'description': 'Ergonomic wireless mouse with USB receiver',
                'category': 'Electronics',
                'price': 29.99,
                'cost': 15.00,
                'stock_quantity': 100,
                'reorder_level': 20,
                'tax_rate': 0.18
            },
            {
                'barcode': '3456789012',
                'name': 'USB-C Cable 2m',
                'description': 'High-speed USB-C charging cable',
                'category': 'Accessories',
                'price': 14.99,
                'cost': 5.00,
                'stock_quantity': 200,
                'reorder_level': 50,
                'tax_rate': 0.18
            },
            {
                'barcode': '4567890123',
                'name': 'Mechanical Keyboard',
                'description': 'RGB mechanical gaming keyboard',
                'category': 'Electronics',
                'price': 89.99,
                'cost': 45.00,
                'stock_quantity': 50,
                'reorder_level': 10,
                'tax_rate': 0.18
            },
            {
                'barcode': '5678901234',
                'name': 'Office Chair',
                'description': 'Ergonomic office chair with lumbar support',
                'category': 'Furniture',
                'price': 249.99,
                'cost': 150.00,
                'stock_quantity': 15,
                'reorder_level': 5,
                'tax_rate': 0.12
            },
            {
                'barcode': '6789012345',
                'name': 'Monitor 24"',
                'description': '24-inch Full HD IPS monitor',
                'category': 'Electronics',
                'price': 179.99,
                'cost': 100.00,
                'stock_quantity': 30,
                'reorder_level': 8,
                'tax_rate': 0.18
            },
            {
                'barcode': '7890123456',
                'name': 'Desk Lamp LED',
                'description': 'Adjustable LED desk lamp',
                'category': 'Accessories',
                'price': 39.99,
                'cost': 20.00,
                'stock_quantity': 75,
                'reorder_level': 15,
                'tax_rate': 0.18
            },
            {
                'barcode': '8901234567',
                'name': 'Notebook A4',
                'description': 'A4 ruled notebook 200 pages',
                'category': 'Stationery',
                'price': 4.99,
                'cost': 2.00,
                'stock_quantity': 500,
                'reorder_level': 100,
                'tax_rate': 0.05
            },
            {
                'barcode': '9012345678',
                'name': 'Pen Set (10 pack)',
                'description': 'Blue ballpoint pens pack of 10',
                'category': 'Stationery',
                'price': 7.99,
                'cost': 3.00,
                'stock_quantity': 300,
                'reorder_level': 50,
                'tax_rate': 0.05
            },
            {
                'barcode': '0123456789',
                'name': 'Water Bottle 1L',
                'description': 'Stainless steel insulated water bottle',
                'category': 'Accessories',
                'price': 24.99,
                'cost': 12.00,
                'stock_quantity': 80,
                'reorder_level': 20,
                'tax_rate': 0.12
            }
        ]
        
        for product_data in products:
            product = Product(**product_data)
            db.session.add(product)
        
        print("✓ Created sample products")
        
        # Create default settings
        for setting_data in DEFAULT_SETTINGS:
            setting = Setting(
                key=setting_data['key'],
                description=setting_data['description'],
                category=setting_data['category'],
                is_public=setting_data.get('is_public', False)
            )
            setting.set_value(setting_data['value'])
            db.session.add(setting)
        
        print("✓ Created default settings")
        
        # Commit all changes
        db.session.commit()
        print("✅ Database seeding completed successfully!")


def reset_database(app):
    """Drop and recreate all tables"""
    with app.app_context():
        db.drop_all()
        print("✓ Dropped all tables")
        db.create_all()
        print("✓ Recreated all tables")
        seed_database(app)


if __name__ == '__main__':
    # For standalone execution
    from flask import Flask
    
    app = Flask(__name__)
    
    # Configure database
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_dir = os.path.join(os.path.dirname(basedir), 'database')
    os.makedirs(database_dir, exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(database_dir, "pos.db")}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize and seed database
    init_db(app)
    seed_database(app)
    
    print("\n" + "="*50)
    print("Database initialized at:", os.path.join(database_dir, "pos.db"))
    print("="*50)
