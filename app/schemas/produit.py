from sqlmodel import SQLModel

# Schéma pour la création et la lecture
class ProduitCreate(SQLModel):
    nom: str
    description: str
    prix: float
    stock: int
    categorie_id: int

class ProduitRead(SQLModel):
    id: int
    nom: str
    description: str
    prix: float
    stock: int
    categorie_id: int
