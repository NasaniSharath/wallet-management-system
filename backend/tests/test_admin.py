import pytest
from unittest.mock import patch
from flask_jwt_extended import create_access_token
from main import app  # Your Flask app factory function
from models import User, Transaction

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def admin_token():
    return create_access_token(identity='admin@gmail.com')

# Test for /wallets endpoint
def test_get_all_wallets_authorized(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}

    # Mock database query results
    mock_wallets = [
        User(wallet_id='1', name='User1', balance=100.0),
        User(wallet_id='2', name='User2', balance=200.0)
    ]

    with patch('models.User.query') as mock_query:
        mock_query.all.return_value = mock_wallets
        response = client.get('/wallets', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert len(data) == 2
        assert data[0]['name'] == 'User1'

# Test for /transactions endpoint
def test_get_all_transactions_authorized(client, admin_token):
    headers = {'Authorization': f'Bearer {admin_token}'}
    
    mock_transactions = [
        Transaction(wallet_id='1', transaction_type='Add Money', amount=50.0, timestamp='2023-11-10T10:00:00'),
    ]

    with patch('models.Transaction.query.order_by') as mock_query:
        mock_query.return_value.all.return_value = mock_transactions
        response = client.get('/transactions', headers=headers)
        assert response.status_code == 200
        data = response.get_json()
        assert data[0]['type'] == 'Add Money'

# Test for unauthorized access
def test_get_wallets_unauthorized(client):
    response = client.get('/wallets')
    assert response.status_code == 401  # No token provided
