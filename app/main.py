"""
Task Tracker API - Application Entry Point

This module creates the FastAPI application, configures CORS,
and defines the health-check and task CRUD endpoints.
Task storage and status-transition rules are handled by
the storage and business-rules modules.
"""

from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate


app = FastAPI(
    title="Task Tracker API",
    description="A minimal learning-project REST API for tracking tasks.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:8000",
        "http://localhost:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)


@app.get("/health", tags=["health"])
def health_check() -> dict:
    """Report service liveness.

    Route:
        GET /health

    Returns:
        dict: A mapping with ``status`` set to ``"ok"`` and ``timestamp`` set to
            the current UTC time as an ISO-8601 string.

    Example:
        Request::

            GET /health

        Response (200)::

            {"status": "ok", "timestamp": "2026-08-11T12:00:00+00:00"}
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    search: str | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally narrowed by query-string filters.

    All filters are optional and are combined with AND by the storage layer.
    Filtering is delegated to :func:`app.storage.get_all_tasks`; see that
    function for the exact matching rules.

    Route:
        GET /tasks

    Args:
        status: Keep only tasks whose status equals this value. ``None`` applies
            no status filter.
        priority: Keep only tasks whose priority equals this value. ``None``
            applies no priority filter.
        search: Case-insensitive substring matched against a task's title or
            description. ``None`` or a blank/whitespace-only string applies no
            search filter.
        overdue: When ``True``, keep only tasks with a ``due_date`` strictly
            before today whose status is not ``Done``. ``False`` and ``None``
            both apply no overdue filter.

    Returns:
        list[TaskResponse]: The matching tasks. Empty when nothing matches.

    Example:
        Request::

            GET /tasks?status=InProgress&priority=High&search=report

        Response (200)::

            [
              {
                "id": "6f1c...",
                "title": "Write report",
                "description": "",
                "status": "InProgress",
                "priority": "High",
                "assignee": null,
                "due_date": null,
                "created_at": "2026-08-11T12:00:00+00:00",
                "updated_at": "2026-08-11T12:00:00+00:00"
              }
            ]
    """
    return storage.get_all_tasks(
        status=status,
        priority=priority,
        search=search,
        overdue=overdue,
    )
    
@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by its identifier.

    Route:
        GET /tasks/{task_id}

    Args:
        task_id: Identifier of the task to fetch.

    Returns:
        TaskResponse: The stored task.

    Raises:
        HTTPException: 404 Not Found if no task has this identifier.

    Example:
        Request::

            GET /tasks/6f1c0f6a-2a58-4a2f-9d0c-1a2b3c4d5e6f

        Response (404)::

            {"detail": "Task with id 6f1c0f6a-2a58-4a2f-9d0c-1a2b3c4d5e6f not found"}
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a task and store it.

    The identifier and the ``created_at``/``updated_at`` timestamps are assigned
    by the storage layer; they are not accepted from the request body.

    Route:
        POST /tasks

    Args:
        payload: Validated request body. ``title`` is required; ``status``
            defaults to ``ToDo`` and ``priority`` to ``Medium``.

    Returns:
        TaskResponse: The created task, including its generated ``id`` and
            timestamps. Sent with HTTP 201 Created.

    Raises:
        RequestValidationError: Raised by FastAPI (surfaced as HTTP 422) when
            the body fails ``TaskCreate`` validation - for example a blank
            title, a title longer than 200 characters, or an unknown field
            (the model sets ``extra="forbid"``).

    Example:
        Request::

            POST /tasks
            {"title": "Write report", "priority": "High"}

        Response (201)::

            {
              "id": "6f1c...",
              "title": "Write report",
              "description": "",
              "status": "ToDo",
              "priority": "High",
              "assignee": null,
              "due_date": null,
              "created_at": "2026-08-11T12:00:00+00:00",
              "updated_at": "2026-08-11T12:00:00+00:00"
            }
    """
    return storage.add_task(payload)


@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update a task, enforcing the status-transition rules.

    Only fields present in the request body are changed. When the body includes
    ``status``, the existing task is loaded first so that a missing task yields
    404 before the transition is checked, and the transition is validated
    before any write occurs.

    Route:
        PATCH /tasks/{task_id}

    Args:
        task_id: Identifier of the task to update.
        payload: Validated request body holding the fields to change. Fields
            left out are untouched.

    Returns:
        TaskResponse: The updated task. If the request body is an empty JSON
            object (``{}``), the task is returned unchanged (including its
            original ``updated_at``).
            
    Raises:
        HTTPException: 404 Not Found if no task has this identifier.
        HTTPException: 422 Unprocessable Entity if ``status`` is present and the
            move from the task's current status to the requested one is not in
            :data:`app.business_rules.VALID_TRANSITIONS`.
        RequestValidationError: Raised by FastAPI (surfaced as HTTP 422) when
            the body fails ``TaskUpdate`` validation - for example an explicit
            ``"title": null``, a blank title, a title longer than 200
            characters, or an unknown field (``extra="forbid"``).

    Example:
        Request::

            PATCH /tasks/6f1c...
            {"status": "Done"}

        Response (422) when the task is still ``ToDo``::

            {"detail": "Invalid status transition from ToDo to Done. Allowed transitions: ['Done->InProgress', 'InProgress->Done', 'ToDo->InProgress']"}
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    """Delete a task.

    Route:
        DELETE /tasks/{task_id}

    Args:
        task_id: Identifier of the task to delete.

    Returns:
        None: Sent with HTTP 204 No Content and an empty body.

    Raises:
        HTTPException: 404 Not Found if no task has this identifier.

    Example:
        Request::

            DELETE /tasks/6f1c0f6a-2a58-4a2f-9d0c-1a2b3c4d5e6f

        Response (204): empty body.
    """
    if storage.delete_task(task_id):
        return
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")