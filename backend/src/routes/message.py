from flask import Blueprint, request, jsonify
from src.services.message_service import save_message, get_message, delete_message

message_bp = Blueprint("message", __name__)


@message_bp.route("/message", methods=["POST"])
def create_message():
    data = request.json
    message_id = save_message(data)
    return jsonify({"message_id": message_id}), 201


@message_bp.route("/message/<message_id>", methods=["GET"])
def fetch_message(message_id):
    message = get_message(message_id)
    if not message:
        return jsonify({"error": "Message not found"}), 404
    return jsonify(message)


@message_bp.route("/message/<message_id>", methods=["DELETE"])
def remove_message(message_id):
    deleted = delete_message(message_id)
    if deleted:
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Message not found"}), 404
