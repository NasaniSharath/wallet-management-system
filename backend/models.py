from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    wallet_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid.uuid4()))
    balance = db.Column(db.Float, default=0.0)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.String(36), db.ForeignKey('users.wallet_id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
