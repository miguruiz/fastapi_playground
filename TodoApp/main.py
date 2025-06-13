from typing import Annotated, Optional

from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos


app = FastAPI()

models.Base.metadata.create_all(bind=engine) # Create the database tables if they do not exist

app.include_router(auth.router) # Include the auth router to handle authentication-related endpoints
app.include_router(todos.router) # Include the todos router to handle todo-related endpoints
