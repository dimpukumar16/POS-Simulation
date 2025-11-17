import pytest
from test_auth import client, get_auth_headers


def test_add_to_cart(client):
    """Test adding item to cart"""
    headers = get_auth_headers(client)
    
    response = client.post('/api/cart/add', 
        headers=headers,
        json={
            'barcode': 'TEST123',
            'quantity': 2
        }
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['cart']['item_count'] == 1
    assert data['cart']['items'][0]['quantity'] == 2


def test_get_cart(client):
    """Test getting cart"""
    headers = get_auth_headers(client)
    
    # Add item first
    client.post('/api/cart/add', 
        headers=headers,
        json={'barcode': 'TEST123', 'quantity': 1}
    )
    
    # Get cart
    response = client.get('/api/cart', headers=headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'cart' in data
    assert len(data['cart']['items']) > 0


def test_update_cart_quantity(client):
    """Test updating cart item quantity"""
    headers = get_auth_headers(client)
    
    # Add item
    response = client.post('/api/cart/add', 
        headers=headers,
        json={'barcode': 'TEST123', 'quantity': 1}
    )
    cart_item_id = response.get_json()['cart']['items'][0]['cart_item_id']
    
    # Update quantity
    response = client.put('/api/cart/update',
        headers=headers,
        json={'cart_item_id': cart_item_id, 'quantity': 5}
    )
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['cart']['items'][0]['quantity'] == 5


def test_remove_from_cart(client):
    """Test removing item from cart"""
    headers = get_auth_headers(client)
    
    # Add item
    response = client.post('/api/cart/add',
        headers=headers,
        json={'barcode': 'TEST123', 'quantity': 1}
    )
    cart_item_id = response.get_json()['cart']['items'][0]['cart_item_id']
    
    # Remove item
    response = client.delete(f'/api/cart/remove/{cart_item_id}', headers=headers)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['cart']['item_count'] == 0


def test_clear_cart(client):
    """Test clearing cart"""
    headers = get_auth_headers(client)
    
    # Add items
    client.post('/api/cart/add',
        headers=headers,
        json={'barcode': 'TEST123', 'quantity': 2}
    )
    
    # Clear cart
    response = client.delete('/api/cart/clear', headers=headers)
    
    assert response.status_code == 200


def test_add_invalid_product(client):
    """Test adding non-existent product"""
    headers = get_auth_headers(client)
    
    response = client.post('/api/cart/add',
        headers=headers,
        json={'barcode': 'INVALID', 'quantity': 1}
    )
    
    assert response.status_code == 404
