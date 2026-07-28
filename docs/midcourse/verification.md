# Verification Report

## Project

Task Tracker Mid-Course Project

---

# Environment

- Python 3.13
- FastAPI
- pytest
- HTML / CSS / JavaScript frontend

---

# Automated Tests

Command:

```bash
python -m pytest
```

Result:

```
39 passed
```

All existing tests continued to pass after implementing the new features.

Additional tests were added for:

- Due date creation
- Due date updates
- Removing a due date
- Overdue filtering
- Search functionality
- Combined filtering

---

# Backend Verification

Verified manually using Swagger UI.

## Health endpoint

- GET `/health`
- Returned HTTP 200

## Task endpoints

Verified:

- Create task
- Retrieve task
- Update task
- Delete task
- Search tasks
- Status filtering
- Priority filtering
- Combined filtering
- Overdue filtering

Expected validation errors continued to return HTTP 422.

---

# Frontend Verification

Verified in the browser.

Confirmed that users can:

- Create tasks
- Edit tasks
- Delete tasks
- Assign a due date
- Remove a due date
- View due dates
- View overdue badges
- Search by title or description
- Filter by status
- Filter by priority
- Filter overdue tasks
- Combine multiple filters

The existing drag-and-drop status update functionality continued to work correctly.

---

# Regression Verification

The following existing functionality was verified after implementing the new features:

- Task creation
- Task editing
- Task deletion
- Status transitions
- Priority filtering
- Existing validation rules
- Existing API endpoints

No previously implemented functionality was intentionally changed.

---

# Break Test Verification

To verify that the automated tests detect regressions correctly, two intentional defects were introduced into the application.

## Break Test 1 – Blank title validation

Intentional change:

- Temporarily removed the validation that rejects blank task titles.

Verification:

- Ran the related pytest test.
- The test failed as expected because the API incorrectly accepted the invalid title.

Recovery:

- Restored the original validation.
- Re-ran the test.
- The test passed successfully.

Result:

- Confirmed that the automated test correctly detects regressions in title validation.

---

## Break Test 2 – Overdue filtering

Intentional change:

- Temporarily modified the overdue calculation so that completed tasks were incorrectly reported as overdue.

Verification:

- Ran the overdue filtering tests.
- The tests failed as expected.

Recovery:

- Restored the correct overdue logic.
- Re-ran the tests.
- All tests passed.

Result:

- Confirmed that the overdue filtering tests detect regressions correctly.

---

# Result

The project passed automated tests and manual verification.

The implemented features integrate with the existing application while preserving the original functionality.