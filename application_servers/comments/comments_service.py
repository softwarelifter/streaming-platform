import traceback
from flask import request, jsonify, Blueprint, current_app as app

from application_servers.db.base import DatabaseAccessor
from application_servers.comments.comments_model import Comment
from application_servers.user.user_service import auth_required

comments_service_bp = Blueprint("comments_service", __name__)


@comments_service_bp.route("/comment", methods=["POST"])
@auth_required
def create_comment():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "text" not in data or "video_id" not in data:
            return jsonify({"error": "Missing text or video_id"}), 400

        data["user_id"] = request["user_id"]
        comment = Comment(data)
        comment_accessor = DatabaseAccessor(Comment)
        comment_accessor.add(comment)

        return jsonify({"message": "Comment created successfully"}), 201
    except Exception as e:
        print(f"Error creating comment: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@comments_service_bp.route("/comment/<str:comment_id>", methods=["GET"])
@auth_required
def get_comment(comment_id):
    try:
        comment_accessor = DatabaseAccessor(Comment)
        comment = comment_accessor.get(id=comment_id)
        if comment is None:
            return jsonify({"error": "Comment not found"}), 404

        return jsonify(comment.to_dict())
    except Exception as e:
        print(f"Error getting comment: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@comments_service_bp.route("/comment/<str:comment_id>", methods=["PUT"])
@auth_required
def update_comment(comment_id):
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        comment_accessor = DatabaseAccessor(Comment)
        comment = comment_accessor.get(id=comment_id)
        if comment is None:
            return jsonify({"error": "Comment not found"}), 404

        comment.update(data)
        comment_accessor.update(comment)

        return jsonify({"message": "Comment updated successfully"})
    except Exception as e:
        print(f"Error updating comment: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@comments_service_bp.route("/comment/<str:comment_id>", methods=["DELETE"])
@auth_required
def delete_comment(comment_id):
    try:
        comment_accessor = DatabaseAccessor(Comment)
        comment = comment_accessor.get(id=comment_id)
        if comment is None:
            return jsonify({"error": "Comment not found"}), 404

        comment_accessor.delete(comment)
        return jsonify({"message": "Comment deleted successfully"})
    except Exception as e:
        print(f"Error deleting comment: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@comments_service_bp.route("/comment/<str:video_id>", methods=["GET"])
@auth_required
def video_comments(video_id):
    try:
        # Retrieve pagination parameters from the request
        page = request.args.get("page", 1, type=int)
        limit = request.args.get("limit", 10, type=int)

        # Calculate the offset for pagination
        offset = (page - 1) * limit

        comment_accessor = DatabaseAccessor(Comment)
        comments = comment_accessor.get_all_paginated(
            video_id=video_id, offset=offset, limit=limit
        )
        total_comments = comment_accessor.count(video_id=video_id)

        if comments is None:
            return jsonify({"error": "Comments not found"}), 404

        # Convert comments to dictionary format
        comments_list = [comment.to_dict() for comment in comments]

        # Return the comments along with pagination information
        return jsonify(
            {
                "comments": comments_list,
                "page": page,
                "limit": limit,
                "total_comments": total_comments,
                "total_pages": (total_comments + limit - 1) // limit,
            }
        )
    except Exception as e:
        print(f"Error getting comments: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
