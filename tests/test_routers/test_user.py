import pytest


# TEST UNAUTHORIZED CLIENT


def test_unauthorized_client_get_all_users(client, session):
    res = client.get("/users/")
    assert res.status_code == 401


def test_unauthorized_client_get_user_by_id(client, session, test_user):
    res = client.get("/users/1")
    assert res.status_code == 401


@pytest.mark.parametrize(
    "name, surname, username, email, password, confirm_password",
    [
        (
            "John",
            "Drummond",
            "jdrummond",
            "jdrummondmail.com",
            "Pass1234!",
            "Pass1234!",
        ),  # incorrect mail
        ("Anna", "Doe", "", "adoe@mail.com", "Pass1234!", "Pass1234!"),  # no username
        ("Tom", "", "tom", "tom@mail.com", "Pass1234!", "Pass1234!"),  # no surname
        (
            "",
            "Johnes",
            "jjohnes",
            "jjohnes@mail.com",
            "Pass1234!",
            "Pass1234!",
        ),  # no name
        (
            "Kate",
            "Wind",
            "kwind",
            "kwind@mail.com",
            "12Pass34!",
            "Pass1234!",
        ),  # not the same password
    ],
)
def test_unauthorized_client_create_user_with_invalid_input(
    client, session, name, surname, username, email, password, confirm_password
):
    res = client.post(
        "/users/",
        json={
            "name": name,
            "surname": surname,
            "username": username,
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
        },
    )
    assert res.status_code == 422


def test_unauthorized_client_create_user(client, session):
    res = client.post(
        "/users/",
        json={
            "name": "William",
            "surname": "Smith",
            "username": "wsmith",
            "email": "wsmith@mail.com",
            "password": "pass1234!",
            "confirm_password": "pass1234!",
        },
    )
    assert res.status_code == 201


def test_unauthorized_client_update_group(client, session, test_user):
    res = client.patch(
        f"/users/update/1",
        json={"email": "updated@mail.com"},
    )
    assert res.status_code == 401


def test_unauthorized_client_delete_group(client, session, test_user):
    res = client.delete(f"/users/delete/1")
    assert res.status_code == 401


# TEST AUTHORIZED CLIENT


def test_get_all_users(authorize_client, test_user2):
    res = authorize_client.get("/users")
    assert len(res.json()) == 2
    assert res.status_code == 200


def test_get_user_by_id(authorize_client, test_user2):
    res = authorize_client.get(f"/users/2")
    assert res.status_code == 200


def test_create_user(
    authorize_client,
):
    res = authorize_client.post(
        "/users/",
        json={
            "name": "Sophia",
            "surname": "Brown",
            "username": "sbrown",
            "email": "sbrown@mail.com",
            "password": "Pass1234!",
            "confirm_password": "Pass1234!",
        },
    )
    print(res.json())
    assert res.status_code == 201


def test_update_user(authorize_client, session, test_user2):
    res = authorize_client.patch(
        f"/users/update/1",
        json={"email": "updated@mail.com"},
    )
    assert res.status_code == 200
    assert res.json()["email"] == "updated@mail.com"


def test_delete_user(authorize_client, session, test_user2):
    res = authorize_client.delete(f"/users/delete/1")
    assert res.status_code == 204


# AUTHORIZED CLIENT BUT IS NOT A TESTED USER


def test_update_other_user(authorize_client, session, test_user2):
    res = authorize_client.patch(
        f"/users/update/{test_user2['id']}",
        json={"email": "updated@mail.com"},
    )
    assert res.status_code == 404


def test_delete_other_user(authorize_client, session, test_user2):
    res = authorize_client.delete(f"/users/delete/{test_user2['id']}")
    assert res.status_code == 404
