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

# Endpoint to get all books, should be placed ahead of the path parameter, because of the order of the routes
@app.get("/books/allbooks")
async def read_all_books():
    return BOOKS


# Path Parameters
@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    return BOOKS[book_id]

@app.get("/books/title/{book_title}")
# eg. http://127.0.0.1:8000/books/title/1984
# eg. http://127.0.0.1:8000/books/title/To%20Kill%20a%20Mockingbird
async def get_book_by_title(book_title: str):
    return [book for book in BOOKS.values() if book['title'].lower() == book_title.lower()]


