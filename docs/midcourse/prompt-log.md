# Prompt Log

## Project

Task Tracker Mid-Course Project

---

# Feature 1: Search + Combined Filters

## Prompt 1: Generate User Stories

### Role

You are a product owner writing user stories for a small development team.

### Context

I am extending an existing Task Tracker web application with a Python/FastAPI backend and a simple web frontend.

The existing application already supports:

- Create tasks
- View tasks
- Update tasks
- Delete tasks
- Filter by status and priority

New feature:

Search tasks by text and combine search with status and priority filters.

### Task

Generate 3–5 user stories for this feature.

### Constraints

- Use "team member" as the main role.
- Include 2–3 specific and testable acceptance criteria for each story.
- Cover happy paths and at least one failure case.
- Keep the feature small.
- Do not introduce pagination, saved searches, or advanced search syntax.

### Output Format

Return a table with columns:

`ID | Story | Acceptance Criteria | Notes / Assumptions`

### AI Response Summary

The AI generated user stories covering:

- Searching by task title
- Searching by task description
- Combining search with status and priority filters
- Clearing the search and filters
- Handling searches with no matching results

### Review Decision

- Accepted case-insensitive partial matching.
- Accepted searching title and description.
- Accepted combining filters using AND logic.
- Accepted an empty result list when no tasks match.
- Rejected advanced search syntax and saved searches.
- Edited the stories to keep them small and testable.

---

## Prompt 2: Design the Backend Search Behavior

### Role

You are a senior FastAPI backend developer reviewing a small learning project.

### Context

I have an existing Task Tracker REST API built with Python and FastAPI.

The existing `GET /tasks` endpoint already supports optional filtering by:

- Status
- Priority

Each task contains:

- ID
- Title
- Description
- Status
- Priority
- Assignee

I want to add text search without creating a separate endpoint.

### Task

Propose the smallest backend change needed to support text search and combined filtering.

The search should match task titles and descriptions.

### Constraints

- Extend the existing `GET /tasks` endpoint.
- Use an optional `search` query parameter.
- Search must be case-insensitive.
- Search must support partial text matching.
- Existing status and priority filters must continue to work.
- When multiple filters are supplied, combine them using AND logic.
- Do not add pagination, sorting, a database, or a new endpoint.
- Keep the implementation easy to understand and test with pytest.

### Output Format

Return:

1. Recommended endpoint behavior
2. Filtering order
3. Edge cases
4. Minimal implementation plan
5. Risks or assumptions

### AI Response Summary

The AI recommended extending `GET /tasks` with an optional `search` parameter and applying search, status, and priority filters to the same task collection.

The proposed search normalized both the query and task fields to lowercase before checking for partial matches.

### Review Decision

- Accepted extending the existing endpoint.
- Accepted title and description as searchable fields.
- Accepted case-insensitive partial matching.
- Accepted AND logic for all active filters.
- Rejected a separate `/tasks/search` endpoint.
- Rejected searching the assignee field because it was not required.
- Rejected pagination and sorting as out of scope.

---

## Prompt 3: Generate Backend Tests for Search and Combined Filters

### Role

You are a Python test engineer experienced with pytest and FastAPI TestClient.

### Context

The Task Tracker API now supports:

- `GET /tasks?search=...`
- `GET /tasks?status=...`
- `GET /tasks?priority=...`
- Combined search, status, and priority filters

Search is case-insensitive and matches partial text in the title or description.

### Task

Generate focused pytest tests for the new search and combined-filter behavior.

### Constraints

- Use the existing pytest and FastAPI TestClient setup.
- Keep each test independent.
- Create only the tasks needed by each test.
- Test title search.
- Test description search.
- Test case-insensitive search.
- Test partial matching.
- Test no matching results.
- Test search combined with status.
- Test search combined with priority.
- Test search combined with both status and priority.
- Do not modify unrelated tests or application behavior.

### Output Format

Return complete pytest test functions with clear names and short comments only where necessary.

### AI Response Summary

The AI generated tests for the main search behavior and combinations with existing filters.

The tests checked both successful matches and empty result lists.

### Review Decision

- Accepted the focused tests.
- Accepted independent task setup inside tests.
- Accepted testing combined filters explicitly.
- Edited test names to match the existing project style.
- Rejected unnecessary parameterized complexity for this small project.
- Ran the complete test suite after implementation.

---

## Prompt 4: Extend the Frontend Search Controls

### Role

You are a frontend developer working with plain HTML, CSS, and JavaScript.

### Context

The backend supports these optional query parameters on `GET /tasks`:

- `search`
- `status`
- `priority`

The existing frontend already displays tasks and includes status and priority filters.

### Task

Add a small search interface and update the task-loading logic so search can be combined with the existing filters.

### Constraints

- Use the existing frontend structure and styles.
- Add one search text field.
- Keep the existing status and priority filters.
- Build the query string only from active values.
- Refresh the task list when the user searches or changes a filter.
- Add a clear action that resets search and filters.
- Display the existing empty-state message when no tasks match.
- Do not add a frontend framework.
- Do not redesign the whole page.

### Output Format

Return:

1. Required HTML changes
2. Required JavaScript changes
3. Any minimal CSS changes
4. Manual verification steps

### AI Response Summary

The AI suggested adding a search input next to the existing filters and using `URLSearchParams` to construct the query string from active controls.

### Review Decision

- Accepted the search input.
- Accepted using the same task-loading function for all filters.
- Accepted a clear action for resetting filters.
- Reused the existing empty state.
- Rejected adding a framework or restructuring the page.

---

# Feature 2: Due Dates + Overdue Filtering

## Prompt 5: Generate User Stories

### Role

You are a product owner writing user stories for a small development team.

### Context

I am extending an existing Task Tracker web application with a Python/FastAPI backend and a simple web frontend.

The existing application already supports:

- Create tasks
- View tasks
- Update tasks
- Delete tasks
- Filter by status and priority

New feature:

Add optional due dates and overdue filtering.

### Task

Generate 3–5 user stories for this feature.

### Constraints

- Use "team member" as the main role.
- Include 2–3 specific and testable acceptance criteria for each story.
- Cover happy paths and at least one failure case.
- Keep the feature small.
- Do not introduce pagination, saved searches, or advanced search syntax.

### Output Format

Return a table with columns:

`ID | Story | Acceptance Criteria | Notes / Assumptions`

### AI Response Summary

The AI generated stories covering:

- Creating a task with an optional due date
- Viewing the due date
- Updating or removing the due date
- Identifying overdue tasks
- Filtering to show overdue tasks only
- Rejecting invalid date input

### Review Decision

- Accepted an optional date-only field.
- Accepted allowing the due date to be updated or removed.
- Accepted dynamic overdue calculation.
- Accepted excluding completed tasks from overdue results.
- Rejected reminders and notifications because they were out of scope.
- Edited the stories so the overdue rule was explicit and testable.

---

## Prompt 6: Design Due-Date and Overdue Backend Behavior

### Role

You are a senior FastAPI developer helping extend a small learning project.

### Context

The Task Tracker uses:

- Python
- FastAPI
- Pydantic models
- In-memory task storage
- JSON file persistence

Each task currently contains:

- ID
- Title
- Description
- Status
- Priority
- Assignee

Task statuses are:

- `ToDo`
- `InProgress`
- `Done`

### Task

Design the smallest backend change required to add an optional due date and overdue filtering.

### Constraints

- Add an optional `due_date` field.
- Use a date-only value in `YYYY-MM-DD` format.
- A missing due date must be stored and returned as `null`.
- Allow the due date to be added, updated, or removed.
- A task is overdue only when:
  - a due date exists
  - the due date is before today's date
  - the status is not `Done`
- A task due today is not overdue.
- Extend `GET /tasks` with an optional `overdue=true` query parameter.
- Overdue filtering must combine with search, status, and priority using AND logic.
- Do not store a separate `is_overdue` field.
- Do not add reminders, notifications, timestamps, or a new endpoint.

### Output Format

Return:

1. Model changes
2. Create and update behavior
3. Overdue rule
4. Filtering behavior
5. Edge cases
6. Minimal implementation plan

### AI Response Summary

The AI recommended using Python's date type for `due_date`, allowing `null`, and calculating overdue dynamically whenever tasks are returned or filtered.

### Review Decision

- Accepted a date-only field.
- Accepted `null` when no due date is provided.
- Accepted dynamic overdue calculation.
- Accepted that tasks due today are not overdue.
- Accepted excluding `Done` tasks from overdue results.
- Rejected storing an `is_overdue` boolean because it could become stale.
- Rejected a separate overdue endpoint.
- Rejected reminders and notifications.

---

## Prompt 7: Generate Due-Date and Overdue Tests

### Role

You are a Python test engineer using pytest and FastAPI TestClient.

### Context

The Task Tracker API now supports:

- Optional `due_date` values
- Creating a task with or without a due date
- Updating a due date
- Removing a due date by sending `null`
- `GET /tasks?overdue=true`

A task is overdue when its due date is before today and its status is not `Done`.

### Task

Generate focused tests for due-date validation, updates, removal, and overdue filtering.

### Constraints

- Use the existing test setup.
- Keep tests independent.
- Test creation with a valid due date.
- Test creation without a due date.
- Test invalid date input.
- Test updating a due date.
- Test removing a due date.
- Test that a past incomplete task is overdue.
- Test that a task due today is not overdue.
- Test that a future task is not overdue.
- Test that a completed task is not overdue.
- Test overdue combined with search, status, and priority.
- Do not change unrelated behavior.

### Output Format

Return complete pytest test functions with descriptive test names.

### AI Response Summary

The AI generated tests for valid and invalid due dates, update and removal behavior, the overdue rule, and combined filtering.

### Review Decision

- Accepted date validation tests.
- Accepted explicit tests for today, past, and future dates.
- Accepted checking completed tasks separately.
- Accepted combined-filter tests.
- Edited date setup to avoid hard-coded dates where practical.
- Ran the full test suite after the changes.

---

## Prompt 8: Extend the Frontend for Due Dates and Overdue Tasks

### Role

You are a frontend developer working with an existing HTML, CSS, and JavaScript Task Tracker.

### Context

The backend now supports:

- An optional `due_date` field
- Creating and updating due dates
- Removing a due date by sending `null`
- `GET /tasks?overdue=true`

The frontend already supports creating, displaying, editing, deleting, searching, and filtering tasks.

### Task

Add due-date input, due-date display, overdue indication, and an overdue filter to the existing frontend.

### Constraints

- Use `<input type="date">` for due dates.
- Keep the due date optional.
- Include the due date when creating a task only when entered.
- Allow users to update or remove a due date.
- Display the due date on each task card when present.
- Display an `OVERDUE` badge only when:
  - the due date is before today
  - the task is not `Done`
- Add an overdue-only checkbox or filter.
- Combine it with search, status, and priority filters.
- Preserve the existing design and JavaScript structure.
- Do not add a framework or redesign the application.

### Output Format

Return:

1. HTML changes
2. JavaScript changes
3. Minimal CSS changes
4. Manual verification checklist

### AI Response Summary

The AI proposed adding date inputs to the create and edit forms, displaying due dates on task cards, adding an overdue badge, and appending `overdue=true` when the overdue filter is active.

### Review Decision

- Accepted the date input.
- Accepted due-date display on cards.
- Accepted the overdue badge.
- Accepted combining the overdue checkbox with existing filters.
- Edited the update payload so `status` is sent only when the user changes it.
- Rejected adding reminders, notifications, and additional UI libraries.

---

# Prompt Refinement Example

## Weak Prompt

```text
Add due dates and overdue filtering to my Task Tracker.
```

## Problems with the Weak Prompt

- It does not describe the existing architecture.
- It does not define the overdue rule.
- It does not explain whether the due date is optional.
- It does not describe how due dates should be updated or removed.
- It does not specify how overdue filtering should combine with existing filters.
- It does not define the expected response format.
- It allows the AI to introduce unnecessary features.

## Improved Prompt

### Role

You are a senior FastAPI developer extending a small Task Tracker learning project.

### Context

The application uses Python, FastAPI, Pydantic, in-memory storage with JSON file persistence, and a plain HTML/CSS/JavaScript frontend.

The existing `GET /tasks` endpoint supports search, status, and priority filtering.

### Task

Add optional due dates and overdue filtering to the backend, frontend, and automated tests.

### Constraints

- Store `due_date` as an optional date-only value.
- Use `YYYY-MM-DD`.
- Return `null` when no due date exists.
- Allow the due date to be created, updated, or removed.
- A task is overdue only when its due date is before today and its status is not `Done`.
- A task due today is not overdue.
- Extend `GET /tasks` with `overdue=true`.
- Combine overdue with search, status, and priority using AND logic.
- Do not store `is_overdue`.
- Do not add reminders, notifications, timestamps, pagination, a database, or a new endpoint.
- Preserve existing behavior and tests.

### Output Format

Return:

1. Backend changes by file
2. Frontend changes by file
3. Pytest tests
4. Manual verification steps
5. Assumptions and rejected alternatives

### Improvement Result

The improved prompt produced a smaller and more relevant implementation plan, reduced unnecessary assumptions, and made the result easier to review and test.

---

# Final Review

AI assistance was used to:

- Generate and refine user stories
- Review backend design
- Suggest minimal implementation steps
- Generate focused automated tests
- Extend the existing frontend
- Identify edge cases
- Support manual verification
- Document accepted and rejected alternatives

All AI-generated suggestions were reviewed before implementation.

Changes were accepted only when they matched the project requirements, existing architecture, and scope.

The final project passed the complete automated test suite:

```text
39 passed
```
