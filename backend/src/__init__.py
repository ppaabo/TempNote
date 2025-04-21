from flask import Flask
from src.routes.message import messages_bp
from src.exceptions import MessageNotFound, DatabaseError, InvalidPayload
from src.utils.response import create_response
import logging


def create_app():
    app = Flask(__name__)
    app.register_blueprint(messages_bp, url_prefix="/api")

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    @app.errorhandler(MessageNotFound)
    def handle_msg_not_found(e):
        logger.info(f"MessageNotFound: {e}")
        return create_response(is_success=False, message=str(e), http_status=404)

    @app.errorhandler(DatabaseError)
    def handle_db_error(e):
        logger.error(f"DatabaseError: {e}")
        return create_response(
            is_success=False, message="Database error", http_status=500
        )

    @app.errorhandler(InvalidPayload)
    def handle_payload_error(e):
        logger.info(f"Invalid request payload: {e}")
        return create_response(is_success=False, message=str(e), http_status=400)

    @app.errorhandler(Exception)
    def handle_generic_error(e):
        logger.exception(f"Unhandled Exception: {e}")
        return create_response(
            is_success=False, message="Internal server error", http_status=500
        )

    return app
