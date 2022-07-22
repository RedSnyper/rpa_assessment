from .db import engine, Base

def add_models_to_database() -> None:
    Base.metadata.create_all(bind=engine)