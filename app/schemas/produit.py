from pydantic import BaseModel
from typing import Optional

class ProduitCreate(BaseModel):
    nom: str
    description: str
    prix: float
    stock: int
    categorie_id: int

class ProduitRead(BaseModel):
    id: int
    nom: str
    description: str
    prix: float
    stock: int
    categorie_id: int

class ProduitUpdate(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    prix: Optional[float] = None
    stock: Optional[int] = None
    categorie_id: Optional[int] = None

    class Config:
        from_attributes = True
