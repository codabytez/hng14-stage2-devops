# FIXES.md — Bug Report

All bugs found and fixed in the starter repository.

---

## Bug 1 — `api/.env` committed to repository

**File:** `api/.env`
**Problem:** The `.env` file containing secrets (`REDIS_PASSWORD`) was committed to the repository. This is a critical security violation.
**Fix:** Deleted `api/.env`, added `.env` and `*.env` to `.gitignore`, and created `.env.example` with placeholder values.

---

## Bug 2 — `api/main.py` line 6: Redis host hardcoded to localhost

**File:** `api/main.py`, line 6
**Problem:** `redis.Redis(host="localhost", port=6379)` — hardcoded localhost does not work inside Docker containers. Services must communicate via service names on the internal network.
**Fix:** Changed to use environment variables: `host=os.getenv("REDIS_HOST", "redis")`, `port=int(os.getenv("REDIS_PORT", 6379))`.

---

## Bug 3 — `api/main.py` line 6: Redis password ignored

**File:** `api/main.py`, line 6
**Problem:** The Redis connection did not include the password even though `REDIS_PASSWORD` was defined in `.env`. This would cause authentication failures against a password-protected Redis instance.
**Fix:** Added `password=os.getenv("REDIS_PASSWORD")` to the Redis connection.

---

## Bug 4 — `api/main.py` line 14: Wrong queue name

**File:** `api/main.py`, line 14
**Problem:** `r.lpush("job", job_id)` — the API pushed to a queue named `"job"` but the worker consumed from `"jobs"` (or vice versa), causing jobs to never be picked up.
**Fix:** Standardized queue name to `"jobs"` in both API and worker.

---

## Bug 5 — `api/main.py`: Missing 404 status code

**File:** `api/main.py`, GET `/jobs/{job_id}` handler
**Problem:** When a job was not found, the endpoint returned `{"error": "not found"}` with HTTP status 200 instead of 404.
**Fix:** Used `JSONResponse(status_code=404, content={"error": "not found"})`.

---

## Bug 6 — `api/main.py`: Missing `/health` endpoint

**File:** `api/main.py`
**Problem:** No health check endpoint existed, making it impossible for Docker and load balancers to verify the service is alive.
**Fix:** Added `GET /health` returning `{"status": "healthy"}`.

---

## Bug 7 — `worker/worker.py` line 6: Redis host hardcoded to localhost

**File:** `worker/worker.py`, line 6
**Problem:** Same as Bug 2 — `redis.Redis(host="localhost")` does not work in Docker.
**Fix:** Changed to use environment variables: `host=os.getenv("REDIS_HOST", "redis")`.

---

## Bug 8 — `worker/worker.py` line 6: Redis password ignored

**File:** `worker/worker.py`, line 6
**Problem:** Same as Bug 3 — password not passed to Redis connection.
**Fix:** Added `password=os.getenv("REDIS_PASSWORD")` to the Redis connection.

---

## Bug 9 — `worker/worker.py`: Signal handlers imported but not implemented

**File:** `worker/worker.py`, line 4
**Problem:** `signal` was imported but no signal handlers were registered. Docker sends SIGTERM on shutdown — without a handler, the worker would be force-killed, potentially losing in-progress jobs.
**Fix:** Added `handle_shutdown()` function and registered handlers for both `SIGTERM` and `SIGINT`. The `running` flag allows the main loop to exit cleanly.

---

## Bug 10 — `frontend/app.js` line 5: API URL hardcoded to localhost

**File:** `frontend/app.js`, line 5
**Problem:** `const API_URL = "http:/
