from flask import Flask
from src.routes.message import messages_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(messages_bp, url_prefix="/api")
    return app
