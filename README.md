 <div align="center">

# Python REST API & DevOps

### Building · Containerizing · Automating

A containerized REST API built with Python and Flask, backed by MongoDB, with automated testing and continuous integration using GitHub Actions.

<br/>

<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-REST_API-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/MongoDB-Database-47A248?style=flat-square&logo=mongodb&logoColor=white" alt="MongoDB"/>
<img src="https://img.shields.io/badge/Docker-Containerization-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/Docker_Compose-Orchestration-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker Compose"/>
<img src="https://img.shields.io/badge/GitHub_Actions-CI-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions"/>
<img src="https://img.shields.io/badge/Tests-pytest-0A9EDC?style=flat-square&logo=pytest&logoColor=white" alt="pytest"/>

<br/><br/>

[Repository](https://github.com/asmaghanmi1/python-rest-api-devops)
  ·  
[API Source Code](https://github.com/asmaghanmi1/python-rest-api-devops/blob/main/app.py)
  ·  
[CI Workflow](https://github.com/asmaghanmi1/python-rest-api-devops/blob/main/.github/workflows/ci.yml)

</div>

---

## Overview

This project demonstrates the development and containerization of a REST API using Python, Flask, and MongoDB.

The application provides task management endpoints, health checks, database connectivity checks, and automated tests. Docker packages the application, while Docker Compose orchestrates the API and database services in a reproducible local environment.

GitHub Actions automates key validation steps, including Python syntax checks, automated tests, database connectivity verification, and Docker image building.

The project focuses on practical backend development, containerization, testing, and continuous integration fundamentals.

## Architecture

```text
                  Client
                    |
                    v
          +--------------------+
          |    Flask REST API  |
          |      Port 5000     |
          +--------------------+
                    |
                    v
          +--------------------+
          |      MongoDB       |
          |     Port 27017     |
          +--------------------+
                    |
                    v
           Persistent Volume

       Docker Compose manages
          both services

      GitHub Actions validates
       code, tests and image
```

## Core Features

* **REST API:** Create, retrieve, update, and delete tasks.
* **Health check:** Verify application availability.
* **Database connectivity:** Check the connection to MongoDB.
* **Input validation:** Handle invalid identifiers and request data.
* **Error handling:** Return appropriate responses for invalid IDs and missing resources.
* **Partial updates:** Update selected task fields without overwriting other fields.
* **Containerization:** Package the Flask application using Docker.
* **Service orchestration:** Run the API and database with Docker Compose.
* **Persistent storage:** Store MongoDB data in a named Docker volume.
* **Automated testing:** Validate application behavior with pytest.
* **Continuous integration:** Run automated checks through GitHub Actions.

## Technology Stack

| Component             | Technology     |
| --------------------- | -------------- |
| Programming language  | Python 3.12    |
| API framework         | Flask          |
| Database              | MongoDB        |
| Database driver       | PyMongo        |
| Containerization      | Docker         |
| Service orchestration | Docker Compose |
| Application server    | Gunicorn       |
| Automated testing     | pytest         |
| CI automation         | GitHub Actions |
| Version control       | Git and GitHub |

## Getting Started

### Prerequisites

Install the following tools:

* [Git](https://git-scm.com/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Docker Compose is included with current Docker Desktop installations.

### 1. Clone the repository

```bash
git clone https://github.com/asmaghanmi1/python-rest-api-devops.git
cd python-rest-api-devops
```

### 2. Start the application

Build the API image and start the application and database:

```bash
docker compose up --build -d
```

Check the running containers:

```bash
docker compose ps
```

View the application logs:

```bash
docker compose logs -f api
```

The API is available at:

```text
http://localhost:5000
```

Press `Ctrl+C` to stop following the logs. This does not stop the containers.

### 3. Test the application

Check the API health:

```bash
curl http://localhost:5000/health
```

Check MongoDB connectivity:

```bash
curl http://localhost:5000/db-test
```

### 4. Stop the application

```bash
docker compose down
```

To remove the database volume as well:

```bash
docker compose down -v
```

**Warning:** The `-v` option deletes the MongoDB data stored in the Compose volume.

## API Reference

Base URL: `http://localhost:5000`

| Method | Endpoint      | Description                |
| ------ | ------------- | -------------------------- |
| GET    | `/`           | Display the home page      |
| GET    | `/health`     | Check application status   |
| GET    | `/db-test`    | Check MongoDB connectivity |
| POST   | `/tasks`      | Create a task              |
| GET    | `/tasks`      | Retrieve all tasks         |
| GET    | `/tasks/<id>` | Retrieve a specific task   |
| PUT    | `/tasks/<id>` | Update a task              |
| DELETE | `/tasks/<id>` | Delete a task              |

### Health Check

Request:

```bash
curl http://localhost:5000/health
```

Example successful response:

```json
{
  "status": "UP"
}
```

### Database Connectivity

Request:

```bash
curl http://localhost:5000/db-test
```

The endpoint checks whether the application can communicate with MongoDB. The exact response depends on the implementation in `app.py`.

### Create a Task

Request:

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Docker",
    "description": "Practice containerization",
    "status": "todo"
  }'
```

The API returns a response indicating the result and, on successful creation, the task identifier.

### Retrieve All Tasks

```bash
curl http://localhost:5000/tasks
```

### Retrieve One Task

Replace `<task_id>` with an identifier returned by the API:

```bash
curl http://localhost:5000/tasks/<task_id>
```

### Update a Task

Update a task's fields:

```bash
curl -X PUT http://localhost:5000/tasks/<task_id> \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Docker Compose",
    "description": "Run a multi-container application",
    "status": "done"
  }'
```

The API also supports partial updates. For example, updating only the status should preserve the other task fields:

```bash
curl -X PUT http://localhost:5000/tasks/<task_id> \
  -H "Content-Type: application/json" \
  -d '{
    "status": "done"
  }'
```

### Delete a Task

```bash
curl -X DELETE http://localhost:5000/tasks/<task_id>
```

**Note:** Replace `<task_id>` with a valid task identifier. The available status values and exact response formats are determined by the application implementation.

## Automated Tests

The project includes automated tests written with pytest.

Run the test suite locally:

```bash
python -m pytest -v
```

The current test suite contains **17 tests**, which have passed locally.

The tests cover API behavior, including task operations, invalid identifiers, missing tasks, and partial-update behavior.

## Continuous Integration

The GitHub Actions workflow is located at:

`.github/workflows/ci.yml`

The workflow performs the following checks:

1. Sets up the Python environment.
2. Installs the project dependencies.
3. Checks Python syntax.
4. Runs the automated pytest suite.
5. Verifies MongoDB connectivity in the CI environment.
6. Builds the Docker image.

The workflow has completed successfully for the latest pushed commit.

[View GitHub Actions runs](https://github.com/asmaghanmi1/python-rest-api-devops/actions)

## Project Structure

```text
python-rest-api-devops/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI workflow
├── templates/
│   └── index.html           # Home page template
├── .dockerignore
├── .gitignore
├── app.py                   # Flask application and API routes
├── test_app.py              # Automated tests
├── Dockerfile               # Docker image definition
├── docker-compose.yml       # API and MongoDB services
└── requirements.txt         # Python dependencies
```

## Project Status

* [x] Implement REST API endpoints for task management.
* [x] Integrate MongoDB.
* [x] Add health and database connectivity checks.
* [x] Containerize the application with Docker.
* [x] Orchestrate the API and database using Docker Compose.
* [x] Configure persistent database storage.
* [x] Add automated tests with pytest.
* [x] Test partial task updates.
* [x] Configure GitHub Actions continuous integration.
* [x] Verify a successful CI run on GitHub.

## Future Improvements

The following items are possible future extensions and are not currently claimed as implemented:

* [ ] Add OpenAPI documentation.
* [ ] Improve application configuration and secrets management.
* [ ] Strengthen container security.
* [ ] Publish the Docker image to a container registry.
* [ ] Explore deployment to AWS.
* [ ] Explore infrastructure provisioning with Terraform.
* [ ] Add monitoring and logging capabilities.

## Author

**Asma Ghanmi**

Computer Engineering Student | Cloud & DevOps | Software Development

* GitHub: [@asmaghanmi1](https://github.com/asmaghanmi1)
* LinkedIn: [Asma Ghanmi](https://www.linkedin.com/in/asma-ghanmi-353992269/)

---

<div align="center">
  <sub>Built to learn, experiment, and improve through practical engineering.</sub>
</div>
