# Personal AI Coding Playbook

## 1. When I reach for AI first

* I reach for AI early when I need to understand an unfamiliar concept, tool, or codebase area. This helped me with Python, FastAPI, testing, Docker, CI, and repository-level workflows during the course.
* I use AI for planning and comparing approaches before changing code. Architecture and context-engineering exercises showed me that comparing options first makes trade-offs clearer.
* I also use AI for a first draft or scaffold that I can inspect and improve, especially for tests, documentation, and infrastructure configuration.

## 2. When I do not reach for AI first

* I do not ask AI to make decisions that are supposed to reflect my own judgment. AI can organize the thinking, but I make the final choice.
* I do not ask for a fix before I understand the actual failure. I prefer to run the test, read the error, and then give AI that evidence.
* I do not give an agent broad write access just because it is convenient. Read-only review is often enough to get useful analysis first.

## 3. My non-negotiables

* I will not paste credentials, authentication secrets, real user records, private assets, production URLs, or other sensitive project data into an AI tool.
* I keep responsibility for the final artifact. AI-generated code, tests, documentation, or configuration are not final until I review and verify them.
* I prefer evidence over confidence. Repository claims should be grounded in actual files, tests, logs, diffs, or runtime behavior.

## 4. My review rules

* I run the relevant tests instead of assuming generated code works. Deliberately breaking validation and seeing a test fail was one of the clearest lessons from the course.
* For repository reviews, I want AI to inspect the relevant files before making conclusions. Too little context can miss details, while uncontrolled broad discovery can make scope harder to manage.
* I review generated infrastructure and configuration carefully. Walking through the Dockerfile line by line helped me understand what I was accepting instead of treating it as a black box.

## 5. What I am still figuring out

* I am still learning how much context is enough for each task. Minimal, structured, and targeted context can all be useful depending on whether I need speed, coverage, or stronger evidence.
* I am still deciding which AI interface fits different kinds of work best: conversational explanation, repository review, planning, or longer-running agent tasks.
* I am still learning where the best boundary is between using AI to save time and doing enough of the work myself to make sure I understand it.

## Decision Card

* **New feature:** AI-assisted planning first, then a coding assistant once scope and acceptance criteria are clear.
* **Code review:** Repository-aware agent in read-only mode first.
* **Debugging:** Failing test, error output, and relevant code first, then AI with that evidence.
* **Infrastructure:** AI for a draft and explanation, followed by manual review and verification.
* **Never paste:** Credentials, authentication secrets, real user records, or private project data.
* **My one rule:** I do not accept AI output until I understand enough of it to verify and own the final result.

## 30-Day Re-read

I will re-read this playbook in 30 days and check which rules I am actually following, which are helping, and which need to change based on real project use.
