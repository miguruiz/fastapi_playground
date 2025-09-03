from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy import and_
from starlette.requests import Request
from starlette.responses import RedirectResponse

from ..models import Todos
from ..database import SessionLocal, get_db
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from .auth import get_current_user
from fastapi.templating import  Jinja2Templates

router = APIRouter(
    prefix='/todos',
    tags=['todos']
)

db_dependency = Annotated[
    Session, Depends(get_db)
]  # This is a type annotation for the database dependency
user_dependency = Annotated[dict, Depends(get_current_user)]

templates = Jinja2Templates(directory="TodoApp/templates")

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

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key = "access_token")
    return redirect_response


### Pages ###
@router.get("/todo-page")
async def render_todo_page(request:Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todos = db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
        return templates.TemplateResponse("todo.html",{"request": request,"todos":todos,"user":user})

    except:
        return redirect_to_login()

@router.get("/add-todo-page")
async def render_add_todo_page(request:Request):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        return templates.TemplateResponse("add-todo.html",{"request": request,"user":user})

    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request:Request, db: db_dependency, todo_id:int = Path(gt=0)):
    try:
        user = await get_current_user(request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        todo = db.query(Todos).filter(
            and_(
                Todos.owner_id == user.get("id"),
                Todos.id == todo_id
            )
        ).first()
        return templates.TemplateResponse("edit-todo.html",{"request": request,"todo":todo,"user":user})

    except:
        return redirect_to_login()

### ENDPOINTS ###

@router.get("/")
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(401, "User not Authenticated")
    return (
        db.query(Todos).filter(Todos.owner_id == user.get("id")).all()
    )  # This will return all the todos from the database


@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
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


@router.post("/add_todo", status_code=status.HTTP_201_CREATED)
async def add_todo(user: user_dependency, db: db_dependency, new_todo: TodoRequest):

    if user is None:
        raise HTTPException(401, "User not Authenticated")
    todo_model = Todos(
        **new_todo.model_dump(), owner_id=user.get("id")
    )  # id will automatically increment by SQLALCHEMY

    db.add(todo_model)
    db.commit()


@router.put("/update/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_to_update: TodoRequest,
    todo_id: int = Path(gt=0),
):
    if user is None:
        raise HTTPException(401, "User not Authenticated")

    todo_model = (
        db.query(Todos)
        .filter(Todos.id == todo_id)
        .filter(Todos.owner_id == user.get("id"))
        .first()
    )

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    todo_model.title = todo_to_update.title
    todo_model.description = todo_to_update.description
    todo_model.priority = todo_to_update.priority
    todo_model.complete = todo_to_update.complete

    db.add(todo_model)
    db.commit()


@router.delete("/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
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
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    db.query(Todos).filter(Todos.id == todo_id).filter(
        Todos.owner_id == user.get("id")
    ).delete()
    db.commit()
