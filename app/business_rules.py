from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    """Reject a status change that is not an allowed transition.

    A change is allowed only if the ``(current, new)`` pair is a member of
    :data:`VALID_TRANSITIONS`. Every other pair is rejected, including a
    same-status pair such as ``ToDo -> ToDo``.

    Args:
        current: The task's status before the change.
        new: The status being requested.

    Returns:
        None: Returns normally when the transition is allowed.

    Raises:
        HTTPException: 422 Unprocessable Entity when the pair is not in
            :data:`VALID_TRANSITIONS`. The detail message names both statuses
            and lists the allowed transitions in sorted ``"From->To"`` form.
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )
