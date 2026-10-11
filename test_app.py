
from unittest.mock import MagicMock, patch

from bson import ObjectId

from app import app


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "UP"}


@patch("app.tasks_collection")
def test_create_task(mock_collection):
    mock_collection.insert_one.return_value = MagicMock(
        inserted_id="test-task-id"
    )

    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "title": "Learn Docker",
            "description": "My first DevOps project",
            "status": "todo",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["message"] == "Task created successfully"
    mock_collection.insert_one.assert_called_once()


@patch("app.tasks_collection")
def test_create_task_without_title(mock_collection):
    client = app.test_client()

    response = client.post(
        "/tasks",
        json={"description": "Task without a title"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "title is required"}
    mock_collection.insert_one.assert_not_called()


@patch("app.tasks_collection")
def test_create_task_with_blank_title(mock_collection):
    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "title": "   ",
            "description": "Test with a blank title",
            "status": "todo",
        },
    )

    assert response.status_code == 400
    mock_collection.insert_one.assert_not_called()


@patch("app.tasks_collection")
def test_create_task_with_invalid_status(mock_collection):
    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "title": "Learn Docker",
            "description": "Test invalid status",
            "status": "finished123",
        },
    )

    assert response.status_code == 400
    mock_collection.insert_one.assert_not_called()


@patch("app.tasks_collection")
def test_create_task_default_status(mock_collection):
    mock_collection.insert_one.return_value = MagicMock(
        inserted_id="test-task-id"
    )

    client = app.test_client()

    response = client.post(
        "/tasks",
        json={
            "title": "Learn Python testing",
            "description": "Test the default status",
        },
    )

    assert response.status_code == 201

    inserted_task = mock_collection.insert_one.call_args.args[0]
    assert inserted_task["status"] == "todo"


@patch("app.tasks_collection")
def test_get_tasks(mock_collection):
    mock_collection.find.return_value = [
        {
            "_id": ObjectId("507f1f77bcf86cd799439011"),
            "title": "Learn Docker",
            "description": "My first DevOps project",
            "status": "todo",
        }
    ]

    client = app.test_client()
    response = client.get("/tasks")

    assert response.status_code == 200

    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Learn Docker"
    assert tasks[0]["_id"] == "507f1f77bcf86cd799439011"


@patch("app.tasks_collection")
def test_get_task(mock_collection):
    task_id = "507f1f77bcf86cd799439011"

    mock_collection.find_one.return_value = {
        "_id": ObjectId(task_id),
        "title": "Learn Docker",
        "description": "My first DevOps project",
        "status": "todo",
    }

    client = app.test_client()
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    task = response.get_json()
    assert task["title"] == "Learn Docker"
    assert task["status"] == "todo"
    assert task["_id"] == task_id


@patch("app.tasks_collection")
def test_get_task_invalid_id(mock_collection):
    client = app.test_client()
    response = client.get("/tasks/invalid-id")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid task ID"}
    mock_collection.find_one.assert_not_called()


@patch("app.tasks_collection")
def test_get_task_not_found(mock_collection):
    mock_collection.find_one.return_value = None

    task_id = "507f1f77bcf86cd799439011"
    client = app.test_client()
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}


@patch("app.tasks_collection")
def test_update_task(mock_collection):
    mock_collection.update_one.return_value.matched_count = 1

    task_id = "507f1f77bcf86cd799439011"
    client = app.test_client()

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Learn Docker and CI/CD",
            "description": "Practice automated testing",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Task updated successfully"
    }
    mock_collection.update_one.assert_called_once()


@patch("app.tasks_collection")
def test_update_task_partial_preserves_other_fields(mock_collection):
    mock_collection.update_one.return_value.matched_count = 1

    task_id = "507f1f77bcf86cd799439011"
    client = app.test_client()

    response = client.put(
        f"/tasks/{task_id}",
        json={"status": "done"},
    )

    assert response.status_code == 200
    mock_collection.update_one.assert_called_once_with(
        {"_id": ObjectId(task_id)},
        {"$set": {"status": "done"}},
    )


@patch("app.tasks_collection")
def test_update_task_not_found(mock_collection):
    mock_collection.update_one.return_value.matched_count = 0

    task_id = "507f1f77bcf86cd799439011"
    client = app.test_client()

    response = client.put(
        f"/tasks/{task_id}",
        json={
            "title": "Learn Docker",
            "description": "Practice testing",
            "status": "in_progress",
        },
    )

    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}


@patch("app.tasks_collection")
def test_update_task_invalid_id(mock_collection):
    client = app.test_client()

    response = client.put(
        "/tasks/invalid-id",
        json={
            "title": "Learn Docker",
            "description": "Practice testing",
            "status": "in_progress",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid task ID"}
    mock_collection.update_one.assert_not_called()


@patch("app.tasks_collection")
def test_delete_task(mock_collection):
    mock_collection.delete_one.return_value.deleted_count = 1

    task_id = "507f1f77bcf86cd799439011"
    client = app.test_client()
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Task deleted successfully"
    }
    mock_collection.delete_one.assert_called_once()


@patch("app.tasks_collection")
def test_delete_task_not_found(mock_collection):
    mock_collection.delete_one.return_value.deleted_count = 0

    task_id = "507f1f77bcf86cd799439011"
    client = app.test_client()
    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}


@patch("app.tasks_collection")
def test_delete_task_invalid_id(mock_collection):
    client = app.test_client()
    response = client.delete("/tasks/invalid-id")

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid task ID"}
    mock_collection.delete_one.assert_not_called()