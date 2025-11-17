"""
Initialize Database Script
Run this to set up the database with seed data
"""
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Now we can import
from app import app
from models.user import db, User
from utils.db import seed_database

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔧 Initializing POS Simulator Database")
    print("="*60)
    
    with app.app_context():
        # Check if already initialized
        if User.query.first():
            print("⚠  Database already initialized!")
            print("   To reset, delete the database file and run again.")
        else:
            # Seed database
            seed_database(app)
    
    print("\n" + "="*60)
    print("✅ Database ready!")
    print("="*60)
    print("\nYou can now start the server with: python app.py")
    print("\n")
