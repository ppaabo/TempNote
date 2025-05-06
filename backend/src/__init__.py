from flask import Flask
from src.routes.message import messages_bp
from src.exceptions import MessageNotFound, DatabaseError, InvalidPayload
from src.utils.response import create_response
from src.db import initialize_db, close_db
import logging
import os
import sys


def configure_logging():
    env = os.getenv("APP_ENV", "production")
    log_level = logging.INFO
    log_format = "%(asctime)s %(levelname)s in %(module)s:%(lineno)d %(message)s"
    date_format = "%d-%m-%Y %H:%M:%S"

    logging.basicConfig(
        stream=sys.stdout,
        level=log_level,
        format=log_format,
        datefmt=date_format,
    )

    return env


def create_app():
    env = configure_logging()
    app = Flask(__name__)
    app.logger.handlers = logging.getLogger().handlers
    app.logger.setLevel(logging.getLogger().level)
    app.logger.propagate = False
    app.logger.info(f"Application starting in {env} environment")
    app.register_blueprint(messages_bp, url_prefix="/api")

    initialize_db()

    @app.teardown_appcontext
    def teardown_db(exception):
        close_db()

    @app.errorhandler(MessageNotFound)
    def handle_msg_not_found(e):
        app.logger.info(f"MessageNotFound: {e}")
        return create_response(
            is_success=False, message="Message not found", http_status=404
        )

    @app.errorhandler(DatabaseError)
    def handle_db_error(e):
        app.logger.error(f"DatabaseError: {e}")
        return create_response(
            is_success=False, message="Database error", http_status=500
        )

    @app.errorhandler(InvalidPayload)
    def handle_payload_error(e):
        app.logger.info(f"Invalid request payload: {e}")
        return create_response(
            is_success=False, message="Invalid request data", http_status=400
        )

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        app.logger.exception(f"Unhandled Exception: {e}")
        return create_response(
            is_success=False, message="Internal server error", http_status=500
        )

    return app
