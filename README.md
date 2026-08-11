# Task Tracker

A small full-stack Task Tracker learning project for Module 4, built with FastAPI and a
single-page vanilla HTML/CSS/JavaScript frontend.

## 1. Project overview

The API exposes CRUD operations over an in-memory list of tasks, plus filtering and a
status-transition rule set. There is no database and no persistence: the store is a
plain dictionary in `app/storage.py`, so **all tasks are lost when the process stops**.

Each task has an `id`, `title`, `description`, `status`, `priority`, `assignee`,
`due_date`, `created_at`, and `updated_at`.

| Method | Path          | Purpose                                                   |
| ------ | ------------- | --------------------------------------------------------- |
| GET    | `/health`     | Liveness check; returns status and a UTC timestamp        |
| GET    | `/tasks`      | List tasks, with optional filters (see below)             |
| GET    | `/tasks/{id}` | Fetch one task, or 404                                    |
| POST   | `/tasks`      | Create a task; returns 201                                |
| PATCH  | `/tasks/{id}` | Partially update a task; enforces status transitions      |
| DELETE | `/tasks/{id}` | Delete a task; returns 204                                |

`GET /tasks` accepts four optional query parameters, combined with AND logic:

- `status` - one of `ToDo`, `InProgress`, `Done`
- `priority` - one of `Low`, `Medium`, `High`
- `search` - case-insensitive substring matched against title or description
- `overdue` - when `true`, keeps tasks whose `due_date` is before today and whose
  status is not `Done`. A task due today is not overdue. Passing `overdue=false`
  applies no filter rather than inverting it.

Status changes are restricted to `ToDo -> InProgress`, `InProgress -> Done`, and
`Done -> InProgress`. Every other change, including re-sending a task's current status,
is rejected with 422. The rules live in `app/business_rules.py`.

## 2. Prerequisites

- Python 3.11 - matches the Dockerfile and the CI workflow
- A modern web browser, to use the frontend
- Docker, only for the container workflow in section 6

## 3. Local setup

Run everything from the repository root.

```bash
python -m venv venv
```

Activate the environment.

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
venv\Scripts\activate.bat
```

macOS or Linux:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## 4. Run the app locally

Start the API from the repository root:

```bash
uvicorn app.main:app --reload --port 8000
```

- API root: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

The frontend is a static file and is not served by FastAPI, so it needs its own
server. Leave the API running and, in a second terminal from the repository root:

```bash
python -m http.server 5500
```

Then open `http://localhost:5500/frontend/index.html`. The page calls the API at the
hard-coded `API_BASE` of `http://localhost:8000` (`frontend/index.html`), and that
origin is one of the four allowed by the CORS middleware in `app/main.py`, alongside
`http://127.0.0.1:8000`, `http://localhost:5173`, and `null`.

Opening `frontend/index.html` with the VS Code Live Server extension works too, and
also lands on port 5500 by default.

## 5. Run tests

```bash
python -m pytest -v
```

The suite currently reports **40 passed**. Tests use FastAPI's `TestClient`, and an
autouse fixture in `tests/conftest.py` clears the in-memory store around every test, so
no server needs to be running.

All 40 tests live in `tests/test_tasks.py`, status transitions included.
`tests/test_status_transitions.py` is an empty file and contributes nothing.
`tests/verify_a.py` is a manual print-based script rather than a pytest module - it
defines no `test_` functions, so pytest collects nothing from it. Run it as a module if
you want its output - `python tests/verify_a.py` fails with `No module named 'app'`,
because that form does not put the repository root on `sys.path`:

```bash
python -m tests.verify_a
```

[VERIFY] Whether `tests/test_status_transitions.py` is meant to be empty, and whether
`tests/verify_a.py` should be folded into the pytest suite or removed.

## 6. Run with Docker

The `Dockerfile` is a two-stage build: a builder stage installs dependencies into
`/opt/venv`, and a `python:3.11-slim` runtime stage copies that venv plus `app/` and
`frontend/`. The container runs as a non-root user (`app`, uid 10001) and declares a
`HEALTHCHECK` against `/health`.

Build:

```bash
docker build -t task-tracker .
```

Run:

```bash
docker run --rm -p 8000:8000 task-tracker
```

The container serves the API on `http://localhost:8000`. It binds `0.0.0.0` inside the
container and runs without `--reload`.

Note that `tests/`, `docs/`, and `data/` are excluded by `.dockerignore`, so the image
cannot run the test suite.

## 7. CI workflow summary

`.github/workflows/ci.yml` defines a single `test` job with no branch filter, so it
runs on **every push and every pull request**. On `ubuntu-latest` it:

1. Checks out the repository (`actions/checkout@v4`)
2. Sets up Python 3.11 (`actions/setup-python@v5`)
3. Upgrades pip and installs `requirements.txt`
4. Runs `python -m pytest -v`

There is no linting, coverage gate, dependency cache, build step, or Docker step in the
workflow - a failing test is the only thing that fails CI.

## 8. Project structure

```text
task-tracker/
├── app/
│   ├── __init__.py
│   ├── main.py             # FastAPI app, CORS config, all route handlers
│   ├── models.py           # Pydantic v2 models and the TaskStatus/TaskPriority enums
│   ├── storage.py          # In-memory dict store and its filtering logic
│   ├── business_rules.py   # VALID_TRANSITIONS and validate_status_transition
│   ├── repository.py       # empty placeholder
│   ├── schemas.py          # empty placeholder
│   └── services.py         # empty placeholder
├── frontend/
│   └── index.html          # Single-page UI: HTML, CSS, and JS in one file
├── tests/
│   ├── conftest.py                  # client / created_task fixtures, store reset
│   ├── test_tasks.py                # all 40 tests
│   ├── test_status_transitions.py   # empty
│   └── verify_a.py                  # manual script, not collected by pytest
├── docs/
│   └── midcourse/          # user stories, mini-ADR, verification, prompt log, reflection
├── data/                   # empty; see limitations
├── .github/workflows/ci.yml
├── Dockerfile
├── .dockerignore
├── requirements.txt
├── .env.example            # PORT, APP_ENV
├── CLAUDE.md               # Guidance for Claude Code
└── README.md
```

## 9. Project conventions and current limitations

Conventions:

- Business rules stay in `app/business_rules.py` and are called from the route handler
  in `app/main.py` before any write, so a missing task returns 404 before a transition
  is checked.
- `TaskCreate`, `TaskUpdate`, and `TaskResponse` all set `extra="forbid"`, so an unknown
  field in a request body is a 422 rather than being ignored.
- Titles are stripped and capped at 200 characters; a blank title is rejected.
- Public functions and route handlers carry Google-style docstrings.
- Do not commit virtual environments, caches, credentials, or private data. `.env` is
  gitignored; `.env.example` is the tracked template.

Limitations, all deliberate for this module:

- **No persistence.** Data lives in a process-local dictionary and is gone on restart.
  There is no database.
- **No authentication, accounts, or authorization.** Every endpoint is open.
- **Single-process only.** The in-memory store is not shared across workers, so running
  more than one uvicorn worker gives inconsistent results.
- **Not deployment-ready**, and nothing here has been assessed for production use. The
  Dockerfile exists for local container runs only.
- `app/repository.py`, `app/schemas.py`, and `app/services.py` are empty placeholder
  files.
- The `data/` directory is empty and nothing in `app/` writes to it, even though
  `.gitignore` reserves `data/tasks.json`. [VERIFY] Whether JSON file persistence is
  planned or was abandoned - the previous README claimed it exists, but no code does it.
- `.env` and `.env.example` define `PORT` and `APP_ENV`, and `python-dotenv` is pinned in
  `requirements.txt`, but no module reads them, so setting them has no effect today.
  [VERIFY] Whether these are intended for later use.
- The Dockerfile copies `frontend/` into the image, but the app never mounts static
  files, so the UI is not reachable from the container. [VERIFY] Whether the image is
  meant to serve the frontend.
- `PATCH` applies updates with `model_copy`, which does not re-validate, so an explicit
  `"description": null` is written through as `null` even though the response model
  declares it a string.
- No pagination, sorting, notifications, or bulk operations.

## 10. Technical notes

The mid-course documentation is in `docs/midcourse/`:

- [`mini-adr.md`](docs/midcourse/mini-adr.md) - architecture decision record
- [`user-stories.md`](docs/midcourse/user-stories.md)
- [`verification.md`](docs/midcourse/verification.md)
- [`prompt-log.md`](docs/midcourse/prompt-log.md)
- [`reflection.md`](docs/midcourse/reflection.md)

There is no `docs/decisions/` directory in this repository; `docs/midcourse/mini-adr.md`
is the decision record.
