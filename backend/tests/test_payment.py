import pytest
from test_auth import client, get_auth_headers


def test_process_cash_payment(client):
    """Test processing cash payment"""
    headers = get_auth_headers(client)
    
    # Add item to cart
    client.post('/api/cart/add',
        headers=headers,
        json={'barcode': 'TEST123', 'quantity': 1}
    )
    
    # Get cart total
    cart_response = client.get('/api/cart', headers=headers)
    total = cart_response.get_json()['cart']['total']
    
    # Process payment
    response = client.post('/api/checkout/process',
        headers=headers,
        json={
            'payment_method': 'cash',
            'amount_paid': total + 10
        }
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['transaction']['status'] == 'completed'
    assert data['payment_result']['success'] is True
    assert float(data['payment_result']['change']) >= 0


def test_process_card_payment(client):
    """Test processing card payment"""
    headers = get_auth_headers(client)
    
    # Add item to cart
    client.post('/api/cart/add',
        headers=headers,
        json={'barcode': 'TEST123', 'quantity': 1}
    )
    
    # Process payment
    response = client.post('/api/checkout/process',
        headers=headers,
        json={
            'payment_method': 'card',
            'payment_reference': '4532123456789012'
        }
    )
    
    # Card payment may succeed or fail in simulation
    assert response.status_code in [200, 402]


def test_process_empty_cart(client):
    """Test processing payment with empty cart"""
    headers = get_auth_headers(client)
    
    # Clear cart first
    client.delete('/api/cart/clear', headers=headers)
    
    # Try to process payment
    response = client.post('/api/checkout/process',
        headers=headers,
        json={
            'payment_method': 'cash',
            'amount_paid': 100
        }
    )
    
    assert response.status_code == 400


def test_insufficient_cash_payment(client):
    """Test insufficient cash payment"""
    headers = get_auth_headers(client)
    
    # Add item to cart
    client.post('/api/cart/add',
        headers=headers,
        json={'barcode': 'TEST123', 'quantity': 1}
    )
    
    # Process payment with insufficient amount
    response = client.post('/api/checkout/process',
        headers=headers,
        json={
            'payment_method': 'cash',
            'amount_paid': 1.00
        }
    )
    
    assert response.status_code == 402
