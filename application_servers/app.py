from flask import Flask, request, jsonify, Blueprint
import os


app = Flask(__name__)
app.config["DB_NAME"] = os.getenv("DB_NAME", "youtube")
app.config["DB_USER"] = os.getenv("DB_USER", "postgres")
app.config["DB_PASSWORD"] = os.getenv("DB_PASSWORD", "postgres")
app.config["DB_HOST"] = os.getenv("DB_HOST", "localhost")
app.config["DB_PORT"] = os.getenv("DB_PORT", "5432")
app.secret_key = os.getenv("SECRET_KEY", "secret")


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=os.environ.get("PORT", 5000))
