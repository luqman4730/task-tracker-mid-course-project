# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes

## AI code review mini-log

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| The documented local API command should use `python -m uvicorn` instead of the direct `uvicorn` executable because the current environment has a stale virtual-environment path. | Useful | The direct `uvicorn` command failed during the baseline check, while `python -m uvicorn app.main:app --reload --port 8000` started the API successfully. | Updated `README.md` and `AGENTS.md` to use the verified command. |
| The README claim that the full test suite reports 40 passing tests should be verified before final submission. | Useful | This is a measurable release claim and should not be accepted without running the full suite. | Ran `python -m pytest`; result was `40 passed in 0.31s`. The README claim was kept. |
| The README Docker section may need correction because the image might not run as a non-root user. | Wrong | The Dockerfile explicitly sets `USER app`, and a runtime check confirmed it. | Ran `docker run --rm task-tracker-final whoami`; output was `app`. No README change was needed. |

## AI security mini-review

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Unbounded text inputs can grow the in-memory store without a clear size limit. | `app/models.py`, `app/storage.py`, `app/main.py` | Valid | Fields such as description and assignee are not meaningfully bounded, and task data is stored in process memory. | Document as a known limitation; do not add a new product feature during the final project. |
| An explicit `description: null` update can leave an unexpected null value that may later break search behavior. | `app/models.py`, `app/main.py`, `app/storage.py` | Valid | The update path can store a value that conflicts with later code expecting description to behave as a string. | Record as a known issue; do not change `app/` unless a minimal fix is explicitly justified. |
| The API has no authentication or authorization. | `app/main.py`, `README.md` | Valid | All task endpoints are open. This is a real production security concern, but authentication is intentionally outside the course scope. | Keep documented as an intentional limitation; do not add authentication during the final project. |

## Manual security check

I manually checked that the local `.env` file is not tracked by Git and that the repository working tree was clean before starting the final-project work. I also checked `.dockerignore` and confirmed that `.env`, `.env.*`, `*.pem`, and `*.key` are excluded from the Docker build context. This matters because the final repository and container image should not expose local secrets, credentials, or environment values.

## One AI output I rejected or corrected

AI initially accepted the README command `uvicorn app.main:app --reload --port 8000` as the local API run command. During the baseline check, that direct command failed because the existing virtual environment referenced an old Python path. I did not keep the suggestion as-is. I verified that `python -m uvicorn app.main:app --reload --port 8000` worked, then updated both `README.md` and `AGENTS.md` to use the verified command.

## Three AI usage rules

1. Never paste: credentials, secret values, tokens, `.env` contents, production logs, or real personal/customer data into AI tools.
2. Always verify: AI-generated commands, code changes, documentation claims, and security findings against the actual repository, tests, runtime behavior, or other direct evidence before accepting them.
3. Record AI contributions by: noting what AI suggested or reviewed, the evidence used to check it, and whether I accepted, corrected, downgraded, or rejected the output.

## Ownership statement

I am comfortable submitting this repository as my own work because I reviewed the final changes and verified the important release claims myself. I ran the application, tested the frontend flow, ran the full pytest suite, built and ran the Docker image, and checked the `/health` endpoint and container user. I also graded AI review and security comments instead of accepting them automatically, and I corrected AI-supported documentation when the runtime evidence disagreed with it. I can explain the commands, configuration choices, documented limitations, and changes included in this final branch.
