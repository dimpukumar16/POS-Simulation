from datetime import datetime
from models.user import db


class Refund(db.Model):
    """Refund model for tracking refund transactions"""
    __tablename__ = 'refunds'
    
    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    refund_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    amount_cents = db.Column(db.Integer, nullable=False)  # Store in cents
    refunded_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    refund_method = db.Column(db.String(20), nullable=True)  # 'cash', 'card', 'original_method'
    status = db.Column(db.String(20), default='pending')  # 'pending', 'completed', 'failed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    transaction = db.relationship('Transaction', foreign_keys=[transaction_id], backref='refunds')
    refunded_by_user = db.relationship('User', foreign_keys=[refunded_by])
    
    @property
    def amount(self):
        """Get amount in dollars"""
        return self.amount_cents / 100.0
    
    def to_dict(self):
        """Convert refund to dictionary"""
        return {
            'id': self.id,
            'transaction_id': self.transaction_id,
            'transaction_number': self.transaction.transaction_number if self.transaction else None,
            'refund_number': self.refund_number,
            'amount': self.amount,
            'amount_cents': self.amount_cents,
            'refunded_by': self.refunded_by,
            'refunded_by_name': self.refunded_by_user.full_name if self.refunded_by_user else None,
            'reason': self.reason,
            'refund_method': self.refund_method,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
