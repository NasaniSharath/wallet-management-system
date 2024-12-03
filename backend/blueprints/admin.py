import traceback
from flask import Blueprint, jsonify
from models import User, Transaction
from flask_jwt_extended import jwt_required, get_jwt_identity

admin_bp = Blueprint('admin_bp', __name__)
def check_admin():
    current_user = get_jwt_identity()
    if current_user != 'admin@gmail.com': 
        return False
    return True

@admin_bp.route('/wallets', methods=['GET'])
@jwt_required()
def get_all_wallets():
    """
    Get all wallets
    ---
    tags:
      - Admin Operations
    security:
      - Bearer: []
    responses:
      200:
        description: List of all wallets
        schema:
          type: array
          items:
            type: object
            properties:
              wallet_id:
                type: string
                description: Unique wallet identifier
              name:
                type: string
                description: Name of the user
              balance:
                type: number
                format: float
                description: Wallet balance
      403:
        description: Unauthorized access (Admin only)
      500:
        description: Internal server error
    """
    if not check_admin():
        return jsonify({"message": "Unauthorized"}), 403
    try:
        wallets = User.query.all()
        wallet_list = [{"wallet_id": user.wallet_id, "name": user.name, "balance": user.balance} for user in wallets]
        return jsonify(wallet_list), 200
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        return jsonify({ "message":"Internal server error. Please try again later."}),500

@admin_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_all_transactions():
    """
    Get all transactions
    ---
    tags:
      - Admin Operations
    security:
      - Bearer: []
    responses:
      200:
        description: List of all transactions
        schema:
          type: array
          items:
            type: object
            properties:
              wallet_id:
                type: string
                description: Wallet identifier for the transaction
              type:
                type: string
                description: Type of transaction (e.g., Add Money, Transfer)
              amount:
                type: number
                format: float
                description: Amount of the transaction
              timestamp:
                type: string
                format: date-time
                description: Time of the transaction
      403:
        description: Unauthorized access (Admin only)
      500:
        description: Internal server error
    """
    if not check_admin():
        return jsonify({"message": "Unauthorized"}), 403
    try:
        transactions = Transaction.query.order_by(Transaction.timestamp.desc()).all()
        transaction_list = [{"wallet_id": txn.wallet_id, "type": txn.transaction_type, "amount": txn.amount, "timestamp": txn.timestamp,"id":txn.id} for txn in transactions]
        return jsonify(transaction_list), 200
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        return jsonify({ "message":"Internal server error. Please try again later."}),500


@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_analytics():
    """
    Get analytics
    ---
    tags:
      - Admin Operations
    security:
      - Bearer: []
    responses:
      200:
        description: Analytics data
        schema:
          type: object
          properties:
            total_money_added:
              type: number
              format: float
              description: Total money added to wallets
            total_transactions:
              type: integer
              description: Total number of transactions
            top_wallets:
              type: array
              items:
                type: object
                properties:
                  wallet_id:
                    type: string
                    description: Wallet identifier
                  name:
                    type: string
                    description: Name of the wallet owner
                  balance:
                    type: number
                    format: float
                    description: Balance of the wallet
      403:
        description: Unauthorized access (Admin only)
      500:
        description: Internal server error
    """
    if not check_admin():
        return jsonify({"message": "Unauthorized"}), 403
    try:
        total_money = sum([txn.amount for txn in Transaction.query.filter_by(transaction_type="Add Money").all()])
        total_transactions = Transaction.query.count()
        top_wallets = User.query.order_by(User.balance.desc()).limit(5).all()
        top_wallet_list = [{"wallet_id": user.wallet_id, "name": user.name, "balance": user.balance} for user in top_wallets]

        analytics = {
            "total_money_added": total_money,
            "total_transactions": total_transactions,
            "top_wallets": top_wallet_list
        }
        return jsonify(analytics), 200
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        return jsonify({ "message":"Internal server error. Please try again later."}),500
