SQLALCHEMY_DATABASE_URL = "sqlite:///./todo.db"

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) # To enable multiple threads to
# access the SQLite database simultaneously.

SessionLocal = sessionmaker (autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
