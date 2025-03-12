from flask import Blueprint, request, jsonify
from src.services.message_service import save_message, get_message, delete_message

message_bp = Blueprint("message", __name__)


@message_bp.route("/message", methods=["POST"])
def create_message():
    data = request.json
    msg_id = save_message(data)
    if msg_id:
        return jsonify({"msg_id": msg_id}), 201
    return jsonify({"error": "Saving the message failed"}), 400


@message_bp.route("/message/<id>", methods=["GET"])
def fetch_message(id):
    message = get_message(id)
    if message:
        return jsonify(message)
    return jsonify({"error": "Message not found"}), 404


@message_bp.route("/message/<id>", methods=["DELETE"])
def remove_message(id):
    deleted = delete_message(id)
    if deleted:
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Message not found"}), 404
