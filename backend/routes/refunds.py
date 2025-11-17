from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from models.user import db, User
from models.product import Product
from models.transaction import Transaction, TransactionItem
from models.refund import Refund
from models.inventory import InventoryLog
from utils.logger import AuditLogger

refund_bp = Blueprint('refund', __name__, url_prefix='/api/refunds')


def generate_refund_number():
    """Generate unique refund number"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return f"REF-{timestamp}"


def has_permission(role, permission):
    """Check if role has permission"""
    permissions = {
        'administrator': ['all'],
        'manager': ['refund', 'void', 'override', 'reports', 'sales'],
        'cashier': ['sales']
    }
    return 'all' in permissions.get(role, []) or permission in permissions.get(role, [])


@refund_bp.route('', methods=['GET'])
@jwt_required()
def get_refunds():
    """
    Get all refunds (manager/admin only)
    
    Query parameters:
        from: ISO datetime (optional)
        to: ISO datetime (optional)
        transaction_id: int (optional)
        status: str (optional)
    """
    try:
        # Get user info from JWT
        jwt_data = get_jwt()
        user_role = jwt_data.get('role', 'cashier')
        
        # Check permissions
        if not has_permission(user_role, 'refund'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        # Build query
        query = Refund.query
        
        # Apply filters
        transaction_id = request.args.get('transaction_id')
        if transaction_id:
            query = query.filter_by(transaction_id=int(transaction_id))
        
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        from_date = request.args.get('from')
        if from_date:
            query = query.filter(Refund.created_at >= datetime.fromisoformat(from_date))
        
        to_date = request.args.get('to')
        if to_date:
            query = query.filter(Refund.created_at <= datetime.fromisoformat(to_date))
        
        # Execute query
        refunds = query.order_by(Refund.created_at.desc()).all()
        
        return jsonify({
            'refunds': [refund.to_dict() for refund in refunds],
            'count': len(refunds)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@refund_bp.route('/<int:refund_id>', methods=['GET'])
@jwt_required()
def get_refund(refund_id):
    """Get refund details by ID"""
    try:
        # Get user info from JWT
        jwt_data = get_jwt()
        user_role = jwt_data.get('role', 'cashier')
        
        # Check permissions
        if not has_permission(user_role, 'refund'):
            return jsonify({'error': 'Insufficient permissions'}), 403
        
        refund = Refund.query.get(refund_id)
        
        if not refund:
            return jsonify({'error': 'Refund not found'}), 404
        
        return jsonify({'refund': refund.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@refund_bp.route('/transaction/<int:transaction_id>', methods=['POST'])
@jwt_required()
def create_refund(transaction_id):
    """
    Create a refund for a transaction (manager/admin only)
    
    Request body:
        reason: str
        amount_cents: int (optional, defaults to full transaction amount)
        refund_method: str (optional, defaults to 'original_method')
        items: list of {item_id: int, quantity: int} (optional, for partial refunds)
    """
    try:
        # Get user info from JWT
        user_id = int(get_jwt_identity())
        jwt_data = get_jwt()
        user_role = jwt_data.get('role', 'cashier')
        
        # Check permissions (manager or admin only)
        if not has_permission(user_role, 'refund'):
            return jsonify({'error': 'Insufficient permissions. Manager or administrator role required.'}), 403
        
        # Get request data
        data = request.get_json()
        reason = data.get('reason', 'Customer request')
        amount_cents = data.get('amount_cents')
        refund_method = data.get('refund_method', 'original_method')
        items_to_refund = data.get('items', [])  # For partial refunds
        
        # Get transaction
        transaction = Transaction.query.get(transaction_id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        if transaction.status == 'voided':
            return jsonify({'error': 'Cannot refund a voided transaction'}), 400
        
        # Check if transaction already fully refunded
        existing_refunds = Refund.query.filter_by(transaction_id=transaction_id, status='completed').all()
        total_refunded = sum(r.amount_cents for r in existing_refunds)
        
        # Calculate refund amount
        transaction_total_cents = int(transaction.total_amount * 100)
        
        if amount_cents is None:
            # Full refund
            amount_cents = transaction_total_cents - total_refunded
        else:
            amount_cents = int(amount_cents)
        
        # Validate refund amount
        if amount_cents <= 0:
            return jsonify({'error': 'Invalid refund amount'}), 400
        
        if total_refunded + amount_cents > transaction_total_cents:
            return jsonify({'error': f'Refund amount exceeds transaction total. Already refunded: ${total_refunded/100:.2f}'}), 400
        
        # Start database transaction
        try:
            # Create refund record
            refund = Refund(
                transaction_id=transaction_id,
                refund_number=generate_refund_number(),
                amount_cents=amount_cents,
                refunded_by=user_id,
                reason=reason,
                refund_method=refund_method if refund_method != 'original_method' else transaction.payment_method,
                status='pending'
            )
            
            db.session.add(refund)
            db.session.flush()  # Get refund ID
            
            # Restock inventory for refunded items
            if items_to_refund:
                # Partial refund - restock only specified items
                for item_data in items_to_refund:
                    item_id = item_data.get('item_id')
                    quantity = item_data.get('quantity', 0)
                    
                    transaction_item = TransactionItem.query.get(item_id)
                    if not transaction_item or transaction_item.transaction_id != transaction_id:
                        raise ValueError(f'Invalid transaction item: {item_id}')
                    
                    if quantity > transaction_item.quantity:
                        raise ValueError(f'Refund quantity exceeds original quantity for item {item_id}')
                    
                    product = Product.query.get(transaction_item.product_id)
                    if product:
                        old_qty = product.stock_quantity
                        product.stock_quantity += quantity
                        
                        # Log inventory change
                        inventory_log = InventoryLog(
                            product_id=product.id,
                            user_id=user_id,
                            change_type='refund',
                            quantity_before=old_qty,
                            quantity_change=quantity,
                            quantity_after=product.stock_quantity,
                            reference_type='refund',
                            reference_id=refund.id,
                            notes=f'Refund {refund.refund_number}: {reason}'
                        )
                        db.session.add(inventory_log)
            else:
                # Full refund - restock all items
                for transaction_item in transaction.items:
                    product = Product.query.get(transaction_item.product_id)
                    if product:
                        old_qty = product.stock_quantity
                        product.stock_quantity += transaction_item.quantity
                        
                        # Log inventory change
                        inventory_log = InventoryLog(
                            product_id=product.id,
                            user_id=user_id,
                            change_type='refund',
                            quantity_before=old_qty,
                            quantity_change=transaction_item.quantity,
                            quantity_after=product.stock_quantity,
                            reference_type='refund',
                            reference_id=refund.id,
                            notes=f'Refund {refund.refund_number}: {reason}'
                        )
                        db.session.add(inventory_log)
            
            # Update refund status
            refund.status = 'completed'
            refund.completed_at = datetime.utcnow()
            
            # Update transaction status if fully refunded
            if total_refunded + amount_cents >= transaction_total_cents:
                transaction.status = 'refunded'
            
            # Commit transaction
            db.session.commit()
            
            # Log refund action
            AuditLogger.log(
                user_id=user_id,
                action='create_refund',
                resource_type='refund',
                resource_id=refund.id,
                details=f'Refund {refund.refund_number} for transaction {transaction.transaction_number}: ${refund.amount:.2f}. Reason: {reason}',
                ip_address=request.remote_addr
            )
            
            return jsonify({
                'message': 'Refund processed successfully',
                'refund': refund.to_dict(),
                'transaction': transaction.to_dict(include_items=False)
            }), 201
            
        except ValueError as ve:
            db.session.rollback()
            return jsonify({'error': str(ve)}), 400
        except Exception as e:
            db.session.rollback()
            raise e
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@refund_bp.route('/<int:refund_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_refund(refund_id):
    """
    Cancel a pending refund (admin only)
    """
    try:
        # Get user info from JWT
        user_id = int(get_jwt_identity())
        jwt_data = get_jwt()
        user_role = jwt_data.get('role', 'cashier')
        
        # Check permissions (admin only)
        if user_role != 'administrator':
            return jsonify({'error': 'Insufficient permissions. Administrator role required.'}), 403
        
        refund = Refund.query.get(refund_id)
        
        if not refund:
            return jsonify({'error': 'Refund not found'}), 404
        
        if refund.status != 'pending':
            return jsonify({'error': 'Can only cancel pending refunds'}), 400
        
        refund.status = 'failed'
        db.session.commit()
        
        # Log cancellation
        AuditLogger.log(
            user_id=user_id,
            action='cancel_refund',
            resource_type='refund',
            resource_id=refund.id,
            details=f'Cancelled refund {refund.refund_number}',
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Refund cancelled successfully',
            'refund': refund.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
