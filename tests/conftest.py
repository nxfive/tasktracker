import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database.setup import get_db, Base
from auth.oauth2 import create_access_token
from crud.task import crud_task
from schemas.task import TaskCreate
from models.task import DbTask
from typing import List

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@127.0.0.1:5432/test"

engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True)

TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def test_user(client):
    data = {
        "name": "john",
        "surname": "doe",
        "username": "jdoe",
        "email": "jdoe@mail.com",
        "password": "pass1234!",
        "confirm_password": "pass1234!"
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
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture()
def test_tasks(test_user, session) -> List[DbTask]:
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
        }
    ]

    db_tasks = list(map(
        lambda tasks: crud_task.create_task(session, request=TaskCreate(**tasks), user_id=test_user["id"]),
        data
    ))
    session.add_all(db_tasks)
    session.commit()
    return db_tasks
