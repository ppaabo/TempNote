from flask import Blueprint, request
from src.services.message_service import (
    save_message,
    get_message,
    consume_message,
)
from src.utils.response import create_response

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/messages", methods=["POST"])
def create_message():
    """Create a new message."""
    data = request.json
    msg_id = save_message(data)
    return create_response(data={"msg_id": msg_id}, http_status=201)


@messages_bp.route("/messages/<id>", methods=["GET"])
def fetch_message(id):
    """Fetch a message by its ID."""
    message = get_message(id)
    return create_response(data=message, http_status=200)


# Route to DELETE message after it has been read
@messages_bp.route("/messages/<id>", methods=["DELETE"])
def delete_message(id):
    """Delete a message by its ID after it has been read."""
    consume_message(id)
    return create_response(http_status=200)
