from ..models import User, Video
from .db import engine

def add_models_to_database() -> None:
    User.Base.metadata.create_all(bind=engine)
    Video.Base.metadata.create_all(bind=engine)
