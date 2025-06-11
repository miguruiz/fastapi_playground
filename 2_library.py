from typing import Optional

from fastapi import FastAPI, Body
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


BOOKS = []

@app.get("/books/allbooks")
async def read_all_books():
    return BOOKS


@app.post("/books/add_book")
async def add_new_book(book: BookRequest):
    new_boook= book_with_id(book)
    BOOKS.append(new_boook)


def book_with_id(book: BookRequest):
    if BOOKS:
        id = BOOKS[-1].id + 1
    else:
        id = 1
    return Book(id = id, **book.model_dump())