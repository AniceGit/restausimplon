from pydantic import BaseModel, Field
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
    quantite: int = Field(ge=1)
    prix_unitaire: float = Field(gt=0)


class LigneCommandeUpdate(BaseModel):
    id: int
    commande_id: Optional[int] = None
    produit_id: Optional[int] = None
    quantite: Optional[int] = Field(None, ge=1)
    prix_unitaire: Optional[float] = Field(None, gt=0)

    class Config:
        orm_mode = True