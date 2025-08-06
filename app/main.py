from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import produit
from app.routers import utilisateur
from app.routers import commande, ligne_de_commande

app = FastAPI(title="RestauSimplon API")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(produit.router)
app.include_router(utilisateur.router)
#app.include_router(client.router)
app.include_router(commande.router)
app.include_router(ligne_de_commande.router)

@app.get("/")
def root():
    return {"message": "Bienvenue sur l’API RestauSimplon"}