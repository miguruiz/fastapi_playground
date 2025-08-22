SQLALCHEMY_DATABASE_URL = (
    "postgresql://postgres:12345@localhost/TodoApplicationDatabase"
)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(SQLALCHEMY_DATABASE_URL)  # To enable multiple threads to
# access the SQLite database simultaneously.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db  # This is a generator function that yields a database session because FastAPI uses dependency injection
        # to manage resources like database connections. When the request is done, FastAPI will automatically close the session.
        # If we don't use yield here, the session would be closed immediately after the function returns, which would not allow us
        # to use the session in the request handler.
    finally:
        db.close()
