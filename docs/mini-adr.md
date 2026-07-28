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

For the mid-course project, two small end-to-end features will be added:

- Text search combined with the existing status and priority filters.
- Optional due dates with overdue identification and filtering.

The design must remain simple, easy to test, and suitable for a small learning project.

---

## Decision 1: Extend the Existing Task List Endpoint

Search and filtering will be implemented by extending the existing `GET /tasks` endpoint with optional query parameters.

The endpoint will support:

- `search`
- `status`
- `priority`
- `overdue`

The `search` parameter will match task titles and descriptions using case-insensitive text matching.

When multiple parameters are provided, the filters will use AND logic. A task must satisfy all selected conditions to appear in the result.

### Reason

The application already uses `GET /tasks` for status and priority filtering. Extending the same endpoint keeps the API small and avoids creating unnecessary endpoints.

### AI-Suggested Alternatives

The AI suggested:

- Creating a separate `/tasks/search` endpoint.
- Searching title, description, and assignee.
- Adding advanced search syntax.
- Adding pagination and sorting.

### Rejected Alternatives

A separate search endpoint was rejected because it would duplicate task-listing behavior.

Searching the assignee field was rejected to keep the selected feature limited to title and description.

Advanced search syntax, pagination, and sorting were rejected as too complex and outside the scope of the mid-course project.

---

## Decision 2: Store Due Dates as Optional Date-Only Values

Each task will have an optional `due_date` field.

The field will use a date-only value in the following format:

```text
YYYY-MM-DD