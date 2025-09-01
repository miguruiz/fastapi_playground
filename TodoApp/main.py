from fastapi import FastAPI, Request

from .database import Base, engine
from .routers import auth, todos, admin, users
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
app = FastAPI()

Base.metadata.create_all(bind=engine)  # Create the database tables if they do not exist

templates = Jinja2Templates(directory="TodoApp/templates")

app.mount("/static", StaticFiles(directory="TodoApp/static"),name="static")

app.include_router(
    auth.router
)  # Include the auth router to handle authentication-related endpoints
app.include_router(
    todos.router
)  # Include the todos router to handle todo-related endpoints
app.include_router(admin.router)
app.include_router(users.router)

@app.get("/")
def test(request:Request):
    return templates.TemplateResponse("home.html",{"request":request})


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}
