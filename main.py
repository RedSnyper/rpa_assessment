from fastapi import FastAPI
from app.database import add_models_to_database,generate_fake_data
from app.api import api_router
app = FastAPI()
add_models_to_database()
generate_fake_data()

app.include_router(api_router, prefix='/api')


@app.get('/')
def main():
    return {"message": "hello world"}