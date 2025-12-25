from core.db import engine
from core.models import Base

def init_db():
    Base.metadata.create_all(bind=engine)
