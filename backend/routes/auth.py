from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models.user import db, User
from models.refresh_token import RefreshToken
from models.settings import Setting
from utils.logger import AuditLogger

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint
    
    Request body:
        username: str
        password: str (optional if using PIN)
        pin: str (optional if using password)
    
    Returns:
        access_token, user info
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        pin = data.get('pin')
        
        if not username:
            return jsonify({'error': 'Username is required'}), 400
        
        if not password and not pin:
            return jsonify({'error': 'Password or PIN is required'}), 400
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        if not user:
            # Log failed attempt
            AuditLogger.log_login_attempt(
                user_id=None,
                username=username,
                success=False,
                ip_address=request.remote_addr
            )
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Check if account is active
        if not user.is_active:
            return jsonify({'error': 'Account is disabled'}), 403
        
        # Verify credentials
        valid = False
        if password:
            valid = user.check_password(password)
        elif pin and user.pin:
            valid = (pin == user.pin)
        
        if not valid:
            # Increment failed login attempts
            user.failed_login_attempts += 1
            db.session.commit()
            
            # Log failed attempt
            AuditLogger.log_login_attempt(
                user_id=user.id,
                username=username,
                success=False,
                ip_address=request.remote_addr
            )
            
            # Get max attempts from settings
            max_attempts = Setting.get_setting('max_failed_login_attempts', 5)
            
            # Lock account after max failed attempts
            if user.failed_login_attempts >= max_attempts:
                user.is_active = False
                db.session.commit()
                return jsonify({'error': 'Account locked due to too many failed attempts. Contact administrator.'}), 403
            
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Successful login
        user.failed_login_attempts = 0
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Log successful login
        AuditLogger.log_login_attempt(
            user_id=user.id,
            username=username,
            success=True,
            ip_address=request.remote_addr
        )
        
        # Create access token (expires in 8 hours)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role},
            expires_delta=timedelta(hours=8)
        )
        
        # Create refresh token (expires in 30 days)
        refresh_token = RefreshToken.create_token(
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent')
        )
        db.session.add(refresh_token)
        db.session.commit()
        
        print(f"DEBUG LOGIN: Created token for user {user.id} with role {user.role}")
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token.token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/verify-pin', methods=['POST'])
@jwt_required()
def verify_pin():
    """
    Verify manager/admin PIN for override operations
    
    Request body:
        pin: str
        action: str (description of action requiring override)
    
    Returns:
        authorization token
    """
    try:
        data = request.get_json()
        pin = data.get('pin')
        action = data.get('action', 'Unknown action')
        
        if not pin:
            return jsonify({'error': 'PIN is required'}), 400
        
        # Find user with matching PIN
        user = User.query.filter_by(pin=pin, is_active=True).first()
        
        if not user:
            return jsonify({'error': 'Invalid PIN'}), 401
        
        # Check if user has manager or admin privileges
        if user.role not in ['manager', 'administrator']:
            return jsonify({'error': 'Insufficient privileges'}), 403
        
        # Log override action
        AuditLogger.log_manager_override(
            manager_id=user.id,
            action=action,
            details=f"Manager {user.username} authorized: {action}",
            ip_address=request.remote_addr
        )
        
        # Create short-lived override token (15 minutes)
        override_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role, 'override': True},
            expires_delta=timedelta(minutes=15)
        )
        
        return jsonify({
            'authorized': True,
            'override_token': override_token,
            'authorizer': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout endpoint
    Note: JWT tokens are stateless, so we just log the action
    """
    try:
        user_id = int(get_jwt_identity())
        
        # Log logout action
        AuditLogger.log(
            user_id=user_id,
            action='logout',
            resource_type='user',
            ip_address=request.remote_addr
        )
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current user information"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user password"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current and new password are required'}), 400
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if not user.check_password(current_password):
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Set new password
        user.set_password(new_password)
        db.session.commit()
        
        # Log password change
        AuditLogger.log(
            user_id=user_id,
            action='change_password',
            resource_type='user',
            resource_id=user_id,
            ip_address=request.remote_addr
        )
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """
    Refresh access token using refresh token
    
    Request body:
        refresh_token: str
    
    Returns:
        new access_token
    """
    try:
        data = request.get_json()
        refresh_token_str = data.get('refresh_token')
        
        if not refresh_token_str:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        # Find refresh token
        refresh_token = RefreshToken.query.filter_by(token=refresh_token_str).first()
        
        if not refresh_token:
            return jsonify({'error': 'Invalid refresh token'}), 401
        
        # Check if token is valid
        if not refresh_token.is_valid():
            return jsonify({'error': 'Refresh token expired or revoked'}), 401
        
        # Get user
        user = User.query.get(refresh_token.user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'User not found or inactive'}), 401
        
        # Update last used
        refresh_token.update_last_used()
        db.session.commit()
        
        # Create new access token
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={'role': user.role},
            expires_delta=timedelta(hours=8)
        )
        
        # Log token refresh
        AuditLogger.log(
            user_id=user.id,
            action='refresh_token',
            resource_type='auth',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/revoke-token', methods=['POST'])
@jwt_required()
def revoke_token():
    """
    Revoke a refresh token
    
    Request body:
        refresh_token: str
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        refresh_token_str = data.get('refresh_token')
        
        if not refresh_token_str:
            return jsonify({'error': 'Refresh token is required'}), 400
        
        # Find refresh token
        refresh_token = RefreshToken.query.filter_by(token=refresh_token_str, user_id=user_id).first()
        
        if not refresh_token:
            return jsonify({'error': 'Refresh token not found'}), 404
        
        # Revoke token
        refresh_token.revoke()
        db.session.commit()
        
        # Log token revocation
        AuditLogger.log(
            user_id=user_id,
            action='revoke_token',
            resource_type='auth',
            ip_address=request.remote_addr
        )
        
        return jsonify({'message': 'Token revoked successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
