# Task Tracker Architecture

## 1. What The App Does

Task Tracker is a small learning application with a FastAPI backend and a single-page vanilla HTML/CSS/JavaScript frontend. It supports task CRUD operations, filtering, health checks, and validation of allowed task status transitions. Task data is stored in process-local memory and is not durable across application restarts.

## 2. Data Model

The core entity is a task.

Important task fields include:

- `id`: UUID4-generated task identifier.
- `title`: Required on create, trimmed, non-blank, and limited to 200 characters.
- `description`: Optional text, defaulting to an empty string.
- `status`: One of `ToDo`, `InProgress`, or `Done`; defaults to `ToDo`.
- `priority`: One of `Low`, `Medium`, or `High`; defaults to `Medium`.
- `assignee`: Optional assignee value, defaulting to `None`.
- `due_date`: Optional due date, defaulting to `None`.
- `created_at`: UTC timestamp assigned when the task is created.
- `updated_at`: UTC timestamp updated when the task changes.

## 3. Request Flow

When a user creates a task, the frontend sends a request to the FastAPI backend using the hard-coded API base `http://localhost:8000`. The backend route in `app/main.py` receives the create payload and validates it using Pydantic models from `app/models.py`. Unknown fields are rejected, the title is validated, and defaults are applied for omitted optional fields. Storage logic in `app/storage.py` generates a UUID4 task ID, stamps UTC timestamps, stores the task in an in-memory dictionary, and returns the created task response.

## 4. Key Files

- `app/main.py` - Defines the FastAPI app, CORS configuration, health endpoint, and task CRUD/filtering routes.
- `app/models.py` - Defines task models, validation rules, status values, and priority values.
- `app/storage.py` - Implements in-memory task storage, CRUD behavior, filtering, UUID generation, and timestamps.
- `app/business_rules.py` - Defines valid task status transitions and rejects invalid transitions.
- `frontend/index.html` - Provides the single-page vanilla frontend and calls the backend API.
- `tests/conftest.py` - Resets the in-memory task store around each test.
- `requirements.txt` - Confirms FastAPI, Uvicorn, Pydantic v2, pytest, and httpx dependencies.
- `Dockerfile` - Confirms Docker support and Python 3.11 runtime context.

## 5. Conventions

Validation is handled through Pydantic models. Create and update payloads forbid unknown fields. Task titles are required on create and must be valid after trimming; explicit invalid update titles are rejected. Status changes are governed by explicit transition rules: `ToDo -> InProgress`, `InProgress -> Done`, and `Done -> InProgress`; other transitions return HTTP 422. Missing tasks return HTTP 404. Storage is an in-memory dictionary in `app/storage.py`, so data is lost when the process stops. The frontend is a static vanilla page that talks to the backend at `http://localhost:8000`.

## 6. Not Visible Or Assumptions

Durable persistence, database migrations, authentication, authorization, deployment architecture, linting, formatting, type-checking, coverage tooling, and frontend build tooling are not confirmed. `app/repository.py`, `app/schemas.py`, and `app/services.py` are described as placeholders with no active implementation.
