from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import db
from models.product import Product
from datetime import datetime

cart_bp = Blueprint('cart', __name__, url_prefix='/api/cart')

# In-memory cart storage (in production, use Redis or database)
carts = {}


def get_cart_key(user_id):
    """Generate cart key for user"""
    return f"cart_{user_id}"


def get_user_cart(user_id):
    """Get or create user cart"""
    cart_key = get_cart_key(user_id)
    if cart_key not in carts:
        carts[cart_key] = {
            'items': [],
            'discount': {'type': None, 'amount': 0},
            'created_at': datetime.utcnow().isoformat()
        }
    return carts[cart_key]


def calculate_cart_totals(cart):
    """Calculate cart totals including tax and discounts"""
    items = cart['items']
    discount = cart['discount']
    
    subtotal = sum(item['line_total'] for item in items)
    
    # Apply discount
    discount_amount = 0
    if discount['type'] == 'percentage':
        discount_amount = subtotal * (discount['amount'] / 100)
    elif discount['type'] == 'fixed':
        discount_amount = min(discount['amount'], subtotal)
    
    amount_after_discount = subtotal - discount_amount
    
    # Calculate tax
    tax_amount = sum(item['tax_amount'] for item in items)
    
    # Calculate total
    total = amount_after_discount + tax_amount
    
    return {
        'subtotal': round(subtotal, 2),
        'discount_amount': round(discount_amount, 2),
        'discount_type': discount['type'],
        'tax_amount': round(tax_amount, 2),
        'total': round(total, 2),
        'item_count': len(items)
    }


@cart_bp.route('', methods=['GET'])
@jwt_required()
def get_cart():
    """Get current user's cart"""
    try:
        user_id = int(get_jwt_identity())
        cart = get_user_cart(user_id)
        totals = calculate_cart_totals(cart)
        
        return jsonify({
            'cart': {
                'items': cart['items'],
                'discount': cart['discount'],
                **totals
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    """
    Add item to cart
    
    Request body:
        barcode or product_id: str/int
        quantity: int (default 1)
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        barcode = data.get('barcode')
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be positive'}), 400
        
        # Find product
        if barcode:
            product = Product.query.filter_by(barcode=barcode, is_active=True).first()
        elif product_id:
            product = Product.query.filter_by(id=product_id, is_active=True).first()
        else:
            return jsonify({'error': 'Barcode or product_id is required'}), 400
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        # Check stock
        if not product.is_in_stock(quantity):
            return jsonify({
                'error': 'Insufficient stock',
                'available': product.stock_quantity
            }), 400
        
        # Get cart
        cart = get_user_cart(user_id)
        
        # Check if item already in cart
        existing_item = next((item for item in cart['items'] if item['product_id'] == product.id), None)
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item['quantity'] + quantity
            if not product.is_in_stock(new_quantity):
                return jsonify({
                    'error': 'Insufficient stock for requested quantity',
                    'available': product.stock_quantity,
                    'in_cart': existing_item['quantity']
                }), 400
            
            existing_item['quantity'] = new_quantity
            existing_item['line_subtotal'] = product.price * new_quantity
            existing_item['tax_amount'] = existing_item['line_subtotal'] * product.tax_rate
            existing_item['line_total'] = existing_item['line_subtotal'] + existing_item['tax_amount']
        else:
            # Add new item
            line_subtotal = product.price * quantity
            tax_amount = line_subtotal * product.tax_rate
            line_total = line_subtotal + tax_amount
            
            cart_item = {
                'cart_item_id': len(cart['items']) + 1,
                'product_id': product.id,
                'barcode': product.barcode,
                'name': product.name,
                'unit_price': product.price,
                'quantity': quantity,
                'tax_rate': product.tax_rate,
                'item_discount': 0,
                'line_subtotal': round(line_subtotal, 2),
                'tax_amount': round(tax_amount, 2),
                'line_total': round(line_total, 2)
            }
            
            cart['items'].append(cart_item)
        
        totals = calculate_cart_totals(cart)
        
        return jsonify({
            'message': 'Item added to cart',
            'cart': {
                'items': cart['items'],
                'discount': cart['discount'],
                **totals
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/update', methods=['PUT'])
@jwt_required()
def update_cart_item():
    """
    Update cart item quantity
    
    Request body:
        cart_item_id: int
        quantity: int
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        cart_item_id = data.get('cart_item_id')
        quantity = int(data.get('quantity'))
        
        if not cart_item_id:
            return jsonify({'error': 'cart_item_id is required'}), 400
        
        if quantity < 0:
            return jsonify({'error': 'Quantity cannot be negative'}), 400
        
        cart = get_user_cart(user_id)
        
        # Find item
        item = next((item for item in cart['items'] if item['cart_item_id'] == cart_item_id), None)
        
        if not item:
            return jsonify({'error': 'Item not found in cart'}), 404
        
        # If quantity is 0, remove item
        if quantity == 0:
            cart['items'] = [i for i in cart['items'] if i['cart_item_id'] != cart_item_id]
        else:
            # Check stock
            product = Product.query.get(item['product_id'])
            if not product.is_in_stock(quantity):
                return jsonify({
                    'error': 'Insufficient stock',
                    'available': product.stock_quantity
                }), 400
            
            # Update quantity
            item['quantity'] = quantity
            item['line_subtotal'] = item['unit_price'] * quantity
            item['tax_amount'] = item['line_subtotal'] * item['tax_rate']
            item['line_total'] = item['line_subtotal'] + item['tax_amount']
        
        totals = calculate_cart_totals(cart)
        
        return jsonify({
            'message': 'Cart updated',
            'cart': {
                'items': cart['items'],
                'discount': cart['discount'],
                **totals
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/remove/<int:cart_item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_cart(cart_item_id):
    """Remove item from cart"""
    try:
        user_id = int(get_jwt_identity())
        cart = get_user_cart(user_id)
        
        # Remove item
        cart['items'] = [item for item in cart['items'] if item['cart_item_id'] != cart_item_id]
        
        totals = calculate_cart_totals(cart)
        
        return jsonify({
            'message': 'Item removed from cart',
            'cart': {
                'items': cart['items'],
                'discount': cart['discount'],
                **totals
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/discount', methods=['POST'])
@jwt_required()
def apply_discount():
    """
    Apply discount to cart
    
    Request body:
        type: 'percentage' or 'fixed'
        amount: float
        manager_override: bool (required for discounts > 20%)
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        discount_type = data.get('type')
        amount = float(data.get('amount', 0))
        
        if discount_type not in ['percentage', 'fixed', None]:
            return jsonify({'error': 'Invalid discount type'}), 400
        
        # Check if manager override is required for large discounts
        if discount_type == 'percentage' and amount > 20:
            manager_override = data.get('manager_override')
            if not manager_override:
                return jsonify({
                    'error': 'Manager override required for discounts over 20%',
                    'requires_override': True
                }), 403
        
        cart = get_user_cart(user_id)
        
        if discount_type is None or amount == 0:
            # Remove discount
            cart['discount'] = {'type': None, 'amount': 0}
        else:
            cart['discount'] = {'type': discount_type, 'amount': amount}
        
        totals = calculate_cart_totals(cart)
        
        return jsonify({
            'message': 'Discount applied',
            'cart': {
                'items': cart['items'],
                'discount': cart['discount'],
                **totals
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cart_bp.route('/clear', methods=['DELETE'])
@jwt_required()
def clear_cart():
    """Clear all items from cart"""
    try:
        user_id = int(get_jwt_identity())
        cart_key = get_cart_key(user_id)
        
        if cart_key in carts:
            del carts[cart_key]
        
        return jsonify({'message': 'Cart cleared'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
