from pydantic import BaseModel, Field
from typing import Optional
from app.models.commande import CommandeStatusEnum


class LigneCommandeRead(BaseModel):
    id: int = Field(..., gt=0, description="Identifiant unique de la ligne")
    commande_id: int = Field(..., gt=0, description="ID de la commande")
    produit_id: int = Field(..., gt=0, description="ID du produit")
    quantite: int = Field(..., ge=1, description="Quantité commandée")
    prix_unitaire: float = Field(..., gt=0, description="Prix unitaire du produit")

    class Config:
        orm_mode = True

class LigneCommandeCreate(BaseModel):
    commande_id: int = Field(..., gt=0, description="ID de la commande parent")
    produit_id: int = Field(..., gt=0, description="ID du produit à commander")
    quantite: int = Field(..., ge=1, le=999, description="Quantité à commander (1-999)")
    prix_unitaire: float = Field(..., gt=0, le=1000, description="Prix unitaire du produit")


class LigneCommandeUpdate(BaseModel):
    id: int = Field(..., gt=0, description="ID de la ligne de commande à modifier")
    commande_id: Optional[int] = Field(None, gt=0, description="Nouvel ID de commande")
    produit_id: Optional[int] = Field(None, gt=0, description="Nouvel ID de produit")
    quantite: Optional[int] = Field(None, ge=1, le=999, description="Nouvelle quantité")
    prix_unitaire: Optional[float] = Field(None, gt=0, le=1000, description="Nouveau prix unitaire")

    class Config:
        orm_mode = True