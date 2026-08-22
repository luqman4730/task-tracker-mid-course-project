# Architecture A: Task Tracker

## What The App Does

Task Tracker is a small learning-project task board with a FastAPI REST API and a single-page vanilla HTML/CSS/JavaScript frontend. Users can create, view, filter, edit, move, and delete tasks; the backend validates task shape and status transitions, then stores tasks in process-local memory.

## Data Model

Primary entity: `Task`.

Important fields: `id` UUID string, `title`, `description`, `status`, `priority`, `assignee`, `due_date`, `created_at`, and `updated_at`. Status values are `ToDo`, `InProgress`, and `Done`; priority values are `Low`, `Medium`, and `High`. Create defaults include `description=""`, `status=ToDo`, `priority=Medium`, `assignee=null`, and `due_date=null`.

## Request Flow

When a user creates a task, `frontend/index.html` collects form values and sends `POST /tasks` to `http://localhost:8000`. FastAPI receives the request in `app/main.py`, validates it against `TaskCreate` from `app/models.py`, rejects invalid or unknown fields with HTTP 422, then calls `storage.add_task`. The storage layer generates a UUID4 id, stamps UTC `created_at` and `updated_at`, stores the `TaskResponse` in an in-memory dictionary, and returns the created task with HTTP 201.

## Key Files

- `app/main.py` - FastAPI app setup, CORS configuration, health check, and task CRUD routes.
- `app/models.py` - Pydantic models plus task status and priority enums.
- `app/storage.py` - In-memory task dictionary, CRUD operations, filtering, UUID generation, and timestamps.
- `app/business_rules.py` - Allowed status transitions and 422 rejection for invalid transitions.
- `frontend/index.html` - Static single-page board UI, filters, modal form, drag/drop status updates, and API calls.
- `tests/test_tasks.py` - Main pytest coverage for CRUD, validation, filters, due dates, and transitions.
- `tests/conftest.py` - TestClient fixture and automatic in-memory store reset.
- `requirements.txt` - FastAPI, Uvicorn, Pydantic v2, pytest, httpx, and python-dotenv pins.
- `Dockerfile` - Two-stage Python 3.11 container build for running the API.
- `.github/workflows/ci.yml` - CI job that installs dependencies and runs pytest.

## Conventions

Validation lives in Pydantic models: request bodies forbid unknown fields, titles are stripped, blank titles are rejected, and titles are capped at 200 characters. Storage is an in-memory module-level dictionary in `app/storage.py`; data is lost when the process stops. Missing tasks return HTTP 404, invalid payloads return FastAPI/Pydantic HTTP 422, and invalid status transitions also return HTTP 422. `GET /tasks` supports `status`, `priority`, `search`, and `overdue` filters combined with AND logic. The frontend is served separately from the API and uses a hard-coded backend base URL of `http://localhost:8000`.

## Not Visible Or Assumptions

No durable database, authentication, authorization, pagination, sorting API, or production deployment configuration was visible in the inspected files. `app/repository.py`, `app/schemas.py`, and `app/services.py` exist but appear to be empty placeholders. The Docker image copies `frontend/`, but the FastAPI app does not visibly mount or serve it as static files. `.env.example` and `python-dotenv` are present, but no inspected backend file visibly reads environment settings.
