from core.db import engine, init_engine
from core.models import Base

def init_db():
    init_engine()

    if engine is None:
        print("DATABASE_URL not set, skipping DB init")
        return

    Base.metadata.create_all(bind=engine)
