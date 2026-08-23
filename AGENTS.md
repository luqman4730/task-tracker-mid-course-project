# AGENTS.md

This guidance applies to Module 5 governance and review work in the Task Tracker repository unless newer user instructions override it.

## Project Summary

Task Tracker is a small learning project with a FastAPI backend and a single-page vanilla HTML/CSS/JavaScript frontend. The API exposes task CRUD endpoints, filtering, health checks, and status-transition validation. Task data is stored in an in-memory dictionary in `app/storage.py`; no database or durable persistence is confirmed in the code.

Use repository claims only when they are grounded in inspected files such as `README.md`, `app/main.py`, `app/models.py`, `app/storage.py`, `app/business_rules.py`, `frontend/index.html`, and `tests/`.

## Tech Stack

- Python 3.11, confirmed by `README.md`, `Dockerfile`, and `.github/workflows/ci.yml`.
- FastAPI, Uvicorn, Pydantic v2, pytest, and httpx, confirmed by `requirements.txt`.
- Vanilla frontend in `frontend/index.html`.
- Docker support is present through `Dockerfile`.

## Supported Commands

Run from the repository root.

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Run the static frontend:

```bash
python -m http.server 5500
```

Then open `http://localhost:5500/frontend/index.html`. The frontend uses a hard-coded API base of `http://localhost:8000`.

Run tests:

```bash
python -m pytest -v
```

If Docker is available, build and run the Docker image:

```bash
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
```

Not confirmed: lint, format, type-check, coverage, database migration, frontend build, or package-manager commands. Do not invent these commands.

## Visible Business Rules

- Task statuses are `ToDo`, `InProgress`, and `Done`, defined in `app/models.py`.
- Task priorities are `Low`, `Medium`, and `High`, defined in `app/models.py`.
- Create defaults: `status=ToDo`, `priority=Medium`, `description=""`, `assignee=None`, and `due_date=None`, visible in `app/models.py` and `app/storage.py`.
- Task IDs are generated with UUID4 in `app/storage.py`.
- `created_at` and `updated_at` are stamped in UTC in `app/storage.py`.
- Task data is process-local in memory and is lost when the process stops.
- Valid status transitions are defined in `app/business_rules.py`: `ToDo -> InProgress`, `InProgress -> Done`, and `Done -> InProgress`.
- All other status transitions, including same-status updates, are rejected with HTTP 422.
- Missing tasks return HTTP 404.
- Create and update payloads forbid unknown fields through Pydantic `extra="forbid"`.
- `title` is required on create, stripped of surrounding whitespace, must not be blank, and must be at most 200 characters.
- On update, `title` is optional, but an explicit `null`, blank string, or value over 200 characters is rejected.
- `GET /tasks` supports optional `status`, `priority`, `search`, and `overdue` filters. Filters combine with AND logic.
- Search is case-insensitive and matches title or description.
- `overdue=true` returns tasks with a due date before today whose status is not `Done`; `overdue=false` applies no overdue filter.
- Empty PATCH bodies return the task unchanged.
- Tests reset the in-memory store around each test through `tests/conftest.py`.

## Module 5 Guardrails

- Module 5 is for grading, review, governance, and documentation. Do not treat it as feature-building work.
- Prefer read-only analysis first.
- Use docs-first workflows. Edit `docs/` by default unless the user explicitly approves another path.
- Non-`docs/` edits require explicit user approval, except when the user has specifically requested an edit to a named non-`docs/` file.
- Do not modify `app/` unless the user approves one specific minimal fix.
- Keep one bounded task per thread.
- Cite the actual files inspected when making repo claims.
- If a command, rule, behavior, or file is not visible, mark it as `not confirmed`.
- Do not invent findings, test results, architecture, or requirements.

## Security And Governance

- Do not paste, expose, or summarize secret values from `.env`, shell environment variables, credentials, keys, tokens, local config, or private files.
- `.env` is ignored by `.gitignore`; `.env.example` is the tracked template.
- Do not run destructive commands such as recursive delete, `git reset --hard`, or force checkout unless the user explicitly asks and approves.
- Do not install dependencies, change dependency pins, contact external services, or use networked tooling unless the task requires it and the user approves when needed.
- Preserve user changes. Do not revert unrelated work.
- Prefer narrow, evidence-backed reviews over broad rewrites.
- When uncertain, say what is not confirmed and identify the file or command that would verify it.
