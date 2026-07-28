# Task Tracker

A small full-stack Task Tracker learning project built with FastAPI and a plain HTML, CSS, and JavaScript frontend.

The application supports creating, viewing, updating, deleting, searching, and filtering tasks. The mid-course project adds:

- Search with combined status and priority filters
- Optional due dates and overdue filtering

## Requirements

- Python 3.10 or later
- A modern web browser

## Project Setup

Open a terminal in the project folder.

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
venv\Scripts\activate.bat
```

macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the Backend

From the project root, run:

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://localhost:8000
```

FastAPI interactive API documentation is available at:

```text
http://localhost:8000/docs
```

## Open the Frontend

Keep the backend running.

### Option 1: VS Code Live Server

Open `frontend/index.html` with the Live Server extension.

The frontend will normally be available at:

```text
http://localhost:5500/frontend/index.html
```

### Option 2: Python HTTP Server

From the project root, open a second terminal and run:

```bash
python -m http.server 5500
```

Then open:

```text
http://localhost:5500/frontend/index.html
```

## Run the Tests

Activate the virtual environment, then run:

```bash
python -m pytest
```

The final project test suite contains all existing tests plus the new tests for the two selected features.

Final verified result:

```text
39 passed
```

## Mid-Course Documentation

The required documentation is located in:

```text
docs/midcourse/
```

It includes:

- `user-stories.md`
- `mini-adr.md`
- `verification.md`
- `prompt-log.md`
- `reflection.md`

## Selected Feature Behavior

### Search and Combined Filters

- Search matches partial text in task titles and descriptions.
- Search is case-insensitive.
- Search, status, and priority filters can be combined.
- Active filters use AND logic.

### Due Dates and Overdue Filtering

- Due dates are optional.
- Due dates use the `YYYY-MM-DD` format.
- A task is overdue when its due date is before today and its status is not `Done`.
- A task due today is not overdue.
- Overdue filtering can be combined with search, status, and priority filters.

## Notes

- The project uses in-memory storage with JSON file persistence.
- Authentication, user accounts, notifications, pagination, and production deployment are outside the project scope.
- Do not commit virtual environments, caches, credentials, secrets, or private data.
