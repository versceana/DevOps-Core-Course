![Python CI](https://github.com/versceana/DevOps-Core-Course/actions/runs/21964172563)

# DevOps Info Service

A small web service that returns service, system and runtime information.  
Implemented for the DevOps Core Course (Lab 1) using **Python + Flask**.

---

## Overview

This service exposes two endpoints:

- `GET /` — Returns detailed information about the service, system, runtime and request.
- `GET /health` — Lightweight health check for monitoring/probes.

---

## Prerequisites

- **macOS** with Python (3.11+ recommended; tested on 3.13)
- `git`
- `curl` or `http` (HTTPie)
- (optional) `jq` for pretty-printing JSON

---

## Installation (macOS)

From the repository root:

```bash
cd DevOps-Core-Course/app_python

# create a virtual environment inside the project (recommended)
python -m venv venv
source venv/bin/activate   # macOS / Linux

# install pinned dependencies
pip install -r requirements.txt
```

> We keep the virtual environment inside `app_python/venv/`. This directory is listed in `.gitignore` and will not be committed.

---

## Running the application

### Basic

```bash
# default: binds to 0.0.0.0:5000
python app.py
```

### Custom host / port / debug

```bash
# custom port
PORT=8000 python app.py

# custom host and port
HOST=127.0.0.1 PORT=3000 python app.py

# enable debug mode
DEBUG=true python app.py
```

If port `5000` is already used (common on macOS), start on a different port (e.g., `8000`).

---

## API

### `GET /`

Returns a JSON object with keys: `service`, `system`, `runtime`, `request`, `endpoints`.

**Example request**

```bash
curl -s http://127.0.0.1:8000/ | jq .
```

**Example (sample output — will vary per machine)**

```json
{
  "service": {
    "name": "devops-info-service",
    "version": "1.0.0",
    "description": "DevOps course info service",
    "framework": "Flask"
  },
  "system": {
    "hostname": "MacBook-Pro-Diana-2.local",
    "platform": "Darwin",
    "platform_version": "25.2.0",
    "architecture": "arm64",
    "cpu_count": 8,
    "python_version": "3.13.0"
  },
  "runtime": {
    "uptime_seconds": 355,
    "uptime_human": "0 hours, 5 minutes",
    "current_time": "2026-01-28T19:52:46.995203+00:00",
    "timezone": "UTC"
  },
  "request": {
    "client_ip": "127.0.0.1",
    "user_agent": "curl/7.87.0",
    "method": "GET",
    "path": "/"
  },
  "endpoints": [
    { "path": "/", "method": "GET", "description": "Service information" },
    { "path": "/health", "method": "GET", "description": "Health check" }
  ]
}
```

### `GET /health`

Simple health JSON used for monitoring / readiness/liveness probes.

**Example**

```bash
curl -s http://127.0.0.1:8000/health | jq .
```

**Sample**

```json
{
  "status": "healthy",
  "timestamp": "2026-01-28T19:52:29.081981+00:00",
  "uptime_seconds": 337
}
```

**Status codes**

- `200 OK` — healthy
- `500` — internal server error (if thrown)

---

## Configuration

| Environment variable | Default   | Description                          |
| -------------------- | --------- | ------------------------------------ |
| `HOST`               | `0.0.0.0` | Host address to bind to              |
| `PORT`               | `5000`    | Port to listen on                    |
| `DEBUG`              | `false`   | Enable Flask debug mode (true/false) |

Use `PORT=8000` if `5000` is already in use on your machine.

---

## Testing

Quick checks:

```bash
# main endpoint
curl -s http://127.0.0.1:8000/ | jq .

# health
curl -s http://127.0.0.1:8000/health | jq .
```

If `jq` is not installed, use:

```bash
curl -s http://127.0.0.1:8000/ | python -m json.tool
```

---

## Project layout

```
app_python/
├── app.py                    # Main application
├── requirements.txt          # Pinned dependencies
├── venv/                     # (local) virtual environment - ignored by git
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── tests/                    # Unit tests (placeholder)
│   └── __init__.py
└── docs/
    ├── LAB01.md              # Lab submission notes
    └── screenshots/          # PNG screenshots for submission
```

---

## Notes & caveats

- This project uses Flask's development server for lab/demo purposes. For production or grading polish, a WSGI server (Gunicorn/uvicorn) + proper logging should be used.
- The code attempts to use UTC timestamps. There may be a `DeprecationWarning` about `utcnow()` on some Python versions; this does not affect lab functionality. A later commit will make datetime objects timezone-aware to remove the warning.

---

## Contributing / Submission

1. Implement changes on branch `lab01`.
2. Commit and push to your fork.
3. Create PR: `your-fork:lab01` → `inno-devops-labs/DevOps-Core-Course:master`.
4. Include screenshots from `app_python/docs/screenshots/` in the PR description.

---

## License

Educational project for DevOps Core Course.
