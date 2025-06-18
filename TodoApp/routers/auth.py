from fastapi import  APIRouter
from pydantic import BaseModel
from models import Users

router = APIRouter()# If we used FastAPI, it would be an instance of FastAPI, but here we use APIRouter to
# create a router for the auth endpoints. This allows us to group related endpoints together

class CreateUserRequest(BaseModel):
    username: str
    email:str
    first_name: str
    last_name: str
    password: str
    role: str


@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
    email = create_user_request.email,
    username = create_user_request.username,
    first_name = create_user_request.first_name,
    last_name = create_user_request.last_name,
    hashed_password = create_user_request.password,
    role = create_user_request.role,
)
    return create_user_model