import traceback
from flask import request, jsonify, Blueprint, current_app as app

from application_servers.db.base import DatabaseAccessor
from application_servers.video.video_model import Video
from application_servers.user.user_service import auth_required

video_service_bp = Blueprint("video_service", __name__)


@video_service_bp.route("/video", methods=["POST"])
@auth_required
def create_video():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "name" not in data or "description" not in data:
            return jsonify({"error": "Missing name or description"}), 400

        video = Video(data)
        video_accessor = DatabaseAccessor(Video)
        video_accessor.add(video)

        return jsonify({"message": "Video created successfully"}), 201
    except Exception as e:
        print(f"Error creating video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@video_service_bp.route("/video/<str:video_id>", methods=["GET"])
@auth_required
def get_video(video_id):
    try:
        video_accessor = DatabaseAccessor(Video)
        video = video_accessor.get(id=video_id)
        if video is None:
            return jsonify({"error": "Video not found"}), 404

        return jsonify(video.to_dict())
    except Exception as e:
        print(f"Error getting video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@video_service_bp.route("/video/<str:video_id>", methods=["PUT"])
@auth_required
def update_video(video_id):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        video_accessor = DatabaseAccessor(Video)
        video = video_accessor.get(id=video_id)
        if video is None:
            return jsonify({"error": "Video not found"}), 404

        video.update(data)
        video_accessor.update(video)

        return jsonify({"message": "Video updated successfully"})
    except Exception as e:
        print(f"Error updating video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@video_service_bp.route("/video/<str:video_id>", methods=["DELETE"])
@auth_required
def delete_video(video_id):
    try:
        video_accessor = DatabaseAccessor(Video)
        video = video_accessor.get(id=video_id)
        if video is None:
            return jsonify({"error": "Video not found"}), 404

        video_accessor.delete(video)

        return jsonify({"message": "Video deleted successfully"})
    except Exception as e:
        print(f"Error deleting video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@video_service_bp.route("/video/<str:video_id>/view", methods=["POST"])
def view_video(video_id):
    try:
        video_accessor = DatabaseAccessor(Video)
        video = video_accessor.get(id=video_id)
        if video is None:
            return jsonify({"error": "Video not found"}), 404

        video.views += 1
        video_accessor.update(video)

        return jsonify({"message": "Video viewed successfully"})
    except Exception as e:
        print(f"Error viewing video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
