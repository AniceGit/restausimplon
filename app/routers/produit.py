from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas.produit import ProduitRead
from app.crud.produit import get_all_produits

router = APIRouter(prefix="/produits", tags=["Produits"])

@router.get("/", response_model=List[ProduitRead])
def read_produits(session: Session = Depends(get_session)):
    return get_all_produits(session)
