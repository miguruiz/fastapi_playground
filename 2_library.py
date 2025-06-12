from typing import Optional

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field
# .dict() function is now renamed to .model_dump()
# schema_extra function within a Config class is now renamed to json_schema_extra
# Optional variables need a =None example: id: Optional[int] = None

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

@app.get("/books/allbooks")
async def read_all_books():
    return BOOKS

@app.get("/books/")
async def get_books_by_rating(rating: int = Query(gt=0, lt=6)):
    return [book for book in BOOKS if book.rating >= rating]

@app.get("/books/{book_id}")
async def read_book_by_id(book_id: int = Path(gt = 0, lt= 6)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}

print
@app.post("/books/add_book")
async def add_new_book(book: BookRequest):
    new_boook= book_with_id(book)
    BOOKS.append(new_boook)


@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for index, existing_book in enumerate(BOOKS):
        if existing_book.title.casefold() == book.title.casefold():
            book.id = existing_book.id
            BOOKS[index] = Book(**book.model_dump())

@app.delete("/books/delete/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(BOOKS):
        if book.id == book_id:
            BOOKS.pop(index)
            break



def book_with_id(book: BookRequest):
    if BOOKS:
        id = BOOKS[-1].id + 1
    else:
        id = 1
    return Book(id = id, **book.model_dump())