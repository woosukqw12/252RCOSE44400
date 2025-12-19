from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

DATA_PATH = "/data/message.txt"

def read_message():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            return f.read().strip()
    else:
        return ""

def write_message(msg: str):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, 'w', encoding='utf-8') as f:
        f.write(msg)

@app.route("/api/message", methods=["GET"])
def get_message():
    msg = read_message()

    return jsonify({"message": msg})

@app.route("/api/message", methods=["POST"])
def update_message():
    data = request.get_json()
    new_msg = data.get("message", "")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_message = f"{new_msg} (updated at {now})"

    write_message(full_message)

    return jsonify({"status": "ok"})



# v1 has no /api/health endpoint
# (Students add this in v2)

# v2 TODO:
# - Modify write_message() or update_message() to include a timestamp
#   Format: "<message> (updated at YYYY-MM-DD HH:MM:SS)"
#
# - Add new endpoint /api/health that returns:
#   { "status": "healthy" }
@app.route("/api/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)