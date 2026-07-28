# Mid-Course Project User Stories

## Selected Features

1. Search + Combined Filters
2. Due Dates + Overdue Filter

---

# Feature 1: Search + Combined Filters

| ID | Story | Acceptance Criteria | Notes / Assumptions |
|----|-------|---------------------|---------------------|
| US1 | As a team member, I want to search tasks by keyword so that I can quickly find relevant tasks. | • Search matches task title and description.<br>• Search is case-insensitive.<br>• Empty search shows all tasks. | Search is limited to title and description. |
| US2 | As a team member, I want to filter tasks by status so that I can focus on tasks in a specific workflow stage. | • Selecting a status shows only matching tasks.<br>• Clearing the filter restores all tasks. | Existing status values are reused. |
| US3 | As a team member, I want to filter tasks by priority so that I can focus on the most important work. | • Selecting a priority shows only matching tasks.<br>• Clearing the filter restores all tasks. | Existing priority values are reused. |
| US4 | As a team member, I want to combine search, status, and priority filters so that I can narrow my results efficiently. | • Filters can be combined.<br>• A task must satisfy all selected filters.<br>• No matches return an empty list with HTTP 200. | Combined filters use AND logic. |

### AI Assumption Corrected

**Original AI assumption**

Search should also include the assignee field.

**Correction**

Search was limited to **title** and **description** to keep the feature aligned with the project scope and minimize implementation complexity.

---

# Feature 2: Due Dates + Overdue Filter

| ID | Story | Acceptance Criteria | Notes / Assumptions |
|----|-------|---------------------|---------------------|
| US5 | As a team member, I want to assign an optional due date when creating a task so that I can track deadlines. | • Due date is optional.<br>• Valid dates are accepted.<br>• Invalid dates return HTTP 422. | Date only (YYYY-MM-DD). |
| US6 | As a team member, I want to edit or remove a due date so that task deadlines remain accurate. | • Existing due dates can be changed.<br>• Due dates can be removed.<br>• Changes are saved successfully. | Removing a due date sets it to null. |
| US7 | As a team member, I want overdue tasks to be clearly identified so that I can prioritize late work. | • Tasks before today are overdue.<br>• Tasks due today are not overdue.<br>• Completed tasks are never overdue. | Overdue is calculated by the backend. |
| US8 | As a team member, I want to filter overdue tasks so that I can review unfinished late work. | • Overdue filter returns only overdue tasks.<br>• Turning off the filter restores all tasks.<br>• Tasks without due dates are excluded. | Uses the backend overdue rule. |

### AI Assumption Corrected

**Original AI assumption**

Tasks due today should be considered overdue.

**Correction**

A task is overdue **only when its due date is before today and its status is not `Done`**.