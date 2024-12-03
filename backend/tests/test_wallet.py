import pytest
from flask import Flask
from flask_jwt_extended import create_access_token
from main import app, db

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Ensure test DB is initialized
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

@pytest.fixture
def admin_token():
    with app.app_context():
        token = create_access_token(identity='admin@gmail.com')
    return token

@pytest.fixture
def non_admin_token():
    with app.app_context():
        token = create_access_token(identity='user@gmail.com')
    return token

# --- Tests for `/wallets` Route ---
def test_get_all_wallets_admin(client, admin_token):
    response = client.get('/api/admin/wallets', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_all_wallets_unauthorized(client, non_admin_token):
    response = client.get('/api/admin/wallets', headers={'Authorization': f'Bearer {non_admin_token}'})
    assert response.status_code == 403
    assert response.json['message'] == 'Unauthorized'

def test_get_all_wallets_no_token(client):
    response = client.get('/api/admin/wallets')
    assert response.status_code == 401  # No JWT provided

# --- Tests for `/transactions` Route ---
def test_get_all_transactions_admin(client, admin_token):
    response = client.get('/api/admin/transactions', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_all_transactions_unauthorized(client, non_admin_token):
    response = client.get('/api/admin/transactions', headers={'Authorization': f'Bearer {non_admin_token}'})
    assert response.status_code == 403
    assert response.json['message'] == 'Unauthorized'

# --- Tests for `/analytics` Route ---
def test_get_analytics_admin(client, admin_token):
    response = client.get('/api/admin/analytics', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert 'total_money_added' in response.json
    assert 'total_transactions' in response.json
    assert 'top_wallets' in response.json

def test_get_analytics_unauthorized(client, non_admin_token):
    response = client.get('/api/admin/analytics', headers={'Authorization': f'Bearer {non_admin_token}'})
    assert response.status_code == 403
    assert response.json['message'] == 'Unauthorized'
