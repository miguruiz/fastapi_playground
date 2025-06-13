from typing import Annotated

from fastapi import FastAPI, Depends
import models
from models import Todos
from database import engine, SessionLocal
from sqlalchemy.orm import Session

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
