from .utils import *
from ..routers.users import get_db, get_current_user
from fastapi import status


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_return_user(test_user):
    response = client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    response_dict = response.json()
    password = response_dict.pop('hashed_password', None)
    assert response_dict == {'last_name': 'Bar', 'id': 1, 'first_name': 'Foo', 'phone_number': '+34 7682947299', 'email': 'email@email.com', 'username': 'miguel_test', 'is_active': True, 'role': 'admin'}
    assert bcrypt_context.verify("12345", password)


def test_change_password_success(test_user):
    response = client.put("/user/change_password", json={
  "new_password": "new_passw",
  "new_password_validation": "new_passw",
  "old_password": "12345"
})
    assert response.status_code == status.HTTP_204_NO_CONTENT


