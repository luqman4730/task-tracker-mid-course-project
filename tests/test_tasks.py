from datetime import date, timedelta

def test_create_task_valid_returns_201_with_full_body(client):
    payload = {
        "title": "My task",
        "description": "A description",
        "status": "ToDo",
        "priority": "High",
        "assignee": "alice",
    }
    response = client.post("/tasks", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "My task"
    assert body["description"] == "A description"
    assert body["status"] == "ToDo"
    assert body["priority"] == "High"
    assert body["assignee"] == "alice"
    assert "id" in body
    assert "created_at" in body
    assert "updated_at" in body


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid title", "priority": "Urgent"})

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Valid title", "made_up": "value"})

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client, created_task):
    response = client.get("/tasks", params={"status": "InProgress"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    low_response = client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    high_response = client.post("/tasks", json={"title": "High task", "priority": "High"})
    assert low_response.status_code == 201
    assert high_response.status_code == 201

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == high_response.json()["id"]
    assert tasks[0]["priority"] == "High"


# Tests for new feature 1

def test_list_tasks_search_matches_title(client):
    matching_response = client.post(
        "/tasks",
        json={
            "title": "Monthly Report",
            "description": "Prepare finance documents",
        },
    )
    other_response = client.post(
        "/tasks",
        json={
            "title": "Team Meeting",
            "description": "Discuss project progress",
        },
    )
    assert matching_response.status_code == 201
    assert other_response.status_code == 201

    response = client.get("/tasks", params={"search": "Monthly"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == matching_response.json()["id"]


def test_list_tasks_search_matches_description(client):
    matching_response = client.post(
        "/tasks",
        json={
            "title": "Fix Login Page",
            "description": "Update frontend validation",
        },
    )
    other_response = client.post(
        "/tasks",
        json={
            "title": "Write Documentation",
            "description": "Prepare project notes",
        },
    )
    assert matching_response.status_code == 201
    assert other_response.status_code == 201

    response = client.get("/tasks", params={"search": "validation"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == matching_response.json()["id"]


def test_list_tasks_search_is_case_insensitive(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Monthly Report",
            "description": "Prepare finance documents",
        },
    )
    assert create_response.status_code == 201

    response = client.get("/tasks", params={"search": "monthly report".upper()})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == create_response.json()["id"]


def test_list_tasks_search_no_match_returns_200_and_empty_list(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Existing Task"},
    )
    assert create_response.status_code == 201

    response = client.get("/tasks", params={"search": "xxxxxxxx"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_search_combined_with_status_uses_and_logic(client):
    todo_response = client.post(
        "/tasks",
        json={
            "title": "Monthly Report",
            "status": "ToDo",
        },
    )
    in_progress_response = client.post(
        "/tasks",
        json={
            "title": "Monthly Report Draft",
            "status": "InProgress",
        },
    )
    assert todo_response.status_code == 201
    assert in_progress_response.status_code == 201

    response = client.get(
        "/tasks",
        params={
            "search": "Monthly Report",
            "status": "ToDo",
        },
    )

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == todo_response.json()["id"]
    assert tasks[0]["status"] == "ToDo"


def test_list_tasks_search_combined_with_status_and_priority(client):
    matching_response = client.post(
        "/tasks",
        json={
            "title": "Monthly Report",
            "status": "ToDo",
            "priority": "High",
        },
    )
    wrong_priority_response = client.post(
        "/tasks",
        json={
            "title": "Monthly Report",
            "status": "ToDo",
            "priority": "Low",
        },
    )
    wrong_status_response = client.post(
        "/tasks",
        json={
            "title": "Monthly Report",
            "status": "InProgress",
            "priority": "High",
        },
    )
    assert matching_response.status_code == 201
    assert wrong_priority_response.status_code == 201
    assert wrong_status_response.status_code == 201

    response = client.get(
        "/tasks",
        params={
            "search": "Monthly Report",
            "status": "ToDo",
            "priority": "High",
        },
    )

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == matching_response.json()["id"]
    assert tasks[0]["status"] == "ToDo"
    assert tasks[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")

    assert response.status_code == 200
    assert response.json() == created_task


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_patch_partial_update_keeps_other_fields(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Original title",
            "description": "Keep this description",
            "priority": "Low",
            "assignee": "bob",
        },
    )
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(f"/tasks/{task['id']}", json={"title": "Updated title"})

    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Updated title"
    assert body["description"] == "Keep this description"
    assert body["priority"] == "Low"
    assert body["assignee"] == "bob"
    assert body["status"] == "ToDo"
    assert body["id"] == task["id"]
    assert body["created_at"] == task["created_at"]


def test_patch_not_found_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.patch(f"/tasks/{missing_id}", json={"title": "Updated"})

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )

    assert response.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )

    assert response.status_code == 422


def test_patch_blank_title_returns_422(client):
    create_response = client.post("/tasks", json={"title": "Original title"})
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(f"/tasks/{task['id']}", json={"title": "   "})

    assert response.status_code == 422
    assert "title must not be blank" in response.text


def test_patch_invalid_priority_returns_422(client):
    create_response = client.post("/tasks", json={"title": "Original title"})
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(f"/tasks/{task['id']}", json={"priority": "Urgent"})

    assert response.status_code == 422
    assert "Input should be 'Low', 'Medium' or 'High'" in response.text


def test_patch_unsupported_status_returns_422(client):
    create_response = client.post("/tasks", json={"title": "Original title"})
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(f"/tasks/{task['id']}", json={"status": "Completed"})

    assert response.status_code == 422
    assert "Input should be 'ToDo', 'InProgress' or 'Done'" in response.text


def test_patch_unknown_field_returns_422(client):
    create_response = client.post("/tasks", json={"title": "Original title"})
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(f"/tasks/{task['id']}", json={"title": "Updated title", "made_up": "value"})

    assert response.status_code == 422
    assert "Extra inputs are not permitted" in response.text


def test_patch_empty_body_leaves_task_unchanged(client):
    create_response = client.post("/tasks", json={"title": "Original title", "priority": "High"})
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(f"/tasks/{task['id']}", json={})

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == task["id"]
    assert body["title"] == task["title"]
    assert body["priority"] == task["priority"]


def test_patch_done_to_inprogress_returns_200(client):
    create_response = client.post("/tasks", json={"title": "Original title"})
    assert create_response.status_code == 201
    task = create_response.json()

    first_patch = client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"})
    assert first_patch.status_code == 200

    second_patch = client.patch(f"/tasks/{task['id']}", json={"status": "Done"})
    assert second_patch.status_code == 200

    response = client.patch(f"/tasks/{task['id']}", json={"status": "InProgress"})

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    missing_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f"/tasks/{missing_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == f"Task with id {missing_id} not found"



def test_create_task_with_due_date_returns_201(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task with deadline",
            "due_date": "2026-08-15",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["due_date"] == "2026-08-15"


def test_create_task_without_due_date_returns_null(client):
    response = client.post(
        "/tasks",
        json={"title": "Task without deadline"},
    )

    assert response.status_code == 201
    assert response.json()["due_date"] is None


def test_create_task_invalid_due_date_returns_422(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Task with invalid deadline",
            "due_date": "15/08/2026",
        },
    )

    assert response.status_code == 422


def test_patch_due_date_updates_existing_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Original task"},
    )
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"due_date": "2026-09-01"},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == "2026-09-01"


def test_patch_due_date_to_null_removes_due_date(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Task with deadline",
            "due_date": "2026-09-01",
        },
    )
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"due_date": None},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] is None





def test_list_tasks_overdue_returns_only_past_unfinished_tasks(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    overdue_response = client.post(
        "/tasks",
        json={
            "title": "Overdue task",
            "due_date": yesterday,
            "status": "ToDo",
        },
    )
    future_response = client.post(
        "/tasks",
        json={
            "title": "Future task",
            "due_date": tomorrow,
            "status": "ToDo",
        },
    )
    no_due_date_response = client.post(
        "/tasks",
        json={
            "title": "No due date task",
            "status": "ToDo",
        },
    )

    assert overdue_response.status_code == 201
    assert future_response.status_code == 201
    assert no_due_date_response.status_code == 201

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == overdue_response.json()["id"]


def test_list_tasks_due_today_is_not_overdue(client):
    today = date.today().isoformat()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Due today",
            "due_date": today,
            "status": "ToDo",
        },
    )
    assert create_response.status_code == 201

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_done_task_is_not_overdue(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    create_response = client.post(
        "/tasks",
        json={
            "title": "Completed overdue task",
            "due_date": yesterday,
            "status": "Done",
        },
    )
    assert create_response.status_code == 201

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_overdue_false_does_not_filter_tasks(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()

    overdue_response = client.post(
        "/tasks",
        json={"title": "Overdue task", "due_date": yesterday},
    )
    future_response = client.post(
        "/tasks",
        json={"title": "Future task", "due_date": tomorrow},
    )
    assert overdue_response.status_code == 201
    assert future_response.status_code == 201

    response = client.get("/tasks", params={"overdue": "false"})

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_list_tasks_overdue_combines_with_priority(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()

    high_response = client.post(
        "/tasks",
        json={
            "title": "High overdue task",
            "due_date": yesterday,
            "priority": "High",
        },
    )
    low_response = client.post(
        "/tasks",
        json={
            "title": "Low overdue task",
            "due_date": yesterday,
            "priority": "Low",
        },
    )
    assert high_response.status_code == 201
    assert low_response.status_code == 201

    response = client.get(
        "/tasks",
        params={
            "overdue": "true",
            "priority": "High",
        },
    )

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == high_response.json()["id"]

    
def test_patch_null_title_returns_422(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Original title"},
    )

    assert create_response.status_code == 201

    task = create_response.json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"title": None},
    )

    assert response.status_code == 422
    assert "title must not be null" in response.text