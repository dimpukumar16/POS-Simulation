from datetime import datetime
from models.user import db
import json


class Setting(db.Model):
    """Settings model for storing application configuration"""
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=True)
    value_type = db.Column(db.String(20), default='string')  # 'string', 'int', 'float', 'bool', 'json'
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)  # 'tax', 'security', 'payment', 'general'
    is_public = db.Column(db.Boolean, default=False)  # Can be read without authentication
    updated_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    updated_by_user = db.relationship('User', foreign_keys=[updated_by])
    
    def get_value(self):
        """Get typed value based on value_type"""
        if self.value is None:
            return None
        
        try:
            if self.value_type == 'int':
                return int(self.value)
            elif self.value_type == 'float':
                return float(self.value)
            elif self.value_type == 'bool':
                return self.value.lower() in ('true', '1', 'yes', 'on')
            elif self.value_type == 'json':
                return json.loads(self.value)
            else:
                return self.value
        except (ValueError, json.JSONDecodeError):
            return self.value
    
    def set_value(self, value):
        """Set value and auto-detect type if needed"""
        if isinstance(value, bool):
            self.value_type = 'bool'
            self.value = 'true' if value else 'false'
        elif isinstance(value, int):
            self.value_type = 'int'
            self.value = str(value)
        elif isinstance(value, float):
            self.value_type = 'float'
            self.value = str(value)
        elif isinstance(value, (dict, list)):
            self.value_type = 'json'
            self.value = json.dumps(value)
        else:
            self.value_type = 'string'
            self.value = str(value)
    
    @staticmethod
    def get_setting(key, default=None):
        """Get setting value by key"""
        setting = Setting.query.filter_by(key=key).first()
        if setting:
            return setting.get_value()
        return default
    
    @staticmethod
    def set_setting(key, value, description=None, category=None, user_id=None):
        """Set or update a setting"""
        setting = Setting.query.filter_by(key=key).first()
        if not setting:
            setting = Setting(key=key, description=description, category=category)
            db.session.add(setting)
        
        setting.set_value(value)
        setting.updated_by = user_id
        setting.updated_at = datetime.utcnow()
        
        return setting
    
    def to_dict(self):
        """Convert setting to dictionary"""
        return {
            'id': self.id,
            'key': self.key,
            'value': self.get_value(),
            'value_type': self.value_type,
            'description': self.description,
            'category': self.category,
            'is_public': self.is_public,
            'updated_by': self.updated_by,
            'updated_by_name': self.updated_by_user.full_name if self.updated_by_user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Default settings to be seeded on first run
DEFAULT_SETTINGS = [
    {
        'key': 'max_failed_login_attempts',
        'value': 5,
        'description': 'Maximum failed login attempts before account lockout',
        'category': 'security'
    },
    {
        'key': 'session_timeout_hours',
        'value': 8,
        'description': 'Session timeout in hours',
        'category': 'security'
    },
    {
        'key': 'default_tax_rate',
        'value': 0.0,
        'description': 'Default tax rate (0.18 = 18%)',
        'category': 'tax'
    },
    {
        'key': 'store_name',
        'value': 'POS Simulator Store',
        'description': 'Store name for receipts and reports',
        'category': 'general',
        'is_public': True
    },
    {
        'key': 'receipt_footer_text',
        'value': 'Thank you for your business!',
        'description': 'Footer text on receipts',
        'category': 'general'
    },
    {
        'key': 'enable_manager_override',
        'value': True,
        'description': 'Enable manager override for restricted actions',
        'category': 'security'
    },
    {
        'key': 'max_discount_percentage',
        'value': 50,
        'description': 'Maximum discount percentage allowed',
        'category': 'general'
    }
]
