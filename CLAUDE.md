# CLAUDE.md

This file provides guidance to Claude Code for the Module 4 Task Tracker project.

## 1. Tech stack

- Python 3.11
- FastAPI
- Pydantic v2
- Uvicorn
- pytest
- pytest
- httpx
- Vanilla JavaScript frontend in frontend/index.html if present

## 2. Run command

```bash
uvicorn app.main:app --reload --port 8000
```

## 3. Test command

```bash
python -m pytest -v
```

## 4. Architecture summary

- Backend: app/main.py defines the FastAPI routes, app/models.py contains the Pydantic models, app/storage.py holds the in-memory task store, and app/business_rules.py contains the status-transition validation logic.
- Frontend: frontend/index.html contains the single-page HTML/CSS/JavaScript UI.
- Tests: tests/ contains pytest coverage for API behavior and task rules.
- Task rules: status transition rules live in app/business_rules.py and are enforced in app/main.py for PATCH updates.

## 5. Business rules

- Task status values implemented in app/models.py: ToDo, InProgress, Done.
- Allowed transitions implemented in app/business_rules.py: ToDo -> InProgress, InProgress -> Done, Done -> InProgress.
- All other transitions are rejected with 422 Unprocessable Entity.
- The transition check runs before the storage update, so missing tasks return 404 first.

## 6. UI states and CORS notes

- The frontend is a simple single-page vanilla JS app in frontend/index.html.
- The repository does not define a separate formal UI state machine; UI behavior is handled directly in the browser script.
- CORS is configured in app/main.py for localhost:5500, 127.0.0.1:8000, localhost:5173, and null.

## 7. Do-not rules

- Do not add authentication, user accounts, or login flows.
- Do not introduce a database or persistence layer unless explicitly asked.
- Do not add deployment steps or production infrastructure without asking.
- Do not make major UI redesigns or rewrite the frontend structure without asking.
