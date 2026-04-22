# HNG14 Stage 2 DevOps — Containerized Microservices

A job processing system made up of three services: a Node.js frontend, a Python/FastAPI backend, and a Python worker — all containerized with Docker and wired together with Docker Compose.

## Architecture

frontend (Node.js :3000)
└── api (FastAPI :8000)
└── redis (queue)
└── worker (Python)

## Prerequisites

- Docker Desktop (v24+)
- Docker Compose (included with Docker Desktop)
- Git

## Quick Start

### 1. Clone the repository

    git clone https://github.com/codabytez/hng14-stage2-devops.git
    cd hng14-stage2-devops

### 2. Set up environment variables

    cp .env.example .env

Edit `.env` and set a strong `REDIS_PASSWORD`.

### 3. Start the stack

    docker compose up --build

### 4. Verify it's working

Open <http://localhost:3000> in your browser. Click **Submit New Job** — you should see the status change from `queued` to `completed` within a few seconds.

## Endpoints

| Service  | Endpoint        | Description           |
| -------- | --------------- | --------------------- |
| Frontend | GET /           | Job dashboard UI      |
| Frontend | POST /submit    | Submit a new job      |
| Frontend | GET /status/:id | Poll job status       |
| Frontend | GET /health     | Frontend health check |
| API      | POST /jobs      | Create a job          |
| API      | GET /jobs/:id   | Get job status        |
| API      | GET /health     | API health check      |

## Services

- **frontend** — Node.js/Express UI on port 3000. Submits jobs to the API and polls for status.
- **api** — Python/FastAPI on port 8000. Creates jobs, pushes to Redis queue, serves status.
- **worker** — Python process. Consumes jobs from Redis queue and marks them completed.
- **redis** — Queue and job state store. Password-protected, not exposed on host.

## Environment Variables

| Variable       | Description               | Default           |
| -------------- | ------------------------- | ----------------- |
| REDIS_PASSWORD | Redis auth password       | required          |
| REDIS_HOST     | Redis hostname            | redis             |
| REDIS_PORT     | Redis port                | 6379              |
| API_URL        | API base URL for frontend | <http://api:8000> |
| APP_ENV        | Environment name          | production        |

## CI/CD Pipeline

GitHub Actions pipeline runs on every push with these stages in order:

1. **Lint** — flake8 (Python), eslint (JavaScript), hadolint (Dockerfiles)
2. **Test** — pytest with coverage report uploaded as artifact
3. **Build** — builds all 3 images, tags with git SHA and latest, pushes to local registry
4. **Security** — Trivy scan on all images, fails on CRITICAL findings, uploads SARIF artifact
5. **Integration** — brings full stack up, submits a job, polls until completed, tears down
6. **Deploy** — rolling update via SSH (main branch only)

## Running Tests Locally

    python3 -m venv venv
    source venv/bin/activate
    pip install -r api/requirements.txt
    pytest api/test_main.py -v --cov=api

## Stopping the Stack

    docker compose down

To also remove volumes (clears Redis data):

    docker compose down -v
