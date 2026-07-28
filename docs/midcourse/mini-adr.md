# Mini Architecture Decision Record

## Project

Task Tracker Mid-Course Project

## Status

Accepted

## Selected Features

1. Search + Combined Filters
2. Due Dates + Overdue Filter

---

## Context

The existing Task Tracker application already supports creating, viewing, updating, deleting, and filtering tasks by status and priority.

For the mid-course project, two small end-to-end features were selected:

- Search tasks by text and combine the search with the existing status and priority filters.
- Add optional due dates with overdue identification and overdue filtering.

The implementation should remain simple, easy to understand, easy to test with pytest, and consistent with the existing project architecture.

---

# Decision 1: Extend the Existing Task List Endpoint

The existing `GET /tasks` endpoint will be extended with optional query parameters instead of creating additional endpoints.

Supported parameters:

- `search`
- `status`
- `priority`
- `overdue`

The `search` parameter performs case-insensitive partial matching against the task title and description.

When multiple parameters are supplied, all filters are combined using **AND** logic.

### Reason

The project already filters tasks through `GET /tasks`. Extending the existing endpoint keeps the API simple, avoids duplicate logic, and minimizes changes to the frontend.

### AI-Suggested Alternatives

The AI suggested:

- Creating a separate `/tasks/search` endpoint.
- Including the assignee field in search.
- Adding advanced search syntax.
- Adding pagination and sorting.

### Rejected Alternatives

These alternatives were rejected because they increased complexity and were outside the scope of the mid-course project.

---

# Decision 2: Store Due Dates as Optional Date Values

Each task stores an optional `due_date` field using a date-only value (`YYYY-MM-DD`).

A task is considered overdue only when:

- A due date exists.
- The due date is before today's date.
- The task status is not `Done`.

The existing `GET /tasks` endpoint accepts an optional `overdue=true` query parameter to return only overdue tasks.

### Reason

A date-only value satisfies the project requirements while avoiding unnecessary time and timezone complexity.

The overdue state is calculated dynamically instead of being stored, ensuring it always reflects the current date and task status.

### AI-Suggested Alternatives

The AI suggested:

- Storing a full date and time.
- Saving an `is_overdue` field.
- Creating a separate `/tasks/overdue` endpoint.
- Adding reminders or notifications.

### Rejected Alternatives

These alternatives were rejected because they introduced unnecessary complexity or exceeded the project scope.

---

# Frontend Decision

The existing frontend was extended without changing the overall user interface.

The following functionality was added:

- Optional Due Date field in the Create Task dialog.
- Optional Due Date field in the Edit Task dialog.
- Due date displayed on task cards.
- Visual **OVERDUE** badge for overdue tasks.
- Search, Status, Priority, and Overdue filter controls.

When editing a task, the frontend only sends the `status` field if the user actually changed it.

### Reason

The backend already rejects same-to-same status transitions (for example, `InProgress → InProgress`).

Avoiding unnecessary status updates preserves the existing business rule while allowing users to edit other fields, such as the due date.

---

# Consequences

## Positive

- Small and consistent REST API.
- Existing architecture preserved.
- Existing functionality remained unchanged.
- Features are easy to verify manually and through pytest.
- No additional storage or services were required.

## Limitations

- Search is limited to the task title and description.
- Overdue is based on the server's current date.
- No reminders or notifications are included.
- Advanced search, pagination, and sorting remain out of scope.