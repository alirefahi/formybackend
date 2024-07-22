from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Configure JWT
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # Change this to a more secure key

    # Load environment variables
    mongo_uri = "mongodb://root:1G5AediIB2u12lvJNUuKEmbk@formydb:27017/my-app?authSource=admin"

    client = MongoClient(mongo_uri)
    app.db = client.get_default_database()

    # Initialize Bcrypt and JWT
    bcrypt.init_app(app)
    jwt.init_app(app)

    from formyapp.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


# Create Bcrypt and JWT instances
bcrypt = Bcrypt()
jwt = JWTManager()
