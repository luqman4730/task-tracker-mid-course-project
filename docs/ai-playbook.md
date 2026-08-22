# Personal AI Coding Playbook

## 1. When I reach for AI first

* I reach for AI early when I need to understand an unfamiliar concept, tool, or codebase area. This helped me throughout the course when I was working with things that were new to me, especially Python, FastAPI, testing, Docker, CI, and repository-level workflows.
* I use AI early for planning and comparing approaches before I start changing code. In the architecture and context-engineering work, comparing alternatives first helped me see trade-offs before committing to one direction.
* I also use AI when I need a first draft or scaffold that I can inspect and improve. During the course, I used this approach for things like tests, documentation, and Docker configuration, then reviewed and adjusted the result before keeping it.

## 2. When I do not reach for AI

* I do not ask AI to decide something for me when the decision is supposed to reflect my own judgment. The governance work, context strategy comparison, and this playbook all showed me that AI can help organize the thinking, but I still need to make the final choice.
* I do not ask for a fix before I understand the actual failure. During testing, running the test and seeing the real error was more useful than describing the problem from memory.
* I do not give an agent broad write access just because it is convenient. The Module 5 read-only reviews showed me that I can get useful analysis without immediately allowing changes.

## 3. My non-negotiables

* I will not paste credentials, authentication secrets, real user records, private assets, production URLs, or other sensitive project data into an AI tool. The governance work in Module 5 made me explicitly review what I had shared with AI and separate safe project context from information that should never be shared.
* I keep responsibility for the final artifact. During the course, I repeatedly reviewed AI-generated code, tests, and documentation before accepting or changing them, so I do not treat generated output as final by default.
* I prefer evidence over confidence. The Module 5 repository reviews and context-engineering exercise showed me that conclusions are more useful when they are grounded in actual files, tests, logs, or other project evidence.

## 4. My review rules

* I run the relevant tests instead of assuming generated code works. One of the clearest lessons from the course was deliberately breaking validation and seeing the test fail, then restoring the code and seeing it pass.
* For repository review, I want AI to inspect the relevant files before making conclusions. The context-engineering exercise showed me that too little context can miss important details, while uncontrolled broad discovery can make scope harder to manage.
* I review generated infrastructure and configuration carefully, even when it looks simple. Walking through the Dockerfile line by line helped me understand what I was actually accepting instead of treating generated configuration as a black box.

## 5. What I am still figuring out

* I am still figuring out how much context is enough for each task. Module 5.5 showed me that minimal, structured, and targeted context can all be useful, but the right choice depends on whether I need speed, coverage, or deeper evidence.
* I am still deciding which AI interface I prefer for different kinds of work. Some tasks benefit from conversational explanation, while repository planning, review, and long-running work benefit from an agent that can inspect the project directly.
* I am still learning where the best boundary is between using AI to save time and doing enough of the work myself to make sure I actually understand it.

## Decision Card

* For a new feature I reach for: AI-assisted planning first, then an agent or coding assistant once the scope and acceptance criteria are clear.
* For a code review I reach for: a repository-aware agent in read-only mode first.
* For debugging I reach for: the failing test, error output, and relevant code first, then AI with that evidence.
* For infrastructure I reach for: AI for a draft and explanation, followed by manual review and verification.
* I will never paste credentials, authentication secrets, real user records, or private project data into an AI tool.
* My one rule is: I do not accept AI output until I understand enough of it to verify and own the final result.

## 30-Day Re-read

I will re-read this playbook in 30 days and check whether I am actually following these rules, which rules are helping me, and which ones need to change based on how I am using AI in real projects.
