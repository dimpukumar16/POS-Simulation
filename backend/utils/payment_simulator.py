import random
import time
from datetime import datetime


class PaymentSimulator:
    """Mock payment gateway simulator"""
    
    # Payment success rates for different methods
    SUCCESS_RATES = {
        'cash': 1.0,  # Cash always succeeds
        'card': 0.95,  # Card has 95% success rate
        'upi': 0.92   # UPI has 92% success rate
    }
    
    # Simulated processing times (in seconds)
    PROCESSING_TIMES = {
        'cash': 0.1,
        'card': 0.5,
        'upi': 0.7
    }
    
    @staticmethod
    def process_payment(payment_method, amount, reference=None):
        """
        Simulate payment processing
        
        Args:
            payment_method: 'cash', 'card', or 'upi'
            amount: Payment amount
            reference: Optional payment reference (card number, UPI ID, etc.)
        
        Returns:
            dict: Payment result with status, reference, and details
        """
        # Validate payment method
        if payment_method not in PaymentSimulator.SUCCESS_RATES:
            return {
                'success': False,
                'status': 'failed',
                'message': f'Invalid payment method: {payment_method}',
                'reference': None,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        # Validate amount
        if amount <= 0:
            return {
                'success': False,
                'status': 'failed',
                'message': 'Invalid payment amount',
                'reference': None,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        # Simulate processing time
        processing_time = PaymentSimulator.PROCESSING_TIMES[payment_method]
        time.sleep(processing_time)
        
        # Determine success based on success rate
        success_rate = PaymentSimulator.SUCCESS_RATES[payment_method]
        is_successful = random.random() < success_rate
        
        # Generate payment reference
        if not reference:
            reference = PaymentSimulator._generate_reference(payment_method)
        
        if is_successful:
            return {
                'success': True,
                'status': 'approved',
                'message': f'{payment_method.upper()} payment successful',
                'reference': reference,
                'amount': amount,
                'timestamp': datetime.utcnow().isoformat()
            }
        else:
            # Generate appropriate error message
            error_message = PaymentSimulator._generate_error_message(payment_method)
            return {
                'success': False,
                'status': 'declined',
                'message': error_message,
                'reference': reference,
                'amount': amount,
                'timestamp': datetime.utcnow().isoformat()
            }
    
    @staticmethod
    def process_cash_payment(amount_paid, total_amount):
        """
        Process cash payment with change calculation
        
        Args:
            amount_paid: Amount paid by customer
            total_amount: Total amount due
        
        Returns:
            dict: Payment result with change calculation
        """
        if amount_paid < total_amount:
            return {
                'success': False,
                'status': 'failed',
                'message': f'Insufficient payment. Required: ${total_amount:.2f}, Paid: ${amount_paid:.2f}',
                'reference': None,
                'timestamp': datetime.utcnow().isoformat()
            }
        
        change = amount_paid - total_amount
        reference = PaymentSimulator._generate_reference('cash')
        
        return {
            'success': True,
            'status': 'approved',
            'message': 'Cash payment successful',
            'reference': reference,
            'amount': total_amount,
            'amount_paid': amount_paid,
            'change': round(change, 2),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def process_refund(original_payment_method, amount, original_reference=None):
        """
        Simulate refund processing
        
        Args:
            original_payment_method: Payment method used in original transaction
            amount: Refund amount
            original_reference: Reference from original transaction
        
        Returns:
            dict: Refund result
        """
        # Refunds have higher success rate
        time.sleep(0.3)
        
        # Generate refund reference
        refund_reference = f"REF-{PaymentSimulator._generate_reference(original_payment_method)}"
        
        return {
            'success': True,
            'status': 'approved',
            'message': f'Refund processed successfully to {original_payment_method}',
            'reference': refund_reference,
            'original_reference': original_reference,
            'amount': amount,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def _generate_reference(payment_method):
        """Generate a unique payment reference"""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        prefixes = {
            'cash': 'CASH',
            'card': 'CARD',
            'upi': 'UPI'
        }
        
        prefix = prefixes.get(payment_method, 'PAY')
        return f"{prefix}-{timestamp}-{random_suffix}"
    
    @staticmethod
    def _generate_error_message(payment_method):
        """Generate realistic error messages"""
        error_messages = {
            'card': [
                'Card declined by issuer',
                'Insufficient funds',
                'Card expired',
                'Transaction limit exceeded',
                'Invalid card number'
            ],
            'upi': [
                'UPI PIN incorrect',
                'Transaction timeout',
                'UPI service unavailable',
                'Account balance insufficient',
                'Transaction declined by bank'
            ],
            'cash': [
                'Payment processing error'
            ]
        }
        
        messages = error_messages.get(payment_method, ['Payment processing error'])
        return random.choice(messages)
    
    @staticmethod
    def validate_card_number(card_number):
        """Simple Luhn algorithm for card validation (for demonstration)"""
        if not card_number or len(card_number) < 13 or len(card_number) > 19:
            return False
        
        try:
            # Remove spaces and dashes
            card_number = card_number.replace(' ', '').replace('-', '')
            
            # Check if all digits
            if not card_number.isdigit():
                return False
            
            # Luhn algorithm
            digits = [int(d) for d in card_number]
            checksum = 0
            
            for i, digit in enumerate(reversed(digits)):
                if i % 2 == 1:
                    digit *= 2
                    if digit > 9:
                        digit -= 9
                checksum += digit
            
            return checksum % 10 == 0
        except:
            return False
    
    @staticmethod
    def validate_upi_id(upi_id):
        """Validate UPI ID format"""
        if not upi_id:
            return False
        
        # Basic UPI ID format: username@bankname
        parts = upi_id.split('@')
        if len(parts) != 2:
            return False
        
        username, bank = parts
        return len(username) > 0 and len(bank) > 0
