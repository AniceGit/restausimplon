from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.commande import CommandeStatusEnum


class LigneCommandeRead(BaseModel):
    id: int
    commande_id: int
    produit_id: int
    quantite: int
    prix_unitaire: float

    class Config:
        orm_mode = True

class LigneCommandeCreate(BaseModel):
    commande_id: int
    produit_id: int
    quantite: int
    prix_unitaire: float

    class Config:
        orm_mode = True

class LigneCommandeUpdate(BaseModel):
    id: int
    commande_id: Optional[int] = None
    produit_id: Optional[int] = None
    quantite: Optional[int] = None
    prix_unitaire: Optional[float] = None