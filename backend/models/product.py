from datetime import datetime
from models.user import db


class Product(db.Model):
    """Product model for inventory management"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    barcode = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)
    price = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=True)  # Cost price for profit calculations
    stock_quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=10)
    tax_rate = db.Column(db.Float, default=0.0)  # Tax rate as decimal (e.g., 0.18 for 18%)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    transaction_items = db.relationship('TransactionItem', back_populates='product', lazy='dynamic')
    
    def update_stock(self, quantity_change):
        """Update stock quantity"""
        self.stock_quantity += quantity_change
        if self.stock_quantity < 0:
            raise ValueError(f"Insufficient stock for product {self.name}")
    
    def is_in_stock(self, quantity=1):
        """Check if product has sufficient stock"""
        return self.stock_quantity >= quantity
    
    def needs_reorder(self):
        """Check if stock is below reorder level"""
        return self.stock_quantity <= self.reorder_level
    
    def calculate_price_with_tax(self, quantity=1):
        """Calculate total price including tax"""
        subtotal = self.price * quantity
        tax = subtotal * self.tax_rate
        return {
            'subtotal': round(subtotal, 2),
            'tax': round(tax, 2),
            'total': round(subtotal + tax, 2)
        }
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': self.id,
            'barcode': self.barcode,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'price': self.price,
            'cost': self.cost,
            'stock_quantity': self.stock_quantity,
            'reorder_level': self.reorder_level,
            'tax_rate': self.tax_rate,
            'is_active': self.is_active,
            'needs_reorder': self.needs_reorder(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
