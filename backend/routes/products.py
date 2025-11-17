from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.user import db, User
from models.product import Product
from models.inventory import InventoryLog
from utils.logger import AuditLogger

products_bp = Blueprint('products', __name__, url_prefix='/api/products')


def require_role(*roles):
    """Decorator to check user role"""
    def wrapper(fn):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            user_role = claims.get('role')
            if user_role not in roles:
                return jsonify({'error': 'Insufficient privileges'}), 403
            return fn(*args, **kwargs)
        decorator.__name__ = fn.__name__
        return decorator
    return wrapper


@products_bp.route('', methods=['GET'])
@jwt_required()
def get_products():
    """Get all products with optional filtering"""
    try:
        # Debug: Check JWT identity type while troubleshooting auth issues
        user_id = int(get_jwt_identity())
        print(f"DEBUG PRODUCTS: JWT identity: {user_id}, type: {type(user_id)}")
        
        # Query parameters
        category = request.args.get('category')
        active_only = request.args.get('active', 'true').lower() == 'true'
        search = request.args.get('search')
        low_stock = request.args.get('low_stock', 'false').lower() == 'true'
        
        query = Product.query
        
        if active_only:
            query = query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        if search:
            query = query.filter(
                db.or_(
                    Product.name.ilike(f'%{search}%'),
                    Product.barcode.ilike(f'%{search}%'),
                    Product.description.ilike(f'%{search}%')
                )
            )
        
        products = query.all()
        
        if low_stock:
            products = [p for p in products if p.needs_reorder()]
        
        return jsonify({
            'products': [p.to_dict() for p in products],
            'count': len(products)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<barcode>', methods=['GET'])
@jwt_required()
def get_product_by_barcode(barcode):
    """Get product by barcode"""
    try:
        product = Product.query.filter_by(barcode=barcode).first()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/id/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product_by_id(product_id):
    """Get product by ID"""
    try:
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        return jsonify({'product': product.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('', methods=['POST'])
@require_role('administrator', 'manager')
def create_product():
    """Create new product (Admin/Manager only)"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['barcode', 'name', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if barcode already exists
        if Product.query.filter_by(barcode=data['barcode']).first():
            return jsonify({'error': 'Product with this barcode already exists'}), 409
        
        # Create product
        product = Product(
            barcode=data['barcode'],
            name=data['name'],
            description=data.get('description'),
            category=data.get('category'),
            price=float(data['price']),
            cost=float(data.get('cost', 0)),
            stock_quantity=int(data.get('stock_quantity', 0)),
            reorder_level=int(data.get('reorder_level', 10)),
            tax_rate=float(data.get('tax_rate', 0)),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(product)
        db.session.commit()
        
        # Log action
        AuditLogger.log_product_action(
            user_id=user_id,
            action='create_product',
            product_id=product.id,
            details=f"Created product: {product.name}",
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Product created successfully',
            'product': product.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['PUT'])
@require_role('administrator', 'manager')
def update_product(product_id):
    """Update product (Admin/Manager only)"""
    try:
        user_id = int(get_jwt_identity())
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'category' in data:
            product.category = data['category']
        if 'price' in data:
            product.price = float(data['price'])
        if 'cost' in data:
            product.cost = float(data['cost'])
        if 'stock_quantity' in data:
            old_quantity = product.stock_quantity
            new_quantity = int(data['stock_quantity'])
            product.stock_quantity = new_quantity
            
            # Log inventory change
            inv_log = InventoryLog(
                product_id=product.id,
                user_id=user_id,
                change_type='adjustment',
                quantity_before=old_quantity,
                quantity_change=new_quantity - old_quantity,
                quantity_after=new_quantity,
                reference_type='manual',
                notes='Manual stock adjustment'
            )
            db.session.add(inv_log)
        
        if 'reorder_level' in data:
            product.reorder_level = int(data['reorder_level'])
        if 'tax_rate' in data:
            product.tax_rate = float(data['tax_rate'])
        if 'is_active' in data:
            product.is_active = data['is_active']
        
        db.session.commit()
        
        # Log action
        AuditLogger.log_product_action(
            user_id=user_id,
            action='update_product',
            product_id=product.id,
            details=f"Updated product: {product.name}",
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@require_role('administrator')
def delete_product(product_id):
    """Delete product (Admin only)"""
    try:
        user_id = int(get_jwt_identity())
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        product_name = product.name
        
        # Soft delete (just deactivate)
        product.is_active = False
        db.session.commit()
        
        # Log action
        AuditLogger.log_product_action(
            user_id=user_id,
            action='delete_product',
            product_id=product.id,
            details=f"Deleted product: {product_name}",
            ip_address=request.remote_addr
        )
        
        return jsonify({'message': 'Product deleted successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@products_bp.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get all product categories"""
    try:
        categories = db.session.query(Product.category).distinct().filter(Product.category.isnot(None)).all()
        categories = [c[0] for c in categories]
        
        return jsonify({'categories': categories}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
