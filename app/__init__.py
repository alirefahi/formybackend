from flask import Flask
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load environment variables
    mongo_uri = os.getenv('MONGO_URI')
    print(mongo_uri)
    # database_name = os.getenv('DATABASE_NAME')

    client = MongoClient(mongo_uri, server_api=ServerApi('1'), tlsAllowInvalidCertificates=True)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    # app.db = client[database_name]
    app.db = client.get_default_database()

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
