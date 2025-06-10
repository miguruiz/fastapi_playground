from fastapi import FastAPI

app = FastAPI()

# TO RUN
# uvicorn 1_hello_wrold:app --reload
# fastapi run 1_hello_world.py
# fastapi dev 1_hello_world.py

# Swagger UI: http://127.0.0.1:8000/docs
@app.get("/hello-world")
async def hello_world():
    return {'message':'HelloWorld!'}



BOOKS = {
    1: {"title": "1984", "author": "George Orwell", "year": 1949},
    2: {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    3: {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    4: {"title": "Moby Dick", "author": "Herman Melville", "year": 1851},
}


@app.get("/books")
async def read_all_books():
    return BOOKS


# Path Parameters
@app.get("/books/{book_id}")
async def read_all_books(book_id: int):
    return BOOKS[book_id]