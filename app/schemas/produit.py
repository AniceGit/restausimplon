from pydantic import BaseModel, Field
from typing import Optional

class ProduitCreate(BaseModel):
    nom: str = Field(..., min_length=1, max_length=100, description="Nom du produit")
    description: str = Field(..., min_length=1, max_length=100, description="Description du produit")
    prix: float = Field(..., gt=0, description="Prix du produit")
    stock: int = Field(..., ge=0, description="Quantité en stock, ne peut pas être négatif")
    categorie_id: int = Field(..., gt=0, description="ID de la catégorie à laquelle le produit appartient, doit être supérieur à 0")


class ProduitRead(BaseModel):
    id: int = Field(..., description="Identifiant unique du produit")
    nom: str
    description: str
    prix: float
    stock: int
    categorie_id: int

class ProduitUpdate(BaseModel):
    nom: Optional[str] = Field(None, min_length=1, max_length=100, description="Nom du produit")    
    description: Optional[str] = Field(None, min_length=1, max_length=100, description="Description du produit")
    prix: Optional[float] = Field(None, gt=0, description="Prix du produit")
    stock: Optional[int] = Field(None, ge=0, description="Quantité en stock, ne peut pas être négatif")
    categorie_id: Optional[int] = Field(None, gt=0, description="ID de la catégorie à laquelle le produit appartient, doit être supérieur à 0")
    
    class Config:
        from_attributes = True