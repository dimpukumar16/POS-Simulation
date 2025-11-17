"""
Test Data Generator
Generates sample data for testing the POS system
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from faker import Faker
from app import app
from models.user import db, User
from models.product import Product
from models.transaction import Transaction, TransactionItem
from datetime import datetime, timedelta
import random

fake = Faker()


def generate_users(count=10):
    """Generate test users"""
    print(f"\nGenerating {count} test users...")
    
    roles = ['cashier'] * 7 + ['manager'] * 2 + ['administrator'] * 1
    
    for i in range(count):
        username = f"user{i+1}"
        role = roles[i] if i < len(roles) else 'cashier'
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            continue
        
        user = User(
            username=username,
            role=role,
            email=f"{username}@pos.com",
            full_name=fake.name(),
            pin=str(random.randint(1000, 9999))
        )
        user.set_password('password123')
        db.session.add(user)
        
        print(f"  ✓ Created {role}: {username}")
    
    db.session.commit()
    print(f"✅ Generated {count} users")


def generate_products(count=50):
    """Generate test products"""
    print(f"\nGenerating {count} test products...")
    
    categories = [
        'Electronics', 'Furniture', 'Stationery', 
        'Accessories', 'Books', 'Clothing', 'Food'
    ]
    
    for i in range(count):
        barcode = f"TEST{str(random.randint(10000, 99999))}"
        
        # Check if barcode already exists
        if Product.query.filter_by(barcode=barcode).first():
            continue
        
        category = random.choice(categories)
        price = round(random.uniform(5, 500), 2)
        cost = round(price * 0.6, 2)
        
        product = Product(
            barcode=barcode,
            name=fake.catch_phrase(),
            description=fake.text(max_nb_chars=100),
            category=category,
            price=price,
            cost=cost,
            stock_quantity=random.randint(10, 200),
            reorder_level=random.randint(5, 20),
            tax_rate=random.choice([0.05, 0.12, 0.18])
        )
        
        db.session.add(product)
    
    db.session.commit()
    print(f"✅ Generated {count} products")


def generate_transactions(count=100):
    """Generate test transactions"""
    print(f"\nGenerating {count} test transactions...")
    
    users = User.query.filter_by(role='cashier').all()
    products = Product.query.filter_by(is_active=True).all()
    
    if not users or not products:
        print("⚠ Need users and products first!")
        return
    
    payment_methods = ['cash', 'card', 'upi']
    
    for i in range(count):
        user = random.choice(users)
        
        # Random date in the last 30 days
        days_ago = random.randint(0, 30)
        trans_date = datetime.utcnow() - timedelta(days=days_ago)
        
        # Create transaction
        transaction = Transaction(
            transaction_number=f"TXN-{fake.unique.random_number(digits=12)}",
            user_id=user.id,
            transaction_type='sale',
            status='completed',
            payment_method=random.choice(payment_methods),
            created_at=trans_date,
            completed_at=trans_date
        )
        
        db.session.add(transaction)
        db.session.flush()
        
        # Add 1-5 items to transaction
        num_items = random.randint(1, 5)
        selected_products = random.sample(products, min(num_items, len(products)))
        
        subtotal = 0
        tax_total = 0
        
        for product in selected_products:
            quantity = random.randint(1, 3)
            unit_price = product.price
            line_subtotal = unit_price * quantity
            tax_amount = line_subtotal * product.tax_rate
            line_total = line_subtotal + tax_amount
            
            item = TransactionItem(
                transaction_id=transaction.id,
                product_id=product.id,
                quantity=quantity,
                unit_price=unit_price,
                tax_rate=product.tax_rate,
                tax_amount=tax_amount,
                line_total=line_total
            )
            
            db.session.add(item)
            
            subtotal += line_subtotal
            tax_total += tax_amount
        
        # Update transaction totals
        transaction.subtotal = subtotal
        transaction.tax_amount = tax_total
        transaction.total_amount = subtotal + tax_total
        
        if transaction.payment_method == 'cash':
            transaction.amount_paid = transaction.total_amount + random.randint(0, 20)
            transaction.change_given = transaction.amount_paid - transaction.total_amount
        else:
            transaction.amount_paid = transaction.total_amount
            transaction.change_given = 0
    
    db.session.commit()
    print(f"✅ Generated {count} transactions")


def main():
    """Main function to generate all test data"""
    with app.app_context():
        print("\n" + "="*60)
        print("📊 TEST DATA GENERATOR")
        print("="*60)
        
        choice = input("\nWhat would you like to generate?\n"
                      "1. Users\n"
                      "2. Products\n"
                      "3. Transactions\n"
                      "4. All\n"
                      "Enter choice (1-4): ")
        
        if choice == '1':
            count = int(input("How many users? (default 10): ") or 10)
            generate_users(count)
        elif choice == '2':
            count = int(input("How many products? (default 50): ") or 50)
            generate_products(count)
        elif choice == '3':
            count = int(input("How many transactions? (default 100): ") or 100)
            generate_transactions(count)
        elif choice == '4':
            generate_users(10)
            generate_products(50)
            generate_transactions(100)
        else:
            print("Invalid choice!")
            return
        
        print("\n" + "="*60)
        print("✅ TEST DATA GENERATION COMPLETE!")
        print("="*60)


if __name__ == '__main__':
    main()
