import pytest

# TEST UNAUTHORIZED CLIENT


def test_unauthorized_client_get_all_tasks(client, session, test_tasks):
    res = client.get("/tasks")
    assert res.status_code == 401


def test_unauthorized_client_get_task_by_id(client, session, test_tasks):
    res = client.get(f"/tasks/{test_tasks[0].id}")
    assert res.status_code == 401


def test_unauthorized_client_create_task(client, session):
    res = client.post(
        "/tasks",
        json={
            "title": "New task",
            "description": "Description for the new task",
            "status": "To Do",
            "priority": "High",
        },
    )
    assert res.status_code == 401


def test_unauthorized_client_update_task(client, session, test_tasks):
    res = client.patch(
        f"/tasks/update/{test_tasks[0].id}", json={"description": "Updated description"}
    )
    assert res.status_code == 401


def test_unauthorized_client_delete_task(client, session, test_tasks):
    res = client.delete(f"/tasks/delete/{test_tasks[0].id}")
    assert res.status_code == 401


# TEST AUTHORIZED CLIENT


def test_get_all_tasks_empty(authorize_client):
    res = authorize_client.get("/tasks")
    # assert res.json() == [test_tasks]
    assert res.status_code == 200


def test_get_all_tasks(authorize_client, test_tasks):
    res = authorize_client.get("/tasks")
    # assert res.json() == [test_tasks]
    assert res.status_code == 200


def test_get_task_by_id(authorize_client, test_tasks):
    res = authorize_client.get(f"/tasks/{test_tasks[0].id}")
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, description, status, priority",
    [
        ("New task1", "Description of the new task1", "To Do", "High"),
        ("New task2", "", "Review", "Low"),
    ],
)
def test_create_task(authorize_client, test_user, title, description, status, priority):
    res = authorize_client.post(
        "/tasks/",
        json={
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
        },
    )
    assert res.status_code == 201
    assert res.json()["title"] == title
    assert res.json()["description"] == description
    assert res.json()["status"] == status
    assert res.json()["priority"] == priority
    assert res.json()["user"]["id"] == test_user["id"]


def test_update_task(authorize_client, session, test_tasks):
    res = authorize_client.patch(
        f"/tasks/update/{test_tasks[0].id}", json={"description": "Updated description"}
    )
    assert res.status_code == 200
    assert res.json()["description"] == "Updated description"


def test_delete_task(authorize_client, session, test_tasks):
    res = authorize_client.delete(f"/tasks/delete/{test_tasks[0].id}")
    assert res.status_code == 204


# AUTHORIZED CLIENT BUT IS NOT AN OWNER OF THE TASK


def test_update_task_by_no_owner_user(authorize_client, session, test_tasks):
    res = authorize_client.patch(
        f"/tasks/update/{test_tasks[1].id}", json={"description": "Updated description"}
    )
    assert res.status_code == 404


def test_delete_task_by_no_owner_user(authorize_client, session, test_tasks):
    res = authorize_client.delete(f"/tasks/delete/{test_tasks[1].id}")
    assert res.status_code == 404
