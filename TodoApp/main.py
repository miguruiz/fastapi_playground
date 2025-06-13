from typing import Annotated, Optional

from fastapi import FastAPI, Depends, Path, HTTPException
import models
from models import Todos
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field

app = FastAPI()

models.Base.metadata.create_all(bind=engine) # Create the database tables if they do not exist


def get_db():
     db = SessionLocal()
     try:
        yield db # This is a generator function that yields a database session because FastAPI uses dependency injection
        # to manage resources like database connections. When the request is done, FastAPI will automatically close the session.
        # If we don't use yield here, the session would be closed immediately after the function returns, which would not allow us
        # to use the session in the request handler.
     finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]  # This is a type annotation for the database dependency

class TodoRequest(BaseModel):
    id: Optional[int] = Field(description= "ID of the todo", default=None)
    title: str = Field(min_length=3)
    description: str =Field(min_length=3)
    priority: int = Field(ge=1, le=5)  # ge: gr
    complete: bool = Field(default=False)


    model_config = {
        "json_schema_extra": {
            "example": {
                "id":"the Id",
                "title":"The title",
                "description":"the desc",
                "priority":"the priority",
                "complete":"is completed?"
            }
        }
    }



@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()  # This will return all the todos from the database


@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo_from_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(status_code=404, detail='Todo not found.')

@app.post("/todos/add_todo",status_code=status.HTTP_201_CREATED)
async def add_todo(db: db_dependency, new_todo: TodoRequest):
    todo_model = Todos(**new_todo.model_dump()) # id will automatically incremented by SQLALCHEMY

    db.add(todo_model)
    db.commit()


@app.put("/todos/update/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency,todo_to_update: TodoRequest, todo_id: int = Path(gt=0) ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    todo_model.title = todo_to_update.title
    todo_model.description= todo_to_update.description
    todo_model.priority = todo_to_update.priority
    todo_model.complete = todo_to_update.complete

    db.add(todo_model)
    db.commit()

@app.delete("/todos/delete/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()