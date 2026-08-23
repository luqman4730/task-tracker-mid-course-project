# Release Evidence

## Baseline

* Branch: `final-project`
* Date: 2026-08-23
* Local app run command: `python -m uvicorn app.main:app --reload --port 8000`
* `/health` result: HTTP `200 OK` with `{"status":"ok", ...}`
* Frontend check: Opened `frontend/index.html` using VS Code Live Server at `http://localhost:5500/frontend/index.html`. The Kanban board was visible, and both task creation and task editing worked normally.
* Test command: `python -m pytest`
* Test result: `40 passed in 0.31s`

## CI evidence

* Workflow file: `.github/workflows/ci.yml`
* Latest run: GitHub Actions CI run `#13`, `Complete final course project evidence`, on branch `final-project`, completed successfully on 2026-08-23.
* Test command used by CI: `python -m pytest -v`
* Python version: `3.11`
* Dependency installation: `pip install -r requirements.txt`
* Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.
* Optional prior evidence: an intentional failing CI run from Module 4 was followed by a successful restoration run.

## Docker evidence

* Build command: `docker build -t task-tracker-final .`
* Build result: successful; image created as `task-tracker-final:latest`
* Run command: `docker run --rm -p 8001:8000 task-tracker-final`
* `/health` check: `http://127.0.0.1:8001/health` returned HTTP `200 OK` with `{"status":"ok", ...}`
* Non-root check: `docker run --rm task-tracker-final whoami` returned `app`
* No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, `*.pem`, `*.key`, virtual environments, Git metadata, caches, tests, docs, and other files not required at runtime.
* Runtime command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

## Documentation claim-vs-reality log

| Claim checked                                                                                                           | Evidence used                                                                                                                                                                   | Result            | Change made, if any                                                          |
| ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------------------------------------------------------------------- |
| The full test suite runs with `python -m pytest -v` and reports 40 passing tests.                                       | Ran the suite locally from the repository root. Result: `40 passed in 0.31s`.                                                                                                   | Verified          | No change needed.                                                            |
| The Docker image builds, the container serves `/health`, and the runtime user is non-root.                              | Built `task-tracker-final`, ran it on host port 8001, verified `/health`, and ran `whoami` inside a fresh container.                                                            | Verified          | No change needed.                                                            |
| The documented local API command `uvicorn app.main:app --reload --port 8000` works reliably in the current environment. | The direct `uvicorn` command failed because the existing virtual environment referenced an old interpreter path. `python -m uvicorn app.main:app --reload --port 8000` worked successfully. | Needed correction | Updated README to use `python -m uvicorn app.main:app --reload --port 8000`. |
| The frontend can be opened with VS Code Live Server on port 5500.                                                       | Used VS Code `Go Live`; the Task Board opened at `http://localhost:5500/frontend/index.html`, and create/edit actions worked.                                                   | Verified          | No change needed.                                                            |
