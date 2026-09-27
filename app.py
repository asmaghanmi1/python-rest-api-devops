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
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# Health check
# =========================

@app.route("/health")
def health():
    return jsonify({
        "status": "UP"
    })


# =========================
# MongoDB connection test
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

    except Exception as e:
        return jsonify({
            "status": "DOWN",
            "message": str(e)
        }), 500


# =========================
# CREATE
# POST /tasks
# =========================

@app.route("/tasks", methods=["POST"])
def create_task():

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({
            "error": "title is required"
        }), 400

    task = {
        "title": data["title"],
        "description": data.get("description", ""),
        "status": data.get("status", "todo")
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
# GET /tasks/<id>
# =========================

@app.route("/tasks/<task_id>", methods=["GET"])
def get_task(task_id):

    try:
        task = tasks_collection.find_one({
            "_id": ObjectId(task_id)
        })

    except Exception:
        return jsonify({
            "error": "Invalid task ID"
        }), 400

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    task["_id"] = str(task["_id"])

    return jsonify(task)


# =========================
# UPDATE
# PUT /tasks/<id>
# =========================

@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):

    try:
        data = request.get_json()

        update_data = {
            "title": data.get("title"),
            "description": data.get("description"),
            "status": data.get("status")
        }

        result = tasks_collection.update_one(
            {
                "_id": ObjectId(task_id)
            },
            {
                "$set": update_data
            }
        )

    except Exception:
        return jsonify({
            "error": "Invalid task ID"
        }), 400

    if result.matched_count == 0:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "message": "Task updated successfully"
    })


# =========================
# DELETE
# DELETE /tasks/<id>
# =========================

@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):

    try:
        result = tasks_collection.delete_one({
            "_id": ObjectId(task_id)
        })

    except Exception:
        return jsonify({
            "error": "Invalid task ID"
        }), 400

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