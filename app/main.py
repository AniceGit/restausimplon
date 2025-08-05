from fastapi import FastAPI
from app.database import create_db_and_tables

app = FastAPI(title="RestauSimplon API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l’API RestauSimplon"}
