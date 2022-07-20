from fastapi import FastAPI
from app.database import add_models_to_database,generate_fake_data

app = FastAPI()
add_models_to_database()
generate_fake_data()

@app.get('/')
def main():
    return {"message": "hello world"}