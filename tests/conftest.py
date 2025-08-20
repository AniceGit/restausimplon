import os
import pytest
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://test_user:test_password@localhost:5432/test_db")

engine = create_engine(DATABASE_URL, echo=False)

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine) 

@pytest.fixture(scope="function")
def session():
    with Session(engine) as s:
        yield s