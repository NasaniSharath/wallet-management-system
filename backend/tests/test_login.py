import pytest
from main import app, db
from models import User
from flask import json
# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client
# Pytest fixture to set up and tear down the test environment
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()

# Test the registration endpoint for success
def test_register_user_success(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "phone_number": "1234567890"
    }
    response = client.post('/api/register', data=json.dumps(payload), content_type='application/json')
    
    data = json.loads(response.data)
    assert "wallet_id" in data
    assert data["balance"] == 0.0
    assert "token" in data

# Test registration with missing fields
@pytest.mark.parametrize("missing_field", ["name", "email", "phone_number"])
def test_register_user_missing_fields(client, missing_field):
    payload = {"name": "Test User", "email": "test@example.com", "phone_number": "1234567890"}
    payload.pop(missing_field)
    response = client.post('/api/register', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Invalid" in data["message"]

# Test registration with an existing user
def test_register_existing_user(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "phone_number": "1234567890"
    }
    # Register the user first
    client.post('/api/register', data=json.dumps(payload), content_type='application/json')
    # Try to register the same user again
    response = client.post('/api/register', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 409
    data = json.loads(response.data)
    assert data["message"] == "User already Registered"

# Test login endpoint for success
def test_login_success(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "phone_number": "1234567890"
    }
    client.post('/api/register', data=json.dumps(payload), content_type='application/json')

    login_payload = {"email": "test@example.com"}
    response = client.post('/api/login', data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "token" in data
    assert data["wallet_id"] is not None

# Test login with unregistered email
def test_login_unregistered_email(client):
    login_payload = {"email": "unknown@example.com"}
    response = client.post('/api/login', data=json.dumps(login_payload), content_type='application/json')
    assert response.status_code == 400

# Test login with missing email field
def test_login_missing_email(client):
    response = client.post('/api/login', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["message"] == "Invalid email"
