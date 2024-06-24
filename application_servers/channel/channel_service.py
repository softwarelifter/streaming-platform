from flask import request, jsonify, Blueprint, current_app as app
import traceback

from application_servers.db.base import DatabaseAccessor
from application_servers.user.user_service import auth_required
from application_servers.channel.channel_model import Channel

channel_service_bp = Blueprint("channel_service", __name__)


@channel_service_bp.route("/channel", methods=["POST"])
@auth_required
def create_channel():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "name" not in data or "description" not in data:
            return jsonify({"error": "Missing name or description"}), 400

        data["user_id"] = request["user_id"]
        channel = Channel(data)
        channel_accessor = DatabaseAccessor(Channel)
        channel_accessor.add(channel)

        return jsonify({"message": "Channel created successfully"}), 201
    except Exception as e:
        print(f"Error creating channel: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@channel_service_bp.route("/channel/<str:channel_id>", methods=["GET"])
@auth_required
def get_channel(channel_id):
    try:
        channel_accessor = DatabaseAccessor(Channel)
        channel = channel_accessor.get(id=channel_id)
        if channel is None:
            return jsonify({"error": "Channel not found"}), 404

        return jsonify(channel.to_dict())
    except Exception as e:
        print(f"Error getting channel: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@channel_service_bp.route("/channel/<str:channel_id>", methods=["PUT"])
@auth_required
def update_channel(channel_id):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        channel_accessor = DatabaseAccessor(Channel)
        channel = channel_accessor.get(id=channel_id)
        if channel is None:
            return jsonify({"error": "Channel not found"}), 404

        channel.update(data)
        channel_accessor.update(channel)

        return jsonify({"message": "Channel updated successfully"})
    except Exception as e:
        print(f"Error updating channel: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@channel_service_bp.route("/channel/<str:channel_id>", methods=["DELETE"])
@auth_required
def delete_channel(channel_id):
    try:
        channel_accessor = DatabaseAccessor(Channel)
        channel = channel_accessor.get(id=channel_id)
        if channel is None:
            return jsonify({"error": "Channel not found"}), 404

        channel_accessor.delete(channel)

        return jsonify({"message": "Channel deleted successfully"})
    except Exception as e:
        print(f"Error deleting channel: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
