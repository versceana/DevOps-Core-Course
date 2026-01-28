from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

START_TIME = datetime.utcnow()

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "service": "DevOps Core Course",
        "lab": "Lab01",
        "framework": "Flask",
        "uptime_seconds": int((datetime.utcnow() - START_TIME).total_seconds())
    })

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "time": datetime.utcnow().isoformat()
    })

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
