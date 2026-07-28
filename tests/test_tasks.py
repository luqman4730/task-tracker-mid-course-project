def test_create_task_valid_returns_201_with_full_body(client):
    payload = {
        "title": "My task",
        "description": "A description",
        "status": "ToDo",
        "priority": "High",
        "assignee": "alice",
    }
    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
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
