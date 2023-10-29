from os import environ
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from auth.oauth2 import create_access_token
from crud.task import crud_task
from crud.group import crud_group
from schemas.task import TaskCreate
from schemas.group import GroupCreate
from models.task import DbTask
from models.group import DbGroup
from typing import List
from sqlalchemy.orm import Session
from schemas.user import UserBase
from typing import Generator, Any

environ["env_state"] = "test"
from database.setup import get_db, Base, get_engine, get_session  # noqa: E402
from main import get_app  # noqa: E402


@pytest.fixture()
def app() -> FastAPI:
    return get_app()


@pytest.fixture()
def session() -> Generator[Session, Any, None]:
    engine = get_engine()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = get_session()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(app, session) -> Generator[TestClient, Any, None]:
    yield TestClient(app)


@pytest.fixture()
def test_user(client: TestClient):
    data = {
        "name": "john",
        "surname": "doe",
        "username": "jdoe",
        "email": "jdoe@mail.com",
        "password": "pass1234!",
        "confirm_password": "pass1234!",
    }
    res = client.post("/user/", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = data["password"]
    return new_user


@pytest.fixture()
def test_user2(client: TestClient):
    data = {
        "name": "ann",
        "surname": "toe",
        "username": "atoe",
        "email": "atoe@mail.com",
        "password": "pass1234!",
        "confirm_password": "pass1234!",
    }
    res = client.post("/user/", json=data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = data["password"]
    return new_user


@pytest.fixture()
def token(test_user):
    return create_access_token({"sub": test_user["username"]})


@pytest.fixture()
def authorize_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture()
def test_tasks(test_user, test_user2, session) -> List[DbTask]:
    data = [
        {
            "title": "first task",
            "description": "Description of the first task",
            "status": "To Do",
            "priority": "Low",
        },
        {
            "title": "second task",
            "description": "Description of the second task",
            "status": "In Progress",
            "priority": "High",
        },
    ]
    db_tasks = []
    for element, user in zip(data, [test_user, test_user2]):
        print(user["name"])
        db_tasks.append(
            crud_task.create(session, request=TaskCreate(**element), user_id=user["id"])
        )
    session.add_all(db_tasks)
    session.commit()
    return db_tasks


@pytest.fixture()
def test_groups(test_user, test_user2, session):
    data = [
        {
            "name": "group1",
            "description": "Description of the group1",
            "admins": [],
            "members": [],
            "visibility": True,
        },
        {
            "name": "group2",
            "description": "Description of the group2",
            "admins": [],
            "members": [],
            "visibility": True,
        },
    ]
    db_groups = []
    for element, user in zip(data, [test_user, test_user2]):
        db_groups.append(
            crud_group.create(session, GroupCreate(**element), user_id=user["id"])
        )
    session.add_all(db_groups)
    session.commit()
    groups = session.query(DbGroup).all()

    return groups
