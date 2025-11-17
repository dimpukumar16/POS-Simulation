from datetime import datetime, timedelta
from models.user import db
import secrets


class RefreshToken(db.Model):
    """Refresh token model for JWT authentication"""
    __tablename__ = 'refresh_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    is_revoked = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used_at = db.Column(db.DateTime, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    
    # Relationships
    user = db.relationship('User', backref='refresh_tokens')
    
    @staticmethod
    def generate_token():
        """Generate a secure random token"""
        return secrets.token_urlsafe(64)
    
    @staticmethod
    def create_token(user_id, ip_address=None, user_agent=None, expires_days=30):
        """Create a new refresh token"""
        token = RefreshToken(
            user_id=user_id,
            token=RefreshToken.generate_token(),
            expires_at=datetime.utcnow() + timedelta(days=expires_days),
            ip_address=ip_address,
            user_agent=user_agent
        )
        return token
    
    def is_valid(self):
        """Check if token is valid (not expired and not revoked)"""
        return not self.is_revoked and self.expires_at > datetime.utcnow()
    
    def revoke(self):
        """Revoke this token"""
        self.is_revoked = True
    
    def update_last_used(self):
        """Update last used timestamp"""
        self.last_used_at = datetime.utcnow()
    
    def to_dict(self):
        """Convert refresh token to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_revoked': self.is_revoked,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used_at': self.last_used_at.isoformat() if self.last_used_at else None
        }
