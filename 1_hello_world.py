from fastapi import FastAPI

app = FastAPI()

# TO RUN
# uvicorn 1_hello_wrold:app --reload
# fastapi run 1_hello_world.py
# fastapi dev 1_hello_world.py

@app.get("/hello-world")
async def first_api():
    return {'message':'HelloWorld!'}



BOOKS = [
    {"title": "1984", "author": "George Orwell", "year": 1949},
    {"title": "To Kill a Mockingbird", "author": "Harper Lee", "year": 1960},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
    {"title": "Moby Dick", "author": "Herman Melville", "year": 1851},
]


@app.get("/books")
async def read_all_books():
    return BOOKS