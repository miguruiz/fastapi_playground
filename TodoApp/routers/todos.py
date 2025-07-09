from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, HTTPException
from models import Todos
from database import SessionLocal, get_db
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter()

db_dependency = Annotated[
    Session, Depends(get_db)
]  # This is a type annotation for the database dependency
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    id: Optional[int] = Field(description="ID of the todo", default=None)
    title: str = Field(min_length=3)
    description: str = Field(min_length=3)
    priority: int = Field(ge=1, le=5)  # ge: gr
    complete: bool = Field(default=False)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The title",
                "description": "the desc",
                "priority": "the priority",
                "complete": "is completed?",
            }
        }
    }


@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(401, "User not Authenticated")
    return (
        db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    )  # This will return all the todos from the database


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_from_id(
    user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)
):
    if user is None:
        raise HTTPException(401, "User not Authenticated")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail="Todo not found.")


@router.post("/todos/add_todo", status_code=status.HTTP_201_CREATED)
async def add_todo(user: user_dependency, db: db_dependency, new_todo: TodoRequest):

    if user is None:
        raise HTTPException(401, "User not Authenticated")
    todo_model = Todos(
        **new_todo.model_dump(), owner_id=user.get("id")
    )  # id will automatically increment by SQLALCHEMY

    db.add(todo_model)
    db.commit()


@router.put("/todos/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency, todo_to_update: TodoRequest, todo_id: int = Path(gt=0)
):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    todo_model.title = todo_to_update.title
    todo_model.description = todo_to_update.description
    todo_model.priority = todo_to_update.priority
    todo_model.complete = todo_to_update.complete

    db.add(todo_model)
    db.commit()


@router.delete("/todos/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
