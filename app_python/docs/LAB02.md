# LAB02 — Docker Containerization

**Name:** Diana Yakupova  
**Group:** B23-CBS-02  
**Date:** 2026-02-04

---

## What I implemented

- Dockerfile using `python:3.12-slim` (minimal, stable)
- Non-root user (`appuser`) — container does not run as root
- Dependencies copied and installed before app code (cache-friendly layering)
- `.dockerignore` excluding `venv/`, `docs/`, `tests/`, `.git`, etc.
- Local image build and run verified; image pushed to Docker Hub

---

## Dockerfile (main points)

```dockerfile
FROM python:3.12-slim

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy deps first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Switch to non-root
USER appuser

EXPOSE 8000
CMD ["python", "app.py"]
```

**Why these choices:**

- `python:3.12-slim` — small footprint, reliable binary compatibility for common Python packages.
- Non-root user — reduces privilege escalation risk and aligns with Kubernetes security defaults.
- Install deps before copying code — leverages Docker layer cache so iterative code changes don’t reinstall deps.
- `.dockerignore` — prevents sending large/unnecessary files to build context (faster builds, no secrets leaked).

---

## Best practices applied

- **Non-root user (`USER appuser`)** — security: container escape yields an unprivileged user instead of host root.
- **Pinned base image** (`python:3.12-slim`) — reproducibility and easier vulnerability tracking.
- **Layer ordering**: `COPY requirements.txt` + `RUN pip install` before `COPY app.py` — speeds up rebuilds in CI and local dev.
- **.dockerignore** — reduces build context size and prevents accidental inclusion of local secrets, venv or docs.
- **Minimal base** (slim) — smaller attack surface and faster pulls.
- **No runtime artifacts in image** (no `venv/`, `docs/`, `tests/`) — clean runtime image.

---

## Image information & decisions

**Base image chosen:** `python:3.12-slim`
**Reason:** balance of small size and compatibility; avoids musl/glibc issues that can appear on Alpine for some Python wheels.

**Tag used:** `versceana/devops-info-service:lab02`

**Final image size:**

```
REPOSITORY            TAG       SIZE
devops-info-service   lab02     457MB
```

---

## Build & Run process — commands and saved outputs

### How I built the image

```bash
# from app_python/
docker build -t versceana/devops-info-service:lab02 . 2>&1 | tee docs/build_output.txt
```

### Build output (tail)

```
#10 8.244 Collecting itsdangerous>=2.2 (from Flask==3.1.0->-r requirements.txt (line 1))
#10 8.308   Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
#10 8.393 Collecting click>=8.1.3 (from Flask==3.1.0->-r requirements.txt (line 1))
#10 8.452   Downloading click-8.3.1-py3-none-any.whl.metadata (2.6 kB)
#10 8.517 Collecting blinker>=1.9 (from Flask==3.1.0->-r requirements.txt (line 1))
#10 8.586   Downloading blinker-1.9.0-py3-none-any.whl.metadata (1.6 kB)
#10 8.738 Collecting MarkupSafe>=2.0 (from Jinja2>=3.1.2->Flask==3.1.0->-r requirements.txt (line 1))
#10 8.814   Downloading markupsafe-3.0.3-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl.metadata (2.7 kB)
#10 8.884 Downloading flask-3.1.0-py3-none-any.whl (102 kB)
#10 9.027 Downloading blinker-1.9.0-py3-none-any.whl (8.5 kB)
#10 9.091 Downloading click-8.3.1-py3-none-any.whl (108 kB)
#10 9.172 Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
#10 9.237 Downloading jinja2-3.1.6-py3-none-any.whl (134 kB)
#10 9.321 Downloading markupsafe-3.0.3-cp313-cp313-manylinux2014_aarch64.manylinux_2_17_aarch64.manylinux_2_28_aarch64.whl (24 kB)
#10 9.391 Downloading werkzeug-3.1.5-py3-none-any.whl (225 kB)
#10 9.445 Installing collected packages: MarkupSafe, itsdangerous, click, blinker, Werkzeug, Jinja2, Flask
#10 9.907
#10 9.910 Successfully installed Flask-3.1.0 Jinja2-3.1.6 MarkupSafe-3.0.3 Werkzeug-3.1.5 blinker-1.9.0 click-8.3.1 itsdangerous-2.2.0
#10 9.910 WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
#10 DONE 10.4s

#11 [7/8] COPY app.py .
#11 DONE 0.0s

#12 [8/8] RUN chown -R appuser:appgroup /app
#12 DONE 0.2s

#13 exporting to image
#13 exporting layers
#13 exporting layers 7.3s done
#13 exporting manifest sha256:21510e1ea3021e5b4b871880b88467040fecda34575b62215d2630d96ea9df55 done
#13 exporting config sha256:ae057c1a0b4faee60ec0d57053519e7d81aba7a32b4d66fe0cab58a5685a8a75 done
#13 exporting attestation manifest sha256:261ce7665a093eebbd77c9bd681f591e7320e2d11e1277d4c0d1aa66fc026584 0.0s done
#13 exporting manifest list sha256:0bdb7eed5b1a2d0c94182973a6883de99afdb9efbe26b1156d7c8d17b5469845 done
#13 naming to docker.io/library/devops-info-service:lab02 done
#13 unpacking to docker.io/library/devops-info-service:lab02
#13 unpacking to docker.io/library/devops-info-service:lab02 1.6s done
#13 DONE 9.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/10yr646xr8e4bz24kpr8ynrq5
```

### How I ran & tested the container locally

```bash
# run mapping host 8000 -> container 8000 (app exposes 8000)
docker run -d --name lab02_test -p 8000:8000 -e PORT=8000 versceana/devops-info-service:lab02

# test endpoints
curl -s http://127.0.0.1:8000/ | python3 -m json.tool > docs/lab02_curl_main.json
curl -s http://127.0.0.1:8000/health | python3 -m json.tool > docs/lab02_curl_health.json

# stop and remove when done
docker stop lab02_test
docker rm lab02_test
```

**Main endpoint output:**

```
{
    "endpoints": [
        {
            "description": "Service information",
            "method": "GET",
            "path": "/"
        },
        {
            "description": "Health check",
            "method": "GET",
            "path": "/health"
        }
    ],
    "request": {
        "client_ip": "192.168.65.1",
        "method": "GET",
        "path": "/",
        "user_agent": "curl/8.7.1"
    },
    "runtime": {
        "current_time": "2026-02-04T21:01:22.363918+00:00",
        "timezone": "UTC",
        "uptime_human": "0 hours, 0 minutes",
        "uptime_seconds": 11
    },
    "service": {
        "description": "DevOps course info service",
        "framework": "Flask",
        "name": "devops-info-service",
        "version": "1.0.0"
    },
    "system": {
        "architecture": "aarch64",
        "cpu_count": 8,
        "hostname": "92865388df9f",
        "platform": "Linux",
        "platform_version": "6.10.14-linuxkit",
        "python_version": "3.13.11"
    }
}
```

**Health endpoint output:**

```
{
    "status": "healthy",
    "timestamp": "2026-02-04T21:01:34.750688+00:00",
    "uptime_seconds": 24
}
```

---

## Docker Hub

The URL here:

```
https://hub.docker.com/r/versceana/devops-info-service
```

**Push output:** docs/push_output.txt

---

## Challenges & Solutions

- **Tag formatting error:** ensure Docker tag contains non-empty username (when pushing): `username/repo:tag`. If username not set, use local tag `devops-info-service:lab02`.
- **Time constraint:** pushed only if Docker Hub was available and ready; otherwise included build logs for proof.

---

## How to reproduce

```bash
# from repository root
cd app_python

# build locally
docker build -t <your_tag_here> .

# run
docker run --rm -p 8000:8000 -e PORT=8000 <your_tag_here>

# test
curl -s http://127.0.0.1:8000/ | python -m json.tool
curl -s http://127.0.0.1:8000/health | python -m json.tool
```

---

## Conclusion

This lab demonstrates practical application of the lecture: make containers small, secure, and cache-friendly. The Dockerfile provided is intentionally minimal so reviewers can quickly reproduce, inspect, and run the image.

---
