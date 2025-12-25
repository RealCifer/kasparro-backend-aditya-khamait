from core.db import Base, engine
from core import models


def init_db():
    if engine:
        Base.metadata.create_all(bind=engine)
