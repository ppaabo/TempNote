from flask import Blueprint, request, jsonify
from src.services.message_service import save_message, get_message, delete_message

messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/messages", methods=["POST"])
def create_message():
    data = request.json
    msg_id = save_message(data)
    if msg_id:
        return jsonify({"msg_id": msg_id}), 201
    return jsonify({"error": "Saving the message failed"}), 400


@messages_bp.route("/messages/<id>", methods=["GET"])
def fetch_message(id):
    message = get_message(id)
    if message:
        return jsonify(message)
    return jsonify({"error": "Message not found"}), 404


@messages_bp.route("/messages/<id>", methods=["DELETE"])
def remove_message(id):
    deleted = delete_message(id)
    if deleted:
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Message not found"}), 404
