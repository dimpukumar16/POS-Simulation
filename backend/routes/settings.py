from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.user import db
from models.settings import Setting
from utils.logger import AuditLogger

settings_bp = Blueprint('settings', __name__, url_prefix='/api/settings')


def has_permission(role, permission):
    """Check if role has permission"""
    permissions = {
        'administrator': ['all'],
        'manager': ['refund', 'void', 'override', 'reports', 'sales'],
        'cashier': ['sales']
    }
    return 'all' in permissions.get(role, []) or permission in permissions.get(role, [])


@settings_bp.route('', methods=['GET'])
def get_settings():
    """
    Get all settings (public settings available without auth)
    
    Query parameters:
        category: str (optional) - filter by category
        public_only: bool (optional) - only return public settings
    """
    try:
        # Build query
        query = Setting.query
        
        # Check if authenticated
        from flask_jwt_extended import verify_jwt_in_request
        try:
            verify_jwt_in_request(optional=True)
            jwt_data = get_jwt()
            user_role = jwt_data.get('role', None)
            authenticated = user_role is not None
        except:
            authenticated = False
        
        # Filter by public only if not authenticated or public_only param
        public_only = request.args.get('public_only', 'false').lower() == 'true'
        if not authenticated or public_only:
            query = query.filter_by(is_public=True)
        
        # Filter by category
        category = request.args.get('category')
        if category:
            query = query.filter_by(category=category)
        
        # Execute query
        settings = query.all()
        
        return jsonify({
            'settings': [setting.to_dict() for setting in settings],
            'count': len(settings)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@settings_bp.route('/<string:key>', methods=['GET'])
def get_setting(key):
    """Get a specific setting by key"""
    try:
        setting = Setting.query.filter_by(key=key).first()
        
        if not setting:
            return jsonify({'error': 'Setting not found'}), 404
        
        # Check if public or authenticated
        from flask_jwt_extended import verify_jwt_in_request
        try:
            verify_jwt_in_request(optional=True)
            authenticated = True
        except:
            authenticated = False
        
        if not setting.is_public and not authenticated:
            return jsonify({'error': 'Unauthorized'}), 401
        
        return jsonify({'setting': setting.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@settings_bp.route('/<string:key>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_setting(key):
    """
    Update a setting (admin only)
    
    Request body:
        value: any (string, int, float, bool, json)
        description: str (optional)
        category: str (optional)
        is_public: bool (optional)
    """
    try:
        # Get user info from JWT
        user_id = int(get_jwt_identity())
        jwt_data = get_jwt()
        user_role = jwt_data.get('role', 'cashier')
        
        # Check permissions (admin only)
        if user_role != 'administrator':
            return jsonify({'error': 'Insufficient permissions. Administrator role required.'}), 403
        
        data = request.get_json()
        value = data.get('value')
        
        if value is None:
            return jsonify({'error': 'Value is required'}), 400
        
        # Get or create setting
        setting = Setting.query.filter_by(key=key).first()
        
        if not setting:
            setting = Setting(key=key)
            db.session.add(setting)
        
        # Update values
        setting.set_value(value)
        
        if 'description' in data:
            setting.description = data['description']
        
        if 'category' in data:
            setting.category = data['category']
        
        if 'is_public' in data:
            setting.is_public = data['is_public']
        
        setting.updated_by = user_id
        
        db.session.commit()
        
        # Log setting change
        AuditLogger.log(
            user_id=user_id,
            action='update_setting',
            resource_type='setting',
            resource_id=setting.id,
            details=f'Updated setting {key} to {value}',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Setting updated successfully',
            'setting': setting.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@settings_bp.route('', methods=['POST'])
@jwt_required()
def create_setting():
    """
    Create a new setting (admin only)
    
    Request body:
        key: str
        value: any
        description: str (optional)
        category: str (optional)
        is_public: bool (optional)
    """
    try:
        # Get user info from JWT
        user_id = int(get_jwt_identity())
        jwt_data = get_jwt()
        user_role = jwt_data.get('role', 'cashier')
        
        # Check permissions (admin only)
        if user_role != 'administrator':
            return jsonify({'error': 'Insufficient permissions. Administrator role required.'}), 403
        
        data = request.get_json()
        key = data.get('key')
        value = data.get('value')
        
        if not key or value is None:
            return jsonify({'error': 'Key and value are required'}), 400
        
        # Check if setting already exists
        existing = Setting.query.filter_by(key=key).first()
        if existing:
            return jsonify({'error': 'Setting already exists. Use PUT to update.'}), 409
        
        # Create setting
        setting = Setting(
            key=key,
            description=data.get('description'),
            category=data.get('category'),
            is_public=data.get('is_public', False),
            updated_by=user_id
        )
        setting.set_value(value)
        
        db.session.add(setting)
        db.session.commit()
        
        # Log setting creation
        AuditLogger.log(
            user_id=user_id,
            action='create_setting',
            resource_type='setting',
            resource_id=setting.id,
            details=f'Created setting {key} with value {value}',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Setting created successfully',
            'setting': setting.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@settings_bp.route('/<string:key>', methods=['DELETE'])
@jwt_required()
def delete_setting(key):
    """
    Delete a setting (admin only)
    """
    try:
        # Get user info from JWT
        user_id = int(get_jwt_identity())
        jwt_data = get_jwt()
        user_role = jwt_data.get('role', 'cashier')
        
        # Check permissions (admin only)
        if user_role != 'administrator':
            return jsonify({'error': 'Insufficient permissions. Administrator role required.'}), 403
        
        setting = Setting.query.filter_by(key=key).first()
        
        if not setting:
            return jsonify({'error': 'Setting not found'}), 404
        
        db.session.delete(setting)
        db.session.commit()
        
        # Log setting deletion
        AuditLogger.log(
            user_id=user_id,
            action='delete_setting',
            resource_type='setting',
            resource_id=setting.id,
            details=f'Deleted setting {key}',
            ip_address=request.remote_addr
        )
        
        return jsonify({'message': 'Setting deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
