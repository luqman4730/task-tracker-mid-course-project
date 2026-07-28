# Reflection

## AI Usage Reflection

Throughout this project, I used AI as a development assistant rather than a code generator.

At the beginning of the implementation, AI helped me understand the existing Task Tracker project before adding new functionality. Instead of immediately writing code, I first used AI to inspect the current architecture, existing endpoints, data models, frontend structure, and automated tests. This helped me understand where each new feature should be integrated while preserving the existing design.

For Feature 1 (Search and Combined Filters), AI assisted in generating user stories, suggesting a minimal backend design, and proposing automated tests. I reviewed every suggestion before implementation and modified several ideas to better match the project requirements. For example, I kept the search limited to the task title and description, combined filters using AND logic, and intentionally rejected more advanced features such as pagination, saved searches, and separate search endpoints because they were outside the project scope.

For Feature 2 (Due Dates and Overdue Filtering), AI helped design the data model, backend behavior, frontend changes, and testing strategy. Some suggestions were accepted directly, while others were refined before implementation. I decided to store only an optional `due_date` field and calculate whether a task is overdue dynamically instead of storing an `is_overdue` property. This simplified the implementation and reduced the possibility of inconsistent data.

AI was also useful during debugging and testing. It helped identify edge cases, suggest additional pytest tests, explain validation errors, and review unexpected behavior. One example was correcting the frontend update request so that the task status is only included in the PATCH request when it has actually changed, preventing unnecessary validation errors.

The most valuable aspect of using AI was the ability to discuss implementation decisions before writing code. Rather than copying generated code directly, I reviewed each suggestion, compared it with the project requirements, tested the implementation, and made changes where necessary. This approach helped me better understand both the project architecture and the reasoning behind each design decision.

Overall, AI significantly improved my productivity by reducing the time required for planning, debugging, testing, and documentation while still requiring careful review and validation of every generated suggestion. The experience reinforced that AI is most effective when used as a collaborative development assistant rather than as a replacement for understanding the code.