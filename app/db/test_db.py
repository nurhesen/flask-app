# app/db/test_db.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base  # Import your Base

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)  # Important for SQLite and testing
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def create_test_db():
    Base.metadata.create_all(bind=test_engine)

def drop_test_db():
    Base.metadata.drop_all(bind=test_engine)