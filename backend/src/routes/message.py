from flask import Blueprint, request, jsonify
from src.services.message_service import (
    save_message,
    get_message,
    consume_message,
)

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/messages", methods=["POST"])
def create_message():
    """Create a new message."""
    data = request.json
    msg_id = save_message(data)
    return jsonify({"msg_id": msg_id}), 201


@messages_bp.route("/messages/<id>", methods=["GET"])
def fetch_message(id):
    """Fetch a message by its ID."""
    message = get_message(id)
    return jsonify(message)


# Route to DELETE message after it has been read
@messages_bp.route("/messages/<id>", methods=["DELETE"])
def delete_message(id):
    """Delete a message by its ID after it has been read."""
    consume_message(id)
    return jsonify({"status": "deleted"}, 200)
