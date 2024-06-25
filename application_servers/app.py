import os
from flask import Flask, request, jsonify, Blueprint
from application_servers.channel.channel_service import channel_service_bp
from application_servers.like_dislike.like_dislike_service import (
    like_dislike_service_bp,
)
from application_servers.user.user_service import user_service_bp
from application_servers.video.video_service import video_service_bp
from application_servers.comments.comments_service import comments_service_bp


app = Flask(__name__)
app.config["DB_NAME"] = os.getenv("DB_NAME", "youtube")
app.config["DB_USER"] = os.getenv("DB_USER", "postgres")
app.config["DB_PASSWORD"] = os.getenv("DB_PASSWORD", "postgres")
app.config["DB_HOST"] = os.getenv("DB_HOST", "localhost")
app.config["DB_PORT"] = os.getenv("DB_PORT", "5432")
app.config["VIDEO_SERVICE_URL"] = os.getenv(
    "VIDEO_SERVICE_URL", "http://localhost:5000"
)
app.secret_key = os.getenv("SECRET_KEY", "secret")

blueprints = [
    channel_service_bp,
    like_dislike_service_bp,
    user_service_bp,
    video_service_bp,
    comments_service_bp,
]

for bp in blueprints:
    app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=os.getenv("PORT", 5000))
