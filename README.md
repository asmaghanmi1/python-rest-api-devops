
<div align="center">

# Python REST API & DevOps

### Building · Containerizing · Automating

A containerized REST API built with Python and Flask, backed by MongoDB, with a focus on API design, application deployment, and DevOps fundamentals.

<br/>

<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
<img src="https://img.shields.io/badge/Flask-REST_API-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
<img src="https://img.shields.io/badge/MongoDB-Database-47A248?style=flat-square&logo=mongodb&logoColor=white" alt="MongoDB"/>
<img src="https://img.shields.io/badge/Docker-Containerization-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions"/>

<br/><br/>

[Repository](https://github.com/asmaghanmi1/python-rest-api-devops)
&nbsp; · &nbsp;
[API Source Code](https://github.com/asmaghanmi1/python-rest-api-devops/blob/main/app.py)
&nbsp; · &nbsp;
[Docker Configuration](https://github.com/asmaghanmi1/python-rest-api-devops/blob/main/docker-compose.yml)

</div>

---

## Overview

This project explores the development and containerization of a Python REST API connected to MongoDB.

It provides task management endpoints and basic service health checks, while Docker Compose orchestrates the application and database in a reproducible local environment.

The goal is to practice backend engineering and progressively strengthen the deployment workflow using DevOps tools.

## Architecture

```text
              Client / API Request
                       |
                       v
              +------------------+
              |   Flask REST API |
              |     Port 5000    |
              +------------------+
                       |
                       v
              +------------------+
              |     MongoDB      |
              |     Port 27017   |
              +------------------+
                       |
                       v
              Persistent Docker Volume

       Docker Compose orchestrates services
```

## Core Features

- **REST API:** Create, retrieve, update, and delete tasks.
- **Health monitoring:** Check application availability through a health endpoint.
- **Database connectivity:** Verify the MongoDB connection.
- **Containerization:** Package the application using Docker.
- **Service orchestration:** Run Flask and MongoDB with Docker Compose.
- **Persistent storage:** Retain database files in a named Docker volume.
- **Error handling:** Handle invalid task IDs and missing resources.

## Technology Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 |
| API framework | Flask |
| Database | MongoDB |
| Database driver | PyMongo |
| Containerization | Docker |
| Orchestration | Docker Compose |
| Automation | GitHub Actions workflow |

## Getting Started

### Prerequisites

Install the following tools:

- [Git](https://git-scm.com/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Docker Compose is included with current Docker Desktop installations.

### 1. Clone the repository

```bash
git clone https://github.com/asmaghanmi1/python-rest-api-devops.git
cd python-rest-api-devops
```

### 2. Start the application

```bash
docker compose up --build
```

Docker Compose builds the Flask application and starts the MongoDB service.

The API is available at:

```text
http://localhost:5000
```

### 3. Stop the application

```bash
docker compose down
```

To remove the database volume as well, use:

```bash
docker compose down -v
```

**Warning:** Removing the volume deletes the MongoDB data stored in it.

## API Reference

Base URL: `http://localhost:5000`

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Display the home page |
| GET | `/health` | Check application status |
| GET | `/db-test` | Check MongoDB connectivity |
| POST | `/tasks` | Create a task |
| GET | `/tasks` | Retrieve all tasks |
| GET | `/tasks/<id>` | Retrieve a specific task |
| PUT | `/tasks/<id>` | Update a task |
| DELETE | `/tasks/<id>` | Delete a task |

### Health Check

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{
  "status": "UP"
}
```

### Database Connectivity

```bash
curl http://localhost:5000/db-test
```

### Create a Task

```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Docker",
    "description": "Practice containerization",
    "status": "todo"
  }'
```

The API returns a success message and the identifier of the created task.

### Retrieve All Tasks

```bash
curl http://localhost:5000/tasks
```

### Retrieve One Task

Replace `<task_id>` with an identifier returned by the API.

```bash
curl http://localhost:5000/tasks/<task_id>
```

### Update a Task

```bash
curl -X PUT http://localhost:5000/tasks/<task_id> \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Docker Compose",
    "description": "Run a multi-container application",
    "status": "in_progress"
  }'
```

### Delete a Task

```bash
curl -X DELETE http://localhost:5000/tasks/<task_id>
```

## Project Structure

```text
python-rest-api-devops/
├── .github/
│   └── workflows/       # GitHub Actions workflow
├── templates/
│   └── index.html       # Home page template
├── .dockerignore
├── .gitignore
├── app.py               # Flask application and API routes
├── Dockerfile           # Application image definition
├── docker-compose.yml   # API and MongoDB services
└── requirements.txt     # Python dependencies
```

## DevOps Workflow

The project provides a foundation for practicing container-based application delivery.

- Build a Docker image from the application source.
- Run the API and database as separate services.
- Configure service connections through environment variables.
- Preserve database data using a Docker volume.
- Use the repository's GitHub Actions workflow to explore automated development workflows.

## Engineering Roadmap

The following improvements are planned, not claimed as completed:

- [ ] Add automated API tests with `pytest`.
- [ ] Validate request payloads and improve error responses.
- [ ] Add API documentation with OpenAPI.
- [ ] Strengthen container security and configuration management.
- [ ] Extend the CI pipeline with automated testing and image builds.
- [ ] Explore deployment to AWS.
- [ ] Explore infrastructure provisioning with Terraform.

## Author

**Asma Ghanmi**

Computer Engineering Student | Cloud & DevOps | Software Development

- GitHub: [@asmaghanmi1](https://github.com/asmaghanmi1)
- LinkedIn: [Asma Ghanmi](https://www.linkedin.com/in/asma-ghanmi-353992269/)

---

<div align="center">
  <sub>Built to learn, experiment, and improve through practical engineering.</sub>
</div>
