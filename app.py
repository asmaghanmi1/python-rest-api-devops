
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# =========================
# MongoDB connection
# =========================

mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db]

tasks_collection = db["tasks"]


# =========================
# Home page
# GET /
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# Health check
# GET /health
# =========================

@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })


# =========================
# MongoDB connection test
# GET /db-test
# =========================

@app.route("/db-test")
def db_test():
    try:
        client.admin.command("ping")

        return jsonify({
            "status": "UP",
            "database": db.name,
            "message": "MongoDB connection successful"
        })

    except Exception:
        return jsonify({
            "status": "DOWN",
            "message": "MongoDB connection failed"
        }), 500


# =========================
# CREATE
# POST /tasks
# =========================

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "A valid JSON object is required"
        }), 400

    title = data.get("title")

    if not isinstance(title, str) or not title.strip():
        return jsonify({
            "error": "title is required"
        }), 400

    description = data.get("description", "")

    if not isinstance(description, str):
        return jsonify({
            "error": "description must be a string"
        }), 400

    allowed_statuses = ["todo", "in_progress", "done"]
    status = data.get("status", "todo")

    if not isinstance(status, str) or status not in allowed_statuses:
        return jsonify({
            "error": "Invalid status",
            "allowed_statuses": allowed_statuses
        }), 400

    task = {
        "title": title.strip(),
        "description": description,
        "status": status
    }

    result = tasks_collection.insert_one(task)

    return jsonify({
        "message": "Task created successfully",
        "task_id": str(result.inserted_id)
    }), 201


# =========================
# READ ALL
# GET /tasks
# =========================

@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = list(tasks_collection.find())

    for task in tasks:
        task["_id"] = str(task["_id"])

    return jsonify(tasks)


# =========================
# READ ONE
# GET /tasks/<task_id>
# =========================

@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({
            "error": "Invalid task ID"
        }), 400

    task = tasks_collection.find_one({
        "_id": ObjectId(task_id)
    })

    if task is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    task["_id"] = str(task["_id"])

    return jsonify(task)


# =========================
# UPDATE
# PUT /tasks/<task_id>
# Update only supplied fields
# =========================

@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({
            "error": "Invalid task ID"
        }), 400

    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data:
        return jsonify({
            "error": "A non-empty JSON object is required"
        }), 400

    update_data = {}

    # Update title only if provided
    if "title" in data:
        title = data["title"]

        if not isinstance(title, str) or not title.strip():
            return jsonify({
                "error": "title must be a non-empty string"
            }), 400

        update_data["title"] = title.strip()

    # Update description only if provided
    if "description" in data:
        description = data["description"]

        if not isinstance(description, str):
            return jsonify({
                "error": "description must be a string"
            }), 400

        update_data["description"] = description

    # Update status only if provided
    if "status" in data:
        allowed_statuses = ["todo", "in_progress", "done"]
        status = data["status"]

        if not isinstance(status, str) or status not in allowed_statuses:
            return jsonify({
                "error": "Invalid status",
                "allowed_statuses": allowed_statuses
            }), 400

        update_data["status"] = status

    if not update_data:
        return jsonify({
            "error": "No valid fields to update"
        }), 400

    result = tasks_collection.update_one(
        {"_id": ObjectId(task_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task updated successfully"
    })


# =========================
# DELETE
# DELETE /tasks/<task_id>
# =========================

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    if not ObjectId.is_valid(task_id):
        return jsonify({
            "error": "Invalid task ID"
        }), 400

    result = tasks_collection.delete_one({
        "_id": ObjectId(task_id)
    })

    if result.deleted_count == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task deleted successfully"
    })


# =========================
# Run application
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)