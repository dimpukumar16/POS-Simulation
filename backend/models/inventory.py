from datetime import datetime
from models.user import db


class AuditLog(db.Model):
    """Audit log for tracking all system operations"""
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    action = db.Column(db.String(50), nullable=False)
    resource_type = db.Column(db.String(50), nullable=True)  # 'product', 'transaction', 'user', etc.
    resource_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    status = db.Column(db.String(20), default='success')  # 'success', 'failed'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='audit_logs')
    
    def to_dict(self):
        """Convert audit log to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else 'System',
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'status': self.status,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


class InventoryLog(db.Model):
    """Log for inventory changes"""
    __tablename__ = 'inventory_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    change_type = db.Column(db.String(20), nullable=False)  # 'sale', 'refund', 'adjustment', 'restock'
    quantity_before = db.Column(db.Integer, nullable=False)
    quantity_change = db.Column(db.Integer, nullable=False)
    quantity_after = db.Column(db.Integer, nullable=False)
    reference_type = db.Column(db.String(50), nullable=True)  # 'transaction', 'manual'
    reference_id = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    product = db.relationship('Product')
    user = db.relationship('User')
    
    def to_dict(self):
        """Convert inventory log to dictionary"""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'change_type': self.change_type,
            'quantity_before': self.quantity_before,
            'quantity_change': self.quantity_change,
            'quantity_after': self.quantity_after,
            'reference_type': self.reference_type,
            'reference_id': self.reference_id,
            'notes': self.notes,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
