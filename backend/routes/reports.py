from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from models.user import db
from models.transaction import Transaction
from models.product import Product
from models.inventory import InventoryLog, AuditLog
from utils.pdf_generator import PDFGenerator
import csv
import os

reports_bp = Blueprint('reports', __name__, url_prefix='/api/reports')


@reports_bp.route('/sales', methods=['GET'])
@jwt_required()
def get_sales_report():
    """
    Generate sales report
    
    Query params:
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        cashier_id: int (optional)
        category: str (optional)
    """
    try:
        # Parse query parameters
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        cashier_id = request.args.get('cashier_id', type=int)
        category = request.args.get('category')
        
        # Default to today if not provided
        if not start_date_str:
            start_date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        
        if not end_date_str:
            end_date = datetime.utcnow()
        else:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        
        # Build query
        query = Transaction.query.filter(
            Transaction.created_at >= start_date,
            Transaction.created_at <= end_date
        )
        
        if cashier_id:
            query = query.filter_by(user_id=cashier_id)
        
        transactions = query.all()
        
        # Filter by category if specified
        if category:
            filtered_transactions = []
            for trans in transactions:
                has_category = any(
                    item.product.category == category 
                    for item in trans.items 
                    if item.product
                )
                if has_category:
                    filtered_transactions.append(trans)
            transactions = filtered_transactions
        
        # Calculate statistics
        total_transactions = len(transactions)
        completed_transactions = [t for t in transactions if t.status == 'completed']
        sales_transactions = [t for t in completed_transactions if t.transaction_type == 'sale']
        refund_transactions = [t for t in completed_transactions if t.transaction_type == 'refund']
        
        total_sales = sum(t.total_amount for t in sales_transactions)
        total_refunds = sum(abs(t.total_amount) for t in refund_transactions)
        net_sales = total_sales - total_refunds
        
        total_tax = sum(t.tax_amount for t in sales_transactions)
        total_discounts = sum(t.discount_amount for t in sales_transactions)
        
        # Payment method breakdown
        payment_methods = {}
        for trans in sales_transactions:
            method = trans.payment_method or 'unknown'
            if method not in payment_methods:
                payment_methods[method] = {'count': 0, 'total': 0}
            payment_methods[method]['count'] += 1
            payment_methods[method]['total'] += trans.total_amount
        
        # Top products
        product_sales = {}
        for trans in sales_transactions:
            for item in trans.items:
                if item.product_id not in product_sales:
                    product_sales[item.product_id] = {
                        'product_id': item.product_id,
                        'name': item.product.name if item.product else 'Unknown',
                        'quantity': 0,
                        'revenue': 0
                    }
                product_sales[item.product_id]['quantity'] += item.quantity
                product_sales[item.product_id]['revenue'] += item.line_total
        
        top_products = sorted(product_sales.values(), key=lambda x: x['revenue'], reverse=True)[:10]
        
        # Cashier performance
        cashier_sales = {}
        for trans in sales_transactions:
            cashier_id = trans.user_id
            if cashier_id not in cashier_sales:
                cashier_sales[cashier_id] = {
                    'cashier_id': cashier_id,
                    'name': trans.user.full_name if trans.user else 'Unknown',
                    'transaction_count': 0,
                    'total_sales': 0
                }
            cashier_sales[cashier_id]['transaction_count'] += 1
            cashier_sales[cashier_id]['total_sales'] += trans.total_amount
        
        return jsonify({
            'report': {
                'period': {
                    'start': start_date.isoformat(),
                    'end': end_date.isoformat()
                },
                'summary': {
                    'total_transactions': total_transactions,
                    'completed_transactions': len(completed_transactions),
                    'sales_count': len(sales_transactions),
                    'refunds_count': len(refund_transactions),
                    'total_sales': round(total_sales, 2),
                    'total_refunds': round(total_refunds, 2),
                    'net_sales': round(net_sales, 2),
                    'total_tax': round(total_tax, 2),
                    'total_discounts': round(total_discounts, 2),
                    'average_transaction': round(total_sales / len(sales_transactions), 2) if sales_transactions else 0
                },
                'payment_methods': payment_methods,
                'top_products': top_products,
                'cashier_performance': list(cashier_sales.values())
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/inventory', methods=['GET'])
@jwt_required()
def get_inventory_report():
    """
    Generate inventory report
    
    Query params:
        category: str (optional)
        low_stock: bool (optional)
    """
    try:
        category = request.args.get('category')
        low_stock = request.args.get('low_stock', 'false').lower() == 'true'
        
        query = Product.query.filter_by(is_active=True)
        
        if category:
            query = query.filter_by(category=category)
        
        products = query.all()
        
        if low_stock:
            products = [p for p in products if p.needs_reorder()]
        
        # Calculate statistics
        total_products = len(products)
        total_value = sum(p.stock_quantity * p.cost for p in products if p.cost)
        low_stock_count = sum(1 for p in products if p.needs_reorder())
        out_of_stock_count = sum(1 for p in products if p.stock_quantity == 0)
        
        # Category breakdown
        categories = {}
        for product in products:
            cat = product.category or 'Uncategorized'
            if cat not in categories:
                categories[cat] = {
                    'count': 0,
                    'total_quantity': 0,
                    'total_value': 0
                }
            categories[cat]['count'] += 1
            categories[cat]['total_quantity'] += product.stock_quantity
            if product.cost:
                categories[cat]['total_value'] += product.stock_quantity * product.cost
        
        return jsonify({
            'report': {
                'summary': {
                    'total_products': total_products,
                    'total_inventory_value': round(total_value, 2),
                    'low_stock_items': low_stock_count,
                    'out_of_stock_items': out_of_stock_count
                },
                'categories': categories,
                'products': [p.to_dict() for p in products]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/history', methods=['GET'])
@jwt_required()
def get_sales_history():
    """
    Get sales history with search and filtering
    
    Query params:
        search: str (transaction number, product name)
        start_date: YYYY-MM-DD
        end_date: YYYY-MM-DD
        status: str
        limit: int
        offset: int
    """
    try:
        search = request.args.get('search')
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        status = request.args.get('status')
        limit = request.args.get('limit', default=50, type=int)
        offset = request.args.get('offset', default=0, type=int)
        
        query = Transaction.query
        
        if search:
            query = query.filter(
                Transaction.transaction_number.ilike(f'%{search}%')
            )
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            query = query.filter(Transaction.created_at >= start_date)
        
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            query = query.filter(Transaction.created_at <= end_date)
        
        if status:
            query = query.filter_by(status=status)
        
        # Get total count
        total_count = query.count()
        
        # Get paginated results
        transactions = query.order_by(Transaction.created_at.desc()).limit(limit).offset(offset).all()
        
        return jsonify({
            'transactions': [t.to_dict(include_items=True) for t in transactions],
            'pagination': {
                'total': total_count,
                'limit': limit,
                'offset': offset,
                'has_more': (offset + limit) < total_count
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/export', methods=['POST'])
@jwt_required()
def export_report():
    """
    Export report as PDF or CSV
    
    Request body:
        report_type: 'sales' or 'inventory'
        format: 'pdf' or 'csv'
        start_date: YYYY-MM-DD (for sales)
        end_date: YYYY-MM-DD (for sales)
    """
    try:
        data = request.get_json()
        report_type = data.get('report_type')
        export_format = data.get('format', 'pdf')
        
        if report_type == 'sales':
            start_date_str = data.get('start_date')
            end_date_str = data.get('end_date')
            
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else datetime.utcnow().replace(hour=0, minute=0, second=0)
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else datetime.utcnow()
            
            transactions = Transaction.query.filter(
                Transaction.created_at >= start_date,
                Transaction.created_at <= end_date,
                Transaction.status == 'completed'
            ).all()
            
            if export_format == 'pdf':
                filepath = PDFGenerator.generate_sales_report(transactions, start_date, end_date)
                return jsonify({
                    'message': 'Report generated',
                    'filepath': filepath
                }), 200
            elif export_format == 'csv':
                # Generate CSV
                filename = f"sales_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                filepath = os.path.join('receipts', filename)
                os.makedirs('receipts', exist_ok=True)
                
                with open(filepath, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Transaction Number', 'Date', 'Cashier', 'Type', 'Subtotal', 'Discount', 'Tax', 'Total', 'Payment Method'])
                    
                    for trans in transactions:
                        writer.writerow([
                            trans.transaction_number,
                            trans.created_at.strftime('%Y-%m-%d %H:%M:%S') if trans.created_at else '',
                            trans.user.full_name if trans.user else '',
                            trans.transaction_type,
                            trans.subtotal,
                            trans.discount_amount,
                            trans.tax_amount,
                            trans.total_amount,
                            trans.payment_method
                        ])
                
                return jsonify({
                    'message': 'Report generated',
                    'filepath': filepath
                }), 200
        
        return jsonify({'error': 'Invalid report type or format'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@reports_bp.route('/audit-log', methods=['GET'])
@jwt_required()
def get_audit_log():
    """Get audit log entries (Admin/Manager only)"""
    try:
        limit = request.args.get('limit', default=100, type=int)
        user_id = request.args.get('user_id', type=int)
        action = request.args.get('action')
        
        query = AuditLog.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        if action:
            query = query.filter_by(action=action)
        
        logs = query.order_by(AuditLog.timestamp.desc()).limit(limit).all()
        
        return jsonify({
            'logs': [log.to_dict() for log in logs],
            'count': len(logs)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
