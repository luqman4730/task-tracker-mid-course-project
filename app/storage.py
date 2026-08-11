from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create a task from a validated payload and store it.

    Generates a UUID4 identifier and stamps ``created_at`` and ``updated_at``
    with the same current UTC time. A missing or ``None`` description is stored
    as an empty string.

    Args:
        payload: The validated creation payload.

    Returns:
        TaskResponse: The newly stored task.
    """
    now = datetime.now(timezone.utc)
    task = TaskResponse(
        id=str(uuid4()),
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task.id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    """Return the stored tasks, applying any supplied filters.

    Filters are applied in sequence, so a task must satisfy every supplied
    filter to be returned. The result order follows insertion order of the
    underlying dict.

    Args:
        status: Keep only tasks whose status equals this value. ``None`` skips
            the status filter.
        priority: Keep only tasks whose priority equals this value. ``None``
            skips the priority filter.
        search: Case-insensitive (``casefold``) substring matched against the
            task title or description, after stripping surrounding whitespace.
            ``None`` or a blank/whitespace-only string skips the search filter.
        overdue: Only the value ``True`` filters; it keeps tasks whose
            ``due_date`` is not ``None``, is strictly earlier than today's local
            date, and whose status is not ``Done``. ``False`` and ``None`` both
            skip the overdue filter.

    Returns:
        list[TaskResponse]: A new list of the matching tasks.
    """
    tasks = list(_tasks.values())

    if status is not None:
        tasks = [task for task in tasks if task.status == status]

    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]

    if search is not None and search.strip():
        search_text = search.strip().casefold()

        tasks = [
            task
            for task in tasks
            if search_text in task.title.casefold()
            or search_text in task.description.casefold()
        ]

    if overdue is True:
        today = date.today()
        tasks = [
            task
            for task in tasks
            if task.due_date is not None
            and task.due_date < today
            and task.status != TaskStatus.DONE
        ]

    return tasks
    
def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a single task by identifier.

    Args:
        task_id: The identifier to look up.

    Returns:
        Optional[TaskResponse]: The stored task, or ``None`` if no task has this
            identifier.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to a stored task.

    Only fields explicitly set on the payload are applied (``exclude_unset``).
    If nothing was set, the stored task is returned unchanged and its
    ``updated_at`` is not bumped. Otherwise a copy is stored with the supplied
    fields replaced and ``updated_at`` set to the current UTC time.

    Note:
        The copy is made with ``model_copy``, which does not re-run validation,
        so a field explicitly set to ``None`` in the payload is written through
        as ``None``.

    Args:
        task_id: Identifier of the task to update.
        payload: The fields to change.

    Returns:
        Optional[TaskResponse]: The task after the update, or ``None`` if no
            task has this identifier.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    updated = task.model_copy(
        update={**updates, "updated_at": datetime.now(timezone.utc)}
    )
    _tasks[task_id] = updated
    return updated


def delete_task(task_id: str) -> bool:
    """Remove a task from the store.

    Args:
        task_id: Identifier of the task to remove.

    Returns:
        bool: ``True`` if a task was removed, ``False`` if no task had this
            identifier.
    """
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()
