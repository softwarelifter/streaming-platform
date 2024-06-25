import traceback
import requests
from flask import Blueprint, jsonify, request
from flask import current_app as app


stream_service_bp = Blueprint("stream_service", __name__)


@stream_service_bp.route("/stream/<str:video_id>", methods=["GET"])
def stream(video_id):
    try:
        response = requests.get(f"{app.config['VIDEO_SERVICE_URL']}/stream/{video_id}")
        if response.status_code != 200:
            return jsonify({"error": "Error streaming video"}), 500

        return jsonify(response.json())
    except Exception as e:
        print(f"Error streaming video: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500
