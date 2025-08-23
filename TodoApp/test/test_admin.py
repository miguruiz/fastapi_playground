from .utils import *
from ..routers.admin import get_db, get_current_user # To ensure we override the ones of the file we intend to test
from fastapi import  status
app.dependency_overrides[get_db] = override_get_db()
app.dependency_overrides[get_current_user] = override_get_current_user()

def test_admin_read_all_authenticated(test_todo):
    response = client.get("/admin/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'id': 1, 'priority': 0, 'owner_id': 1, 'title': 'Learn to code', 'complete': False, 'description': 'Need to learn every day!'}]

def test_admin_delete_todo (test_todo):

    response = client.delete(f'/admin/delete/1')

    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model == None


def test_admin_delete_todo_not_found (test_todo):

    response = client.delete(f'/admin/delete/9991')

    assert response.status_code == 404
