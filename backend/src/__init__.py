from flask import Flask
from src.routes.message import message_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(message_bp, url_prefix="/api")
    return app
