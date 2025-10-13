import os
from flask import Flask
from flask_cors import CORS
from .config import Config
from database import db

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating instance folder: {e}")

    db.init_app(app)
    CORS(app)

    from .routes import register_routes
    register_routes(app)

    with app.app_context():
        from . import models
        
    return app