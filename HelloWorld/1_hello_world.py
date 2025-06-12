from fastapi import FastAPI, Body

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
    2: {"title": "A first book", "author": "Harper Lee", "year": 1959},
    3: {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    4: {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    5: {"title": "Moby Dick", "author": "Herman Melville", "year": 1851},
}

#########
# GET ... (READ) .. It does not accept a Body
#########

# Endpoint to get all books, should be placed ahead of the path parameter, because of the order of the routes
@app.get("/books/allbooks")
async def read_all_books():
    return BOOKS


# PATH PARAMETERS
@app.get("/books/{book_id}")
async def get_book_by_id(book_id: int):
    return BOOKS[book_id]

@app.get("/books/title/{book_title}")
# eg. http://127.0.0.1:8000/books/title/1984
# eg. http://127.0.0.1:8000/books/title/To%20Kill%20a%20Mockingbird
async def get_book_by_title(book_title: str):
    return [book for book in BOOKS.values() if book['title'].casefold() == book_title.casefold()]

# QUERY PARAMETERS  -> name-value pairs in the URL

@app.get("/books/")
# http://127.0.0.1:8000/books/?author=George%20Orwell
async def get_book_by_title(author: str):
    return [book for book in BOOKS.values() if book['author'].casefold() == author.casefold()]


# QUERY PARAMETERS  + PATH PARAMETER

@app.get("/books/{year}/")
# http://127.0.0.1:8000/books/1959/?author=Harper%20Lee
async def get_book_by_title(year: int, author: str):
    return [book for book in BOOKS.values() if book['author'].casefold() == author.casefold() and book['year'] == year]




#########
# POST ... (CREATE) .. It accepts a Body
#########
@app.post("/books/add_book/")
# Go to swagger, click on the "Try it out" button, fill in the fields and click on "Execute".
# eg. {"title": "One Last Book", "author": "Who knows", "year": 2023}
async def add_book(new_book=Body()):
    BOOKS[len(BOOKS) + 1] = new_book
    return BOOKS

#########
# PUT ... (UPDATE) .. It accepts a Body
#########

@app.put("/books/update_book/")
# eg. {"title": "One Last Book", "author": "Who knows", "year": 2023}
async def add_book(new_book=Body()):
    book_to_update = new_book.get('title')
    for id, book in BOOKS.items():
        if book['title'].casefold() == book_to_update.casefold():
            BOOKS[id] = new_book
            break
    return BOOKS


#########
# DELETE ... (DELETE) .. It does not accept a Body
#########


@app.delete("/books/delete/{book_id}")
async def get_book_by_title(book_id: int):
    return BOOKS.pop(book_id)