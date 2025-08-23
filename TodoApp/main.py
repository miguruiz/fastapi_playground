from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, todos, admin, users

app = FastAPI()

Base.metadata.create_all(bind=engine)  # Create the database tables if they do not exist

app.include_router(
    auth.router
)  # Include the auth router to handle authentication-related endpoints
app.include_router(
    todos.router
)  # Include the todos router to handle todo-related endpoints
app.include_router(admin.router)
app.include_router(users.router)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}
