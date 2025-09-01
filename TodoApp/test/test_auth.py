from datetime import timedelta

from jose import jwt
from starlette.exceptions import HTTPException

from .utils import *
from ..routers.auth import get_db, get_current_user, \
    authenticate_user, create_access_token, SECRET_KEY, \
    ALGORITHM  # To ensure we override the ones of the file we intend to test
from fastapi import  status
import pytest

app.dependency_overrides[get_db] = override_get_db()
app.dependency_overrides[get_current_user] = override_get_current_user()


def test_authenticated_user(test_user):
    db = TestingSessionLocal()
    authenticated_user = authenticate_user(test_user.username, "12345", db)
    assert authenticated_user is not None
    assert authenticated_user.username == 'miguel_test'


def test_create_access_token():
    username = "foo"
    id = 1
    role= "bar"
    access_token = create_access_token(username, id, role, timedelta(days = 1))

    decoded_token = jwt.decode(access_token, SECRET_KEY, ALGORITHM)

    assert username == decoded_token.get("sub")
    assert id == decoded_token.get("id")
    assert role == decoded_token.get("role")


@pytest.mark.asyncio
async def test_get_current_user(test_user):
    username = "foo"
    id = 1
    role= "bar"

    encode = {"sub": username, "id": id, "role": role}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    user = await get_current_user(token)

    assert user == {"username": username, "id": id, "user_role": role}


@pytest.mark.asyncio
async def test_get_current_user_not_valid(test_user):
    role= "bar"

    encode = {"role": role}
    token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as e:
        await get_current_user(token)
    assert e.value.status_code == 401
    assert e.value.detail == 'Could not validate user.'