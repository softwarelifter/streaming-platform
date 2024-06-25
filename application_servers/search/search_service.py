import traceback
import requests
from flask import Blueprint, jsonify, request
from flask import current_app as app

from application_servers.user.user_service import auth_required


search_service_bp = Blueprint("search_service", __name__)


@search_service_bp.route("/search", methods=["GET"])
def search():
    try:
        query = request.args.get("query")
        if query is None:
            return jsonify({"error": "Missing query parameter"}), 400

        # TODO: Implement search logic based on user identification and preferences

        response = requests.get(f"{app.config['VIDEO_SERVICE_URL']}/search?q={query}")
        if response.status_code != 200:
            return jsonify({"error": "Error searching videos"}), 500

        return jsonify(response.json())
    except Exception as e:
        print(f"Error searching videos: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@search_service_bp.route("/recommendations/<str:video_id>", methods=["GET"])
def recommendations(video_id):
    try:
        # TODO: Implement search logic based on user identification and preferences
        response = requests.get(
            f"{app.config['VIDEO_SERVICE_URL']}/recommendations/{video_id}"
        )
        if response.status_code != 200:
            return jsonify({"error": "Error getting recommendations"}), 500

        return jsonify(response.json())
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
