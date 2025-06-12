# Error codes for the application
# 1xx -> Information response: Request is Processing. "Something is happening"
# 2xx -> Success response: Request is successful. "Everything is fine"
#        200 -> Commonly used for successful GET requests when data is returned.
#        201 -> Commonly used for successful POST requests when a new resource is created.
#        204 -> Commonly used for successful for PUT and DELETE requests when the request is successful but does not return content.
# 3xx -> Redirection response: Request is redirected. "Further action is needed"
# 4xx -> Client error response: Request contains an error. "Something is wrong with the request"
#        400 -> Bad Request: The request cannot be processed due to client error.
#        401 -> Unauthorized: The client does not have the right authorisation.
#        403 -> Forbidden: The client does not have permission to access the requested resource.
#        404 -> Not Found: The client requested resource does not exist.
#        422 -> Unprocessable Entity: The request is well-formed but contains semantic errors, such as validation errors.
# 5xx -> Server error response: Request cannot be processed. "Something went wrong on the server side"
#        500 -> Internal Server Error: Generic message when an unexpected issue on the server occurs.

from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    desc: str
    rating: int

    def __init__(self, id: int, title: str, author:str, desc: str, rating: int):
        self.id = id
        self.title = title
        self.author = author
        self.desc = desc
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description= "ID of the book, optional for new books", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    desc: str = Field(min_length=10, max_length=100)
    rating: int = Field(ge=1, le=5)  # ge: gr

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The title of the book",
                "author": "The auth of the book",
                "desc": "The description of the book",
                "rating": 4
            }
        }
    }


BOOKS = [
    Book(id=1, title="1984", author="George Orwell", desc="A dystopian novel set in a totalitarian society.", rating=5),
    Book(id=2, title="To Kill a Mockingbird", author="Harper Lee", desc="A novel about racial injustice in the Deep South.", rating=4),
]

@app.get("/books/allbooks", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/", status_code=status.HTTP_200_OK)
async def get_books_by_rating(rating: int = Query(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating >= rating]


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt = 0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="No books found with the specified rating")


@app.post("/books/add_book", status_code=status.HTTP_201_CREATED)
async def add_new_book(book: BookRequest):
    new_boook= book_with_id(book)
    BOOKS.append(new_boook)


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_found_flag = False
    for index, existing_book in enumerate(BOOKS):
        if existing_book.title.casefold() == book.title.casefold():
            book.id = existing_book.id
            BOOKS[index] = Book(**book.model_dump())
            book_found_flag = True
            break
    if not book_found_flag:
        raise HTTPException(status_code=404, detail="Book not found for update")

@app.delete("/books/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    book_found_flag = False
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            book_found_flag = True
            break
    if not book_found_flag:
        raise HTTPException(status_code=404, detail="Book not found for update")


def book_with_id(book: BookRequest):
    if BOOKS:
        id = BOOKS[-1].id + 1
    else:
        id = 1
    return Book(id = id, **book.model_dump())