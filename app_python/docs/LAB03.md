# Lab 3 – CI/CD Pipeline

**Name:** Diana Yakupova  
**Group:** B23-CBS-02  
**Date:** 2026-02-12

---

## 1. Overview

- **Testing framework:** `pytest` – minimal boilerplate, powerful fixtures, industry standard.
- **Tests cover:**
  - `GET /` – HTTP 200, required JSON fields, service name and framework.
  - `GET /health` – HTTP 200, `"status": "healthy"`, timestamp, uptime.
  - `404` – returns JSON `{"error": "Not Found"}`.
- **CI triggers:**
  - `push` to `master` or `lab03`
  - `pull_request` to `master`
  - **Path filters:** only when `app_python/` or workflow file changes.
- **Versioning strategy:** **Calendar Versioning (CalVer)** – format `YYYY.MM.DD`.
  - Why? The app is a continuously delivered service, not a library. Date‑based tags are trivial to automate and clearly ordered.

---

## 2. Workflow Evidence

| Item                                                                       | Link / Output |
| -------------------------------------------------------------------------- | ------------- |
| `https://github.com/versceana/DevOps-Core-Course/actions/runs/21964172563` |
| ✅ **Local tests passing**                                                 |

```
$ pytest tests/ -v
=============================================================================
collected 4 items

test_app.py::test_main_endpoint_status PASSED
test_app.py::test_main_endpoint_json_structure PASSED
test_app.py::test_health_endpoint PASSED
test_app.py::test_404_error PASSED

================================ 4 passed in 0.15s =============================
```

`https://hub.docker.com/repository/docker/versceana/devops-info-service/general`

✅ **Status badge in README**
![Python CI](https://github.com/versceana/DevOps-Core-Course/actions/runs/21964172563)

---

## 3. Best Practices Implemented

| Practice                     | Implementation                                                                            | Benefit                                                |
| ---------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| **Fail fast**                | Workflow stops immediately on any failure                                                 | Saves CI minutes; prevents pushing broken code         |
| **Job dependencies**         | `docker` job `needs: test`                                                                | Only tested images are published                       |
| **Dependency caching**       | `actions/setup-python` with `cache: pip` + Docker layer caching                           | Install time reduced from ~2 min → ~20 sec (6× faster) |
| **Security scanning (Snyk)** | Snyk CLI installed via `npm`, explicit `snyk auth`, test with `--severity-threshold=high` | Catches vulnerable dependencies before deployment      |

**Snyk result:**  
No high or critical vulnerabilities found in `requirements.txt`.

---

## 4. Key Decisions

- **Versioning strategy:** **CalVer** – releases are date‑based, no need for semantic breaking‑change signaling.
- **Docker tags:** `latest` (rolling) and `YYYY.MM.DD` (immutable).
  - `latest` always points to the most recent build from `master`.
  - Date tag allows pinning to a specific day's release.
- **Workflow triggers:**
  - Run tests on every push/PR to catch issues early.
  - Push Docker images **only from the `master` branch** – avoids polluting registry with feature‑branch images.
- **Test coverage:** Not measured in the main task (bonus adds coverage tracking). Current tests cover all endpoints and error cases.

---

## 5. Challenges & Solutions

| Challenge                                 | Solution                                                                                                   |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Port 5000 already in use on macOS**     | Used `PORT=8000` locally; tests use Flask test client, no port conflict in CI.                             |
| **Docker push skipped on feature branch** | Condition `if: github.ref == 'refs/heads/master'` – correct, merged `lab03` into `master` to trigger push. |
| **Snyk could not find dependencies**      | Added `pip install` before `snyk test`.                                                                    |
| **Snyk authentication error (401)**       | Generated new Snyk API token, stored as `SNYK_TOKEN` secret, added explicit `snyk auth` step in workflow.  |

---

## 6. Conclusion

✅ **All main tasks completed successfully:**

- Unit tests written and passing.
- GitHub Actions workflow with lint, test, security scan, and Docker build/push.
- Dependency caching and Snyk integration.
- Full documentation with evidence.

The pipeline is now production‑ready and will be extended in future labs (monitoring, Kubernetes, GitOps).

---
