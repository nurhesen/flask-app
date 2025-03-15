# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Get the database URL from the environment variables
DATABASE_URL = os.environ.get("DATABASE_URL")

# Create the database engine.
engine = create_engine(DATABASE_URL)

# Create a session factory.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()