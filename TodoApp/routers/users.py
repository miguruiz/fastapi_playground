from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, HTTPException
from passlib.context import CryptContext

from ..models import Todos, Users
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db_dependency = Annotated[
    Session, Depends(get_db)
]  # This is a type annotation for the database dependency
user_dependency = Annotated[dict, Depends(get_current_user)]


class PasswordChangeRequest(BaseModel):
    old_password: str = Field()
    new_password: str = Field(min_length=3)
    new_password_validation: str = Field(min_length=3)

    model_config = {
        "json_schema_extra": {
            "example": {
                "old_password": "old_passw",
                "new_password": "new_passw",
                "new_password_validation": "new_passw",
            }
        }
    }


@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed. ")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    return user_model


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency, db: db_dependency, passw_change: PasswordChangeRequest
):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    user_model: Users = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(passw_change.old_password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect old password")

    if not passw_change.new_password == passw_change.new_password_validation:
        raise HTTPException(status_code=401, detail="New passwords don't match")

    user_model.hashed_password = bcrypt_context.hash(passw_change.new_password)
    db.add(user_model)
    db.commit()


@router.put(
    "/add_or_update_phone_number/{phone_number}", status_code=status.HTTP_204_NO_CONTENT
)
async def change_password(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication failed.")
    user_model: Users = db.query(Users).filter(Users.id == user.get("id")).first()

    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
