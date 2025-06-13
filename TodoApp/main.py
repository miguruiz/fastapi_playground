from typing import Annotated

from fastapi import FastAPI, Depends, Path, HTTPException
import models
from models import Todos
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from starlette import status

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
