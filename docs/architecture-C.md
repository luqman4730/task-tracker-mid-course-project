# Task Tracker Architecture

## 1. What The App Does

Task Tracker is a FastAPI REST API for creating, listing, retrieving, partially updating, and deleting tasks. It also exposes a `/health` endpoint and supports filtering tasks by status, priority, search text, and overdue state.

## 2. Data Model

Primary entity: `Task`.

Important fields:
- `id`: string UUID generated when a task is created.
- `title`: required on create, stripped of whitespace, non-blank, maximum 200 characters.
- `description`: optional, defaults to an empty string.
- `status`: one of `ToDo`, `InProgress`, or `Done`; defaults to `ToDo`.
- `priority`: one of `Low`, `Medium`, or `High`; defaults to `Medium`.
- `assignee`: optional string.
- `due_date`: optional date.
- `created_at`: UTC timestamp assigned on create.
- `updated_at`: UTC timestamp assigned on create and changed on non-empty updates.

## 3. Request Flow

When a user creates a task with `POST /tasks`, FastAPI validates the request body against `TaskCreate`. The API then calls `storage.add_task(payload)`, which creates a `TaskResponse`, generates a UUID4 `id`, sets `created_at` and `updated_at` to the current UTC time, normalizes a missing or `None` description to `""`, stores the task in the module-level `_tasks` dictionary, and returns the created task with HTTP 201.

## 4. Key Files

- `app/main.py`: FastAPI application setup, CORS configuration, health endpoint, and task CRUD route handlers.
- `app/models.py`: Pydantic models and enums for task creation, updates, responses, statuses, and priorities.
- `app/storage.py`: In-memory task storage and functions for create, read, update, delete, filtering, and reset.
- `app/business_rules.py`: Referenced for status-transition validation, but implementation is not visible from the files I read.
- Frontend file: not visible from the files I read.
- Test files: not visible from the files I read.

## 5. Conventions

Validation:
Request payloads use Pydantic models with `extra="forbid"`. Task titles are stripped, cannot be blank, and cannot exceed 200 characters. Explicit `null` title values are rejected on update.

Storage:
Tasks are stored in a module-level in-memory dictionary named `_tasks`. IDs are generated with UUID4. Timestamps are timezone-aware UTC datetimes. Persistence beyond process memory is not visible from the files I read.

Error handling:
Missing tasks return HTTP 404 from route handlers. Invalid request bodies are handled by FastAPI/Pydantic as validation errors. Invalid status-transition handling is delegated to `app.business_rules.validate_status_transition`, but the exact rules are not visible from the files I read.

Frontend/backend interaction:
CORS allows `http://localhost:5500`, `http://127.0.0.1:8000`, and `http://localhost:5173`. Any actual frontend implementation or API base URL is not visible from the files I read.

## 6. Not Visible Or Assumptions

- Status-transition rules are not visible from the files I read.
- Frontend behavior is not visible from the files I read.
- Test coverage is not visible from the files I read.
- Dependency versions are not visible from the files I read.
- Deployment, Docker, CI, linting, formatting, and type-checking setup are not visible from the files I read.
- Durable persistence or database support is not visible from the files I read.
