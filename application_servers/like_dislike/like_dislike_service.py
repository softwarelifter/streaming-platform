import traceback
from flask import Blueprint, jsonify, request

from application_servers.db.base import DatabaseAccessor
from application_servers.like_dislike.like_dislike_model import VideoLikeDislike
from application_servers.like_dislike.like_dislike_model import CommentLikeDislike
from application_servers.user.user_service import auth_required


like_dislike_service_bp = Blueprint("like_dislike_service", __name__)


@like_dislike_service_bp.route("/video/like", methods=["POST"])
@auth_required
def like():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "video_id" not in data:
            return jsonify({"error": "Missing video_id"}), 400

        data["user_id"] = request["user_id"]
        data["like"] = True
        like_dislike = VideoLikeDislike(data)
        like_dislike_accessor = DatabaseAccessor(VideoLikeDislike)
        like_dislike_accessor.add(like_dislike)

        return jsonify({"message": "Liked successfully"}), 201
    except Exception as e:
        print(f"Error liking video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@like_dislike_service_bp.route("/video/dislike", methods=["POST"])
@auth_required
def dislike():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "video_id" not in data:
            return jsonify({"error": "Missing video_id"}), 400

        data["user_id"] = request["user_id"]
        data["dislike"] = True
        like_dislike = VideoLikeDislike(data)
        like_dislike_accessor = DatabaseAccessor(VideoLikeDislike)
        like_dislike_accessor.add(like_dislike)

        return jsonify({"message": "Disliked successfully"}), 201
    except Exception as e:
        print(f"Error disliking video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@like_dislike_service_bp.route("/video/like", methods=["PUT"])
@auth_required
def update_like():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        like_dislike_accessor = DatabaseAccessor(VideoLikeDislike)
        like_dislike = like_dislike_accessor.get(
            user_id=request["user_id"], video_id=data["video_id"]
        )
        if like_dislike is None:
            return jsonify({"error": "Like not found"}), 404

        like_dislike_accessor.update(data)
        return jsonify({"message": "Like updated successfully"})
    except Exception as e:
        print(f"Error updating like: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@like_dislike_service_bp.route("/video/dislike", methods=["PUT"])
@auth_required
def update_dislike():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        like_dislike_accessor = DatabaseAccessor(VideoLikeDislike)
        like_dislike = like_dislike_accessor.get(
            user_id=request["user_id"], video_id=data["video_id"]
        )
        if like_dislike is None:
            return jsonify({"error": "Dislike not found"}), 404

        like_dislike_accessor.update(data)
        return jsonify({"message": "Dislike updated successfully"})
    except Exception as e:
        print(f"Error updating dislike: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@like_dislike_service_bp.route("/comment/like", methods=["POST"])
@auth_required
def like_comment():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "comment_id" not in data:
            return jsonify({"error": "Missing comment_id"}), 400

        data["user_id"] = request["user_id"]
        data["like"] = True
        like_dislike = CommentLikeDislike(data)
        like_dislike_accessor = DatabaseAccessor(CommentLikeDislike)
        like_dislike_accessor.add(like_dislike)

        return jsonify({"message": "Liked successfully"}), 201
    except Exception as e:
        print(f"Error liking comment: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@like_dislike_service_bp.route("/comment/dislike", methods=["POST"])
@auth_required
def dislike_comment():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "comment_id" not in data:
            return jsonify({"error": "Missing comment_id"}), 400

        data["user_id"] = request["user_id"]
        data["dislike"] = True
        like_dislike = CommentLikeDislike(data)
        like_dislike_accessor = DatabaseAccessor(CommentLikeDislike)
        like_dislike_accessor.add(like_dislike)

        return jsonify({"message": "Disliked successfully"}), 201
    except Exception as e:
        print(f"Error disliking comment: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@like_dislike_service_bp.route("/comment/like", methods=["PUT"])
@auth_required
def update_like_comment():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        like_dislike_accessor = DatabaseAccessor(CommentLikeDislike)
        like_dislike = like_dislike_accessor.get(
            user_id=request["user_id"], comment_id=data["comment_id"]
        )
        if like_dislike is None:
            return jsonify({"error": "Like not found"}), 404

        like_dislike_accessor.update(data)
        return jsonify({"message": "Like updated successfully"})
    except Exception as e:
        print(f"Error updating like: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@like_dislike_service_bp.route("/comment/dislike", methods=["PUT"])
@auth_required
def update_dislike_comment():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        like_dislike_accessor = DatabaseAccessor(CommentLikeDislike)
        like_dislike = like_dislike_accessor.get(
            user_id=request["user_id"], comment_id=data["comment_id"]
        )
        if like_dislike is None:
            return jsonify({"error": "Dislike not found"}), 404

        like_dislike_accessor.update(data)
        return jsonify({"message": "Dislike updated successfully"})
    except Exception as e:
        print(f"Error updating dislike: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
