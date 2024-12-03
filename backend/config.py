import os
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "postgresql://postgres:admin@localhost/wallet_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY") or "secret_key"
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt_secret"
    SWAGGER = {
        "title": "My API",
        "version": "1.0.0",
        "description": "My API description",
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header"
            }
        },
        "security": [{"Bearer": []}]
    }
