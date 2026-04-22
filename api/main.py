import os
import uuid
import redis
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True,
)


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/jobs", status_code=201)
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("jobs", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return JSONResponse(status_code=404, content={"error": "not found"})
    return {"job_id": job_id, "status": status}