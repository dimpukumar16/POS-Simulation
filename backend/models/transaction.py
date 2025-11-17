from datetime import datetime
from models.user import db


class Transaction(db.Model):
    """Transaction model for sales records"""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'sale', 'refund', 'void'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed', 'voided'
    
    # Amounts
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    discount_type = db.Column(db.String(20), nullable=True)  # 'percentage', 'fixed'
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, default=0.0)
    
    # Payment details
    payment_method = db.Column(db.String(20), nullable=True)  # 'cash', 'card', 'upi'
    payment_reference = db.Column(db.String(100), nullable=True)
    amount_paid = db.Column(db.Float, default=0.0)
    change_given = db.Column(db.Float, default=0.0)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    refund_reason = db.Column(db.Text, nullable=True)
    authorized_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # For refunds/voids
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], back_populates='transactions', overlaps='authorizer')
    authorizer = db.relationship('User', foreign_keys=[authorized_by], overlaps='user')
    items = db.relationship('TransactionItem', back_populates='transaction', lazy='dynamic', cascade='all, delete-orphan')
    
    def calculate_totals(self):
        """Calculate transaction totals from items"""
        self.subtotal = sum(item.line_total for item in self.items)
        
        # Apply discount
        if self.discount_type == 'percentage':
            self.discount_amount = self.subtotal * (self.discount_amount / 100)
        
        amount_after_discount = self.subtotal - self.discount_amount
        
        # Calculate tax
        self.tax_amount = sum(item.tax_amount for item in self.items)
        
        # Calculate total
        self.total_amount = amount_after_discount + self.tax_amount
        
        return {
            'subtotal': round(self.subtotal, 2),
            'discount': round(self.discount_amount, 2),
            'tax': round(self.tax_amount, 2),
            'total': round(self.total_amount, 2)
        }
    
    def to_dict(self, include_items=True):
        """Convert transaction to dictionary"""
        data = {
            'id': self.id,
            'transaction_number': self.transaction_number,
            'user_id': self.user_id,
            'cashier': self.user.full_name if self.user else None,
            'transaction_type': self.transaction_type,
            'status': self.status,
            'subtotal': self.subtotal,
            'discount_amount': self.discount_amount,
            'discount_type': self.discount_type,
            'tax_amount': self.tax_amount,
            'total_amount': self.total_amount,
            'payment_method': self.payment_method,
            'payment_reference': self.payment_reference,
            'amount_paid': self.amount_paid,
            'change_given': self.change_given,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'refund_reason': self.refund_reason,
            'authorized_by': self.authorized_by
        }
        
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        
        return data


class TransactionItem(db.Model):
    """Individual items in a transaction"""
    __tablename__ = 'transaction_items'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    tax_rate = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    line_total = db.Column(db.Float, nullable=False)
    
    # Relationships
    transaction = db.relationship('Transaction', back_populates='items')
    product = db.relationship('Product', back_populates='transaction_items')
    
    def calculate_line_total(self):
        """Calculate line total including tax"""
        subtotal = self.unit_price * self.quantity
        subtotal_after_discount = subtotal - self.discount_amount
        self.tax_amount = subtotal_after_discount * self.tax_rate
        self.line_total = subtotal_after_discount + self.tax_amount
        return self.line_total
    
    def to_dict(self):
        """Convert transaction item to dictionary"""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'barcode': self.product.barcode if self.product else None,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
            'discount_amount': self.discount_amount,
            'tax_rate': self.tax_rate,
            'tax_amount': self.tax_amount,
            'line_total': self.line_total
        }
