from pydantic import BaseModel
from typing import Optional

class ProduitRead(BaseModel):
    id: int
    nom: str
    description: Optional[str]
    prix: float
    stock: int
    categorie_id: int

    class Config:
        orm_mode = True
