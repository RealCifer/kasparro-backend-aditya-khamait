import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

engine = None
SessionLocal = None

def init_engine():
    global engine, SessionLocal

    if DATABASE_URL and engine is None:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True
        )
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine
        )
