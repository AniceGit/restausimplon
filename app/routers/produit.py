from sqlmodel import SQLModel, create_engine, Session
from fastapi import APIRouter, Depends
from typing import List
from app.crud.produit import creer_produit, get_all_produits
from app.database import get_session
from app.schemas.produit import ProduitRead, ProduitCreate


router = APIRouter(prefix="/produits", tags=["Produits"])

@router.get("/", response_model=List[ProduitRead])
def read_produits(session: Session = Depends(get_session)):
    return get_all_produits(session)


@router.post("/", response_model=ProduitRead)
def create_produit(produit: ProduitCreate, session: Session = Depends(get_session)):
    # Utilisez la fonction creer_produit pour ajouter le produit à la base de données
    return creer_produit(produit, session)