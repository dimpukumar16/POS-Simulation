from datetime import datetime
from models.user import db
from models.inventory import AuditLog


class AuditLogger:
    """Utility class for audit logging"""
    
    @staticmethod
    def log(user_id, action, resource_type=None, resource_id=None, 
            details=None, ip_address=None, status='success'):
        """
        Create an audit log entry
        
        Args:
            user_id: ID of the user performing the action
            action: Action being performed (e.g., 'login', 'create_product', 'process_sale')
            resource_type: Type of resource affected (e.g., 'product', 'transaction')
            resource_id: ID of the affected resource
            details: Additional details about the action
            ip_address: IP address of the request
            status: Status of the action ('success' or 'failed')
        """
        try:
            log_entry = AuditLog(
                user_id=user_id,
                action=action,
                resource_type=resource_type,
                resource_id=resource_id,
                details=details,
                ip_address=ip_address,
                status=status,
                timestamp=datetime.utcnow()
            )
            db.session.add(log_entry)
            db.session.commit()
            return log_entry
        except Exception as e:
            print(f"Error creating audit log: {str(e)}")
            db.session.rollback()
            return None
    
    @staticmethod
    def log_login_attempt(user_id, username, success, ip_address=None):
        """Log login attempt"""
        status = 'success' if success else 'failed'
        details = f"User '{username}' login attempt"
        return AuditLogger.log(
            user_id=user_id,
            action='login',
            resource_type='user',
            details=details,
            ip_address=ip_address,
            status=status
        )
    
    @staticmethod
    def log_product_action(user_id, action, product_id, details=None, ip_address=None):
        """Log product-related actions"""
        return AuditLogger.log(
            user_id=user_id,
            action=action,
            resource_type='product',
            resource_id=product_id,
            details=details,
            ip_address=ip_address
        )
    
    @staticmethod
    def log_transaction_action(user_id, action, transaction_id, details=None, ip_address=None):
        """Log transaction-related actions"""
        return AuditLogger.log(
            user_id=user_id,
            action=action,
            resource_type='transaction',
            resource_id=transaction_id,
            details=details,
            ip_address=ip_address
        )
    
    @staticmethod
    def log_manager_override(manager_id, action, details=None, ip_address=None):
        """Log manager override actions"""
        return AuditLogger.log(
            user_id=manager_id,
            action=f'override_{action}',
            resource_type='authorization',
            details=details,
            ip_address=ip_address
        )
    
    @staticmethod
    def get_recent_logs(limit=100, user_id=None, action=None):
        """
        Retrieve recent audit logs
        
        Args:
            limit: Maximum number of logs to retrieve
            user_id: Filter by user ID
            action: Filter by action type
        """
        query = AuditLog.query.order_by(AuditLog.timestamp.desc())
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if action:
            query = query.filter_by(action=action)
        
        return query.limit(limit).all()
    
    @staticmethod
    def get_failed_login_attempts(username, hours=24):
        """Get failed login attempts for a user within specified hours"""
        from datetime import timedelta
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        logs = AuditLog.query.filter(
            AuditLog.action == 'login',
            AuditLog.status == 'failed',
            AuditLog.details.like(f"%'{username}'%"),
            AuditLog.timestamp >= cutoff_time
        ).count()
        
        return logs


# Convenience function for quick logging
def log_action(user_id, action, **kwargs):
    """Quick logging function"""
    return AuditLogger.log(user_id, action, **kwargs)
