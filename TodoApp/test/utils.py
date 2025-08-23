import pytest
from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..models import Base, Todos, Users
from ..main import app
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_TEST_URL = "sqlite:///./testdb.db"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

engine = create_engine(SQLALCHEMY_DATABASE_TEST_URL,
                       connect_args={"check_same_thread": False},
                       poolclass = StaticPool,
                       )


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username":"miguel_test","id":1,"user_role":"admin"}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code",
        description = "Need to learn every day!",
        priority = False,
        owner_id = 1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        id = 1,
        email = "email@email.com",
        username = "miguel_test",
        first_name = "Foo",
        last_name = "Bar",
        hashed_password = bcrypt_context.hash("12345"),
        is_active = True,
        role = 'admin',
        phone_number = "+34 7682947299"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users"))
        connection.commit()



oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


SECRET_KEY = "5b3a0f116bbdd192024d265939689baab023d45a691241e37b06a2fc0ee51503"
ALGORITHM = "HS256"