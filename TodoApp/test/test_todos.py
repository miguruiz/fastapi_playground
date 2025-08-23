from http.client import responses

from httpx import request
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Base, Todos
from ..main import app
from fastapi import status
from ..routers.todos import get_db, get_current_user
from fastapi.testclient import TestClient
import pytest

SQLALCHEMY_DATABASE_TEST_URL = "sqlite:///./testdb.db"


engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL,
                       connect_args={"check_same_thread": False},
                       poolclass = StaticPool,
                       )


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username":"miguel_test","id":1,"user_role":"admin"}

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code",
        description = "Need to learn every day!",
        priority = False,
        owner_id = 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()



def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1, 'priority': 0, 'owner_id': 1, 'title': 'Learn to code', 'complete': False, 'description': 'Need to learn every day!'}]


def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'id': 1, 'priority': 0, 'owner_id': 1, 'title': 'Learn to code', 'complete': False, 'description': 'Need to learn every day!'}

def test_read_one_authenticated(test_todo):
    response = client.get("/todos/999")
    assert response.status_code == 404
    assert response.json() == {'detail': "Todo not found."}

def test_create_todo(test_todo):
    request_date = {
        'title': 'New Todo!',
        'description':"New todo description",
        'priority': 5,
        'complete': False
    }

    response = client.post('/todos/add_todo', json = request_date)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_date.get('title')
    assert model.description == request_date.get('description')
    assert model.priority == request_date.get('priority')
    assert model.complete == request_date.get('complete')



def test_update_todo (test_todo):
    request_date = {
        'title': 'New Todo!',
        'description':"New todo description",
        'priority': 5,
        'complete': False
    }
    response = client.put(f'/todos/update/1', json = request_date)

    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_date.get('title')
    assert model.description == request_date.get('description')
    assert model.priority == request_date.get('priority')
    assert model.complete == request_date.get('complete')


def test_update_todo_not_found (test_todo):
    request_date = {
        'title': 'New Todo!',
        'description':"New todo description",
        'priority': 5,
        'complete': False
    }
    response = client.put(f'/todos/update/999', json = request_date)

    assert response.status_code == 404
    assert response.json() == {'detail': "Todo not found."}

def test_update_delete_todo (test_todo):

    response = client.delete(f'/todos/delete/1')

    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model == None
