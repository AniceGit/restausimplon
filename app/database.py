from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings  # import de la config

DATABASE_URL = settings.DATABASE_URL
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import os

# # Utilise SQLite en mémoire pour les tests
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# engine = create_engine(DATABASE_URL, echo=True)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def get_session():
#     session = SessionLocal()
#     try:
#         yield session
#     finally:
#         session.close()
