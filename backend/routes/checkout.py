from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import datetime
from models.user import db, User
from models.product import Product
from models.transaction import Transaction, TransactionItem
from models.inventory import InventoryLog
from utils.payment_simulator import PaymentSimulator
from utils.pdf_generator import PDFGenerator
from utils.logger import AuditLogger
from routes.cart import get_user_cart, get_cart_key, carts, calculate_cart_totals

checkout_bp = Blueprint('checkout', __name__, url_prefix='/api/checkout')


def generate_transaction_number():
    """Generate unique transaction number"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    return f"TXN-{timestamp}"


@checkout_bp.route('/process', methods=['POST'])
@jwt_required()
def process_checkout():
    """
    Process checkout and payment
    
    Request body:
        payment_method: 'cash', 'card', or 'upi'
        amount_paid: float (for cash)
        payment_reference: str (optional, for card/upi)
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        payment_method = data.get('payment_method')
        amount_paid = float(data.get('amount_paid', 0))
        payment_reference = data.get('payment_reference')
        
        if not payment_method:
            return jsonify({'error': 'Payment method is required'}), 400
        
        # Get cart
        cart = get_user_cart(user_id)
        
        if not cart['items']:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate totals
        totals = calculate_cart_totals(cart)
        total_amount = totals['total']
        
        # Start transaction
        transaction_number = generate_transaction_number()
        
        # Create transaction record
        transaction = Transaction(
            transaction_number=transaction_number,
            user_id=user_id,
            transaction_type='sale',
            status='pending',
            subtotal=totals['subtotal'],
            discount_amount=totals['discount_amount'],
            discount_type=totals['discount_type'],
            tax_amount=totals['tax_amount'],
            total_amount=total_amount,
            payment_method=payment_method
        )
        
        db.session.add(transaction)
        db.session.flush()  # Get transaction ID
        
        # Add transaction items
        for cart_item in cart['items']:
            product = Product.query.get(cart_item['product_id'])
            
            # Final stock check
            if not product.is_in_stock(cart_item['quantity']):
                db.session.rollback()
                return jsonify({
                    'error': f'Insufficient stock for {product.name}',
                    'available': product.stock_quantity
                }), 400
            
            trans_item = TransactionItem(
                transaction_id=transaction.id,
                product_id=product.id,
                quantity=cart_item['quantity'],
                unit_price=cart_item['unit_price'],
                discount_amount=cart_item.get('item_discount', 0),
                tax_rate=cart_item['tax_rate'],
                tax_amount=cart_item['tax_amount'],
                line_total=cart_item['line_total']
            )
            
            db.session.add(trans_item)
        
        # Process payment
        payment_result = None
        
        if payment_method == 'cash':
            payment_result = PaymentSimulator.process_cash_payment(amount_paid, total_amount)
        else:
            payment_result = PaymentSimulator.process_payment(payment_method, total_amount, payment_reference)
        
        if not payment_result['success']:
            db.session.rollback()
            return jsonify({
                'error': 'Payment failed',
                'payment_result': payment_result
            }), 402
        
        # Payment successful - update transaction
        transaction.status = 'completed'
        transaction.payment_reference = payment_result['reference']
        transaction.amount_paid = payment_result.get('amount_paid', total_amount)
        transaction.change_given = payment_result.get('change', 0)
        transaction.completed_at = datetime.utcnow()
        
        # Update inventory
        for cart_item in cart['items']:
            product = Product.query.get(cart_item['product_id'])
            old_quantity = product.stock_quantity
            product.update_stock(-cart_item['quantity'])
            
            # Log inventory change
            inv_log = InventoryLog(
                product_id=product.id,
                user_id=user_id,
                change_type='sale',
                quantity_before=old_quantity,
                quantity_change=-cart_item['quantity'],
                quantity_after=product.stock_quantity,
                reference_type='transaction',
                reference_id=transaction.id
            )
            db.session.add(inv_log)
        
        # Commit all changes
        db.session.commit()
        
        # Log transaction
        AuditLogger.log_transaction_action(
            user_id=user_id,
            action='process_sale',
            transaction_id=transaction.id,
            details=f"Completed sale: {transaction_number}, Total: ${total_amount:.2f}",
            ip_address=request.remote_addr
        )
        
        # Generate receipt PDF
        try:
            receipt_path = PDFGenerator.generate_receipt(transaction)
        except Exception as e:
            print(f"Error generating receipt: {str(e)}")
            receipt_path = None
        
        # Clear cart
        cart_key = get_cart_key(user_id)
        if cart_key in carts:
            del carts[cart_key]
        
        return jsonify({
            'message': 'Payment successful',
            'transaction': transaction.to_dict(),
            'payment_result': payment_result,
            'receipt_path': receipt_path
        }), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@checkout_bp.route('/refund', methods=['POST'])
@jwt_required()
def process_refund():
    """
    Process refund (requires manager authorization)
    
    Request body:
        transaction_id: int
        reason: str
        manager_pin: str
    """
    try:
        user_id = int(get_jwt_identity())
        claims = get_jwt()
        data = request.get_json()
        
        transaction_id = data.get('transaction_id')
        reason = data.get('reason')
        manager_pin = data.get('manager_pin')
        
        if not transaction_id or not reason:
            return jsonify({'error': 'Transaction ID and reason are required'}), 400
        
        # Verify manager authorization
        if not manager_pin:
            return jsonify({'error': 'Manager PIN is required for refunds'}), 403
        
        manager = User.query.filter_by(pin=manager_pin, is_active=True).first()
        
        if not manager or manager.role not in ['manager', 'administrator']:
            return jsonify({'error': 'Invalid manager PIN or insufficient privileges'}), 403
        
        # Get original transaction
        original_transaction = Transaction.query.get(transaction_id)
        
        if not original_transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        if original_transaction.status not in ['completed']:
            return jsonify({'error': 'Cannot refund this transaction'}), 400
        
        if original_transaction.transaction_type == 'refund':
            return jsonify({'error': 'Cannot refund a refund transaction'}), 400
        
        # Create refund transaction
        refund_number = f"REF-{generate_transaction_number()}"
        
        refund_transaction = Transaction(
            transaction_number=refund_number,
            user_id=user_id,
            transaction_type='refund',
            status='completed',
            subtotal=-original_transaction.subtotal,
            discount_amount=-original_transaction.discount_amount,
            discount_type=original_transaction.discount_type,
            tax_amount=-original_transaction.tax_amount,
            total_amount=-original_transaction.total_amount,
            payment_method=original_transaction.payment_method,
            refund_reason=reason,
            authorized_by=manager.id,
            completed_at=datetime.utcnow()
        )
        
        db.session.add(refund_transaction)
        db.session.flush()
        
        # Create refund items and restore inventory
        for original_item in original_transaction.items:
            refund_item = TransactionItem(
                transaction_id=refund_transaction.id,
                product_id=original_item.product_id,
                quantity=original_item.quantity,
                unit_price=original_item.unit_price,
                discount_amount=original_item.discount_amount,
                tax_rate=original_item.tax_rate,
                tax_amount=original_item.tax_amount,
                line_total=original_item.line_total
            )
            db.session.add(refund_item)
            
            # Restore stock
            product = Product.query.get(original_item.product_id)
            old_quantity = product.stock_quantity
            product.update_stock(original_item.quantity)
            
            # Log inventory change
            inv_log = InventoryLog(
                product_id=product.id,
                user_id=user_id,
                change_type='refund',
                quantity_before=old_quantity,
                quantity_change=original_item.quantity,
                quantity_after=product.stock_quantity,
                reference_type='transaction',
                reference_id=refund_transaction.id,
                notes=f"Refund for transaction {original_transaction.transaction_number}"
            )
            db.session.add(inv_log)
        
        # Process refund payment
        refund_result = PaymentSimulator.process_refund(
            original_transaction.payment_method,
            original_transaction.total_amount,
            original_transaction.payment_reference
        )
        
        refund_transaction.payment_reference = refund_result['reference']
        
        db.session.commit()
        
        # Log refund
        AuditLogger.log_transaction_action(
            user_id=user_id,
            action='process_refund',
            transaction_id=refund_transaction.id,
            details=f"Refund processed by manager {manager.username}: {reason}",
            ip_address=request.remote_addr
        )
        
        AuditLogger.log_manager_override(
            manager_id=manager.id,
            action='refund',
            details=f"Authorized refund for transaction {original_transaction.transaction_number}",
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Refund processed successfully',
            'refund_transaction': refund_transaction.to_dict(),
            'refund_result': refund_result
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@checkout_bp.route('/void', methods=['POST'])
@jwt_required()
def void_transaction():
    """
    Void a transaction (requires manager authorization)
    
    Request body:
        transaction_id: int
        reason: str
        manager_pin: str
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        transaction_id = data.get('transaction_id')
        reason = data.get('reason')
        manager_pin = data.get('manager_pin')
        
        if not transaction_id or not reason:
            return jsonify({'error': 'Transaction ID and reason are required'}), 400
        
        # Verify manager authorization
        if not manager_pin:
            return jsonify({'error': 'Manager PIN is required for voids'}), 403
        
        manager = User.query.filter_by(pin=manager_pin, is_active=True).first()
        
        if not manager or manager.role not in ['manager', 'administrator']:
            return jsonify({'error': 'Invalid manager PIN or insufficient privileges'}), 403
        
        # Get transaction
        transaction = Transaction.query.get(transaction_id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        if transaction.status == 'voided':
            return jsonify({'error': 'Transaction is already voided'}), 400
        
        # Void transaction
        transaction.status = 'voided'
        transaction.refund_reason = reason
        transaction.authorized_by = manager.id
        
        # Restore inventory if transaction was completed
        if transaction.status == 'completed':
            for item in transaction.items:
                product = Product.query.get(item.product_id)
                old_quantity = product.stock_quantity
                product.update_stock(item.quantity)
                
                # Log inventory change
                inv_log = InventoryLog(
                    product_id=product.id,
                    user_id=user_id,
                    change_type='void',
                    quantity_before=old_quantity,
                    quantity_change=item.quantity,
                    quantity_after=product.stock_quantity,
                    reference_type='transaction',
                    reference_id=transaction.id,
                    notes=f"Voided transaction: {reason}"
                )
                db.session.add(inv_log)
        
        db.session.commit()
        
        # Log void
        AuditLogger.log_transaction_action(
            user_id=user_id,
            action='void_transaction',
            transaction_id=transaction.id,
            details=f"Transaction voided by manager {manager.username}: {reason}",
            ip_address=request.remote_addr
        )
        
        AuditLogger.log_manager_override(
            manager_id=manager.id,
            action='void',
            details=f"Authorized void for transaction {transaction.transaction_number}",
            ip_address=request.remote_addr
        )
        
        return jsonify({
            'message': 'Transaction voided successfully',
            'transaction': transaction.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
