from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

FILE = "tasks.json"

@app.route("/tasks", methods=["GET"])
def get_tasks():
    if not os.path.exists(FILE):
        return jsonify([])
    with open(FILE, "r") as f:
        tasks = json.load(f)
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    new_task = request.json
    tasks = []

    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            tasks = json.load(f)

    tasks.append(new_task)
    with open(FILE, "w") as f:
        json.dump(tasks, f)

    return jsonify({"message": "Task added"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if not os.path.exists(FILE):
        return jsonify({"message": "No tasks file found"}), 404

    with open(FILE, "r") as f:
        tasks = json.load(f)

    tasks = [t for t in tasks if t["id"] != task_id]

    with open(FILE, "w") as f:
        json.dump(tasks, f)

    return jsonify({"message": "Task deleted"})

# ----------- REQUIRED FOR RENDER -------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
