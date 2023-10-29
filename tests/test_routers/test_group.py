import pytest

# TEST UNAUTHORIZED CLIENT


def test_unauthorized_client_get_all_groups(client, test_groups):
    res = client.get("/groups/")
    assert res.status_code == 401


def test_unauthorized_client_get_group_by_id(client, session, test_groups):
    res = client.get(f"/groups/{test_groups[0].id}")
    assert res.status_code == 401


def test_unauthorized_client_create_group(client, session):
    res = client.post(
        "/groups",
        json={
            "description": "Description for the new group",
            "visibility": True,
            "admins": [],
            "members": [],
        },
    )
    assert res.status_code == 401


def test_unauthorized_client_update_group(client, session, test_groups):
    res = client.patch(
        f"/groups/update/{test_groups[0].id}",
        json={"description": "Updated description"},
    )
    assert res.status_code == 401


def test_unauthorized_client_delete_group(client, session, test_groups):
    res = client.delete(f"/groups/delete/{test_groups[0].id}")
    assert res.status_code == 401


# TEST AUTHORIZED CLIENT


def test_get_all_groups(authorize_client, test_groups):
    res = authorize_client.get("/groups")
    assert len(res.json()) == 1
    assert res.status_code == 200


def test_get_group_by_id(authorize_client, test_groups):
    res = authorize_client.get(f"/groups/{test_groups[0].id}")
    assert res.status_code == 200


@pytest.mark.parametrize(
    "name, description, admins, members, visibility",
    [
        ("New group1", "This is new group1", [], [], True),
        ("New group2", "This is new group2", [{"username": "atoe"}], [], False),
        ("New group3", "This is new group3", [], [{"username": "atoe"}], True),
        (
            "New group4",
            "This is new group4",
            [{"username": "atoe"}],
            [{"username": "atoe"}],
            True,
        ),
    ],
)
def test_create_group(
    authorize_client,
    test_user,
    test_user2,
    name,
    description,
    admins,
    members,
    visibility,
):
    res = authorize_client.post(
        "/groups/",
        json={
            "name": name,
            "description": description,
            "admins": admins,
            "members": members,
            "visibility": visibility,
        },
    )
    print(res.json())
    assert res.status_code == 201
    assert res.json()["name"] == name
    assert res.json()["description"] == description
    assert res.json()["admins"] == admins
    assert res.json()["members"] == members
    assert res.json()["visibility"] == visibility
    assert res.json()["owner"]["username"] == test_user["username"]


def test_update_group(authorize_client, session, test_groups):
    res = authorize_client.patch(
        f"/groups/update/{test_groups[0].id}",
        json={"description": "Updated description"},
    )
    assert res.status_code == 200
    assert res.json()["description"] == "Updated description"


def test_delete_group(authorize_client, session, test_groups):
    res = authorize_client.delete(f"/groups/delete/{test_groups[0].id}")
    assert res.status_code == 204


# AUTHORIZED CLIENT BUT IS NOT AN OWNER OF THE GROUP


def test_update_group_by_no_owner_user(authorize_client, session, test_groups):
    res = authorize_client.patch(
        f"/groups/update/{test_groups[1].id}",
        json={"description": "Updated description"},
    )
    assert res.status_code == 404


def test_delete_group_by_no_owner_user(authorize_client, session, test_groups):
    res = authorize_client.delete(f"/groups/delete/{test_groups[1].id}")
    assert res.status_code == 404
