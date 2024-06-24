from flask import request, jsonify, Blueprint, current_app as app
from functools import wraps
import traceback
import jwt
import datetime
from hashlib import sha256

from application_servers.user.user_model import User, Address
from application_servers.db.base import DatabaseAccessor


user_service_bp = Blueprint("user_service", __name__)


def generate_token(user_id):
    try:
        token = jwt.encode(
            {
                "user_id": user_id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            },
            app.secret_key,
            algorithm="HS256",
        )
        return token
    except Exception as e:
        print(f"Error encoding token: {e}")
        traceback.print_exc()
        return None


def decode_token(token):
    try:
        return jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid token"}


blacklisted_tokens = (
    set()
)  # TODO: Implement a way to blacklist tokens, e.g. using cache


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get("Authorization") is None:
            return jsonify({"error": "Authorization header is required"}), 401
        try:
            token = request.headers.get("Authorization").split(" ")[1]
            data = decode_token(token)
            if token in blacklisted_tokens:
                return jsonify({"error": "Invalid token"}), 401
            if data["error"]:
                return jsonify(data), 401
            request["user_id"] = data["user_id"]
        except:
            traceback.print_exc()
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated_function


def hash_password(password):
    return sha256(password.encode()).hexdigest()


@user_service_bp.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "username" not in data or "password" not in data or "name" not in data:
            return jsonify({"error": "Missing username or password"}), 400

        data["password"] = hash_password(data["password"])
        data["address"] = [Address(data.get("address", {}))]
        user = User(data)
        user_accessor = DatabaseAccessor(User)
        user_accessor.add(user)

        return (
            jsonify({"message": "User created successfully"}),
            201,
        )
    except Exception as e:
        print(f"Error creating user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@user_service_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Missing JSON data"}), 400

        if "username" not in data or "password" not in data:
            return jsonify({"error": "Missing username or password"}), 400

        user_accessor = DatabaseAccessor(User)
        user = user_accessor.get(username=data["username"])
        if user is None:
            return jsonify({"error": "Invalid username"}), 400

        if user.password != hash_password(data["password"]):
            return jsonify({"error": "Invalid password"}), 400

        token = generate_token(user.id)
        return jsonify({"token": token})
    except Exception as e:
        print(f"Error logging in user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@user_service_bp.route("/logout", methods=["POST"])
@auth_required
def logout():
    try:
        token = request.headers.get("Authorization").split(" ")[1]
        blacklisted_tokens.add(token)
        return jsonify({"message": "Logged out successfully"})
    except Exception as e:
        print(f"Error logging out user: {e}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500


@user_service_bp.route("/is_logged_in", methods=["GET"])
@auth_required
def is_logged_in():
    return jsonify({"message": "User is logged in"})
