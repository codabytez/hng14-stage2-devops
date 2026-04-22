from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient

with patch("redis.Redis") as mock_redis:
    mock_redis.return_value = MagicMock()
    from main import app, r

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_mock():
    r.reset_mock()


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_job():
    r.lpush = MagicMock()
    r.hset = MagicMock()
    response = client.post("/jobs")
    assert response.status_code == 201
    assert "job_id" in response.json()
    r.lpush.assert_called_once()
    r.hset.assert_called_once()


def test_get_job_found():
    r.hget = MagicMock(return_value="completed")
    response = client.get("/jobs/test-job-id")
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_get_job_not_found():
    r.hget = MagicMock(return_value=None)
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 404
    assert response.json()["error"] == "not found"


def test_create_job_returns_uuid():
    r.lpush = MagicMock()
    r.hset = MagicMock()
    response = client.post("/jobs")
    job_id = response.json()["job_id"]
    import uuid
    uuid.UUID(job_id)  # raises ValueError if not valid UUID