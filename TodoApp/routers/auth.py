from typing import Annotated

from fastapi import  APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()# If we used FastAPI, it would be an instance of FastAPI, but here we use APIRouter to
# create a router for the auth endpoints. This allows us to group related endpoints together

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

db_dependency = Annotated[Session, Depends(get_db)]  # This is a type annotation for the database dependency

def authenticate_user(username: str, passw: str, db: db_dependency ):
    user: Users = db.query(Users).filter(Users.username == username).first()


    if not user:
        return False
    if not bcrypt_context.verify(passw, user.hashed_password):
        return False
    return True

class CreateUserRequest(BaseModel):
    username: str
    email:str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest, db: db_dependency):
    create_user_model = Users(
    email = create_user_request.email,
    username = create_user_request.username,
    first_name = create_user_request.first_name,
    last_name = create_user_request.last_name,
    hashed_password = bcrypt_context.hash(create_user_request.password),
    role = create_user_request.role,
)

    db.add(create_user_model)
    db.commit()
    return create_user_model


@router.post("/token")
async def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    if not authenticate_user(from_data.username, from_data.password, db):
        return 'Failed Authentication'
    else:
        return 'Authenticated'

    return {"access_token": "token", "token_type": "bearer"}