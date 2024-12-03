from datetime import timedelta
from flask import Flask, abort, jsonify, request
from flask_cors import CORS
from models import User, db
from blueprints.wallets import wallet_bp
from blueprints.admin import admin_bp
from config import Config
from flask_jwt_extended import JWTManager, create_access_token
from flasgger import Swagger
import traceback

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
jwt = JWTManager(app)
swagger = Swagger(app)
app.register_blueprint(wallet_bp, url_prefix="/api/wallet")
app.register_blueprint(admin_bp, url_prefix="/api/admin")

# cors = CORS(app, origins=["http://localhost:3000","https://frontend-service-54919216065.us-central1.run.app/"])
CORS(app, resources={r"/api/*": {"origins": ["https://frontend-service-54919216065.us-central1.run.app","http://localhost:3000"]}})
@app.route('/api/register', methods=['POST'])
def register():
    """
    User Registration API
    This endpoint registers a new user with a wallet.
    ---
    tags:
      - Registration
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
                type: string
                description: The name of the user.
            email:
                type: string
                description: The email address of the user.
            phone_number:
                type: string
                description: The phone number of the user.
    responses:
      201:
        description: User successfully registered and wallet created.
        schema:
          type: object
          properties:
            wallet_id:
              type: string
              description: Unique wallet identifier
            balance:
              type: number
              format: float
              description: Wallet balance (default 0.0)
            token:
              type: string
              description: JWT token for authentication
      400:
        description: Missing or invalid fields
      409:
        description: User already registered
      500:
        description: Internal server error
    """

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone_number = data.get("phone_number")
    if not name:
        return jsonify({"message":"Invalid name"}), 400
    elif not email:
        return jsonify({"message":"Invalid name"}), 400
    elif not phone_number:
        return jsonify({"message":"Invalid Phone Number"}), 400
    try:
        user = User.query.filter_by(email=email).all()
        if user:
            return jsonify({"message": "User already Registered"}),409
        
        user = User(name=name, email=email, phone_number=phone_number)
        db.session.add(user)
        db.session.commit()
        expires = timedelta(hours=1)
        access_token = create_access_token(identity=email,  expires_delta=expires)
        return jsonify({"wallet_id": user.wallet_id, "balance": user.balance, "token": access_token}), 201
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        db.session.rollback()
        return jsonify({ "message":"Internal server error. Please try again later."}),500

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    try:
      if not email:
          return jsonify({"message":"Invalid email"}), 400
      user = User.query.filter_by(email=email).first()
      if not user:
          return jsonify({"message":"Email not registered"}), 400
      wallet_id = user.wallet_id
      expires = timedelta(hours=1)
      access_token = create_access_token(identity=email,  expires_delta=expires)
      admin =  False
      if email == 'admin@gmail.com':  # Replace with your logic
        admin= True
      

      return jsonify({"token":access_token, "admin":admin,"wallet_id":wallet_id}),200
    except Exception:
        err_msg = traceback.format_exc()
        print(err_msg)
        return jsonify({"message": "Internal server error. Please try again later"}),500


    
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

