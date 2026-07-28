# Verification

## Baseline Before Feature Changes

- Branch: `mid-course-project`
- Existing pytest suite: `23 passed`
- Test command: `python -m pytest`
- Environment: Windows, Python 3.13.14
- Baseline result: all existing tests passed before any feature changes.
- Frontend loaded successfully using Live Server at `http://localhost:5500/frontend/index.html`.
- The frontend successfully fetched and displayed tasks from the running backend.



## Feature 1 Backend Manual Verification

- `GET /tasks?search=A` returned only task A.
- `GET /tasks?search=B` returned only task B.
- `GET /tasks?search=C` returned only task C.
- `GET /tasks?search=xxxxxxxx` returned HTTP 200 with `[]`.
- `GET /tasks?search=A&status=ToDo` returned task A.
- `GET /tasks?search=A&status=Done` returned HTTP 200 with `[]`.

Result: Search and combined filtering behaved as expected.