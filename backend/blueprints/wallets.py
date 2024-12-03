from flask import Blueprint, abort, request, jsonify
from models import User, Transaction, db
from flask_jwt_extended import jwt_required
import traceback
wallet_bp = Blueprint('wallet_bp', __name__)


@wallet_bp.route('/add-money', methods=['POST'])
@jwt_required()
def add_money():
    """
    Add Money to Wallet
    ---
    tags:
      - User Wallet Operations
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            wallet_id:
              type: string
              description: The wallet ID to which money will be added
            amount:
              type: number
              description: The amount to be added to the wallet
    responses:
      200:
        description: Money added successfully
        schema:
          properties:
            updated_balance:
              type: number
              description: The updated balance in the wallet
      400:
        description: Missing wallet_id or amount, or invalid data format
      500:
        description: Internal server error
    """

    data = request.get_json()
    if not data or 'wallet_id' not in data or 'amount' not in data:
        return jsonify({"message":"Missing 'wallet_id' or 'amount'"}), 400
    
    try:
        amount = float(data['amount'])
        if amount <= 0:
            return jsonify({"message":"Amount must be greater than zero"}),400
    except (ValueError, TypeError):
        return jsonify({ "message":"Invalid amount format"}),400
    try:
        user = User.query.filter_by(wallet_id=data['wallet_id']).with_for_update().first_or_404(description="Wallet not found")
        amount = float(data['amount'])
        user.balance += amount
        transaction = Transaction(wallet_id=user.wallet_id, transaction_type="Add Money", amount=amount)
        db.session.add(transaction)
        db.session.commit()
        return jsonify({"updated_balance": user.balance}), 200
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        db.session.rollback()
        db.session.close()
        return jsonify({ "message":"Internal server error. Please try again later."}),500
    
@wallet_bp.route("/<wallet_id>/balance", methods=["GET"])
@jwt_required()
def get_balance(wallet_id):
    """
    Get Wallet Balance
    ---
    tags:
      - User Wallet Operations
    security:
      - Bearer: []
    parameters:
      - in: path
        name: wallet_id
        required: true
        type: string
        description: The wallet ID for which balance is requested
    responses:
      200:
        description: The balance of the wallet
        schema:
          properties:
            balance:
              type: number
              description: The balance of the wallet
      404:
        description: Wallet not found
      500:
        description: Internal server error
    """
     
    try:
        user = User.query.filter_by(wallet_id=wallet_id).first_or_404()
        balance = user.balance
        return jsonify({"balance":balance}), 200
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        db.session.rollback()
        db.session.close()
        return jsonify({ "message":"Internal server error. Please try again later."}),500

@wallet_bp.route("/<wallet_id>/transactions", methods=["GET"])
@jwt_required()
def get_transactions(wallet_id):
    """
    Get Transactions for a Wallet
    ---
    tags:
      - User Wallet Operations
    security:
      - Bearer: []  
    parameters:
      - in: path
        name: wallet_id
        required: true
        type: string
        description: The wallet ID for which transactions are requested
    responses:
      200:
        description: List of transactions for the wallet
        schema:
          properties:
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: The transaction ID
                  wallet_id:
                    type: string
                    description: The wallet ID associated with the transaction
                  transaction_type:
                    type: string
                    description: The type of transaction (e.g., "Add Money", "Transfer")
                  amount:
                    type: number
                    description: The amount of the transaction
                  timestamp:
                    type: string
                    description: The timestamp of the transaction
      404:
        description: No transactions found for the wallet ID
      500:
        description: Internal server error
    """

    try:

        transactions = Transaction.query.filter_by(wallet_id=wallet_id).order_by(Transaction.timestamp.desc()).all()
        
        # Check if any transactions exist for the wallet_id
        if not transactions:
            return jsonify({"message":f"No transactions found for wallet ID {wallet_id}"}),404

        transactions_list = [
            {
                'id': tx.id,
                'wallet_id': tx.wallet_id,
                'transaction_type': tx.transaction_type,
                'amount': tx.amount,
                'timestamp': tx.timestamp
            }
            for tx in transactions
        ]
        
        return jsonify({"data":transactions_list}), 200
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        db.session.rollback()
        db.session.close()
        return jsonify({ "message":"Internal server error. Please try again later."}),500

@wallet_bp.route("/transfer", methods=["POST"])
def transfer_money():
    """
    Transfer Money Between Wallets
    ---
    tags:
      - User Wallet Operations
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            from_wallet_id:
              type: string
            to_wallet_id:
              type: string
            amount:
              type: number
    responses:
      200:
        description: Successful transfer
        schema:
          properties:
            from_balance:
              type: number
            to_balance:
              type: number
      400:
        description: Invalid transfer amount
    """
    data = request.get_json()
    from_wallet_id = data['from_wallet_id']
    to_wallet_id = data['to_wallet_id']
    amount = data['amount']

    if amount <= 0:
        return jsonify({"error": "Invalid transfer amount"}), 400

    try:
        with db.session.begin_nested():
            from_wallet = User.query.filter_by(wallet_id=from_wallet_id).with_for_update().first()
            to_wallet = User.query.filter_by(wallet_id=to_wallet_id).with_for_update().first()

            if not from_wallet or not to_wallet:
                return jsonify({"error": "Invalid wallet IDs"}), 400

            if from_wallet.balance < amount:
                return jsonify({"error": "Insufficient balance"}), 400

            # Deduct from sender's wallet
            from_wallet.balance -= amount
            # Add to receiver's wallet
            to_wallet.balance += amount

            # Log transactions
            transaction_from = Transaction(wallet_id=from_wallet_id, transaction_type='Transfer', amount=-amount)
            transaction_to = Transaction(wallet_id=to_wallet_id, transaction_type='Transfer', amount=amount)

            db.session.add(transaction_from)
            db.session.add(transaction_to)

        db.session.commit()
        return jsonify({
            "from_balance": from_wallet.balance,
            "to_balance": to_wallet.balance
        })

    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        db.session.rollback()
        db.session.close()
        return jsonify({ "message":"Internal server error. Please try again later."}),500