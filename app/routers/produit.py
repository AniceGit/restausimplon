from sqlmodel import SQLModel, create_engine, Session
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from app.crud.produit import creer_produit, get_all_produits, suppression_produit, modification_produit, rechercher_produits
from app.database import get_session
from app.schemas.produit import ProduitRead, ProduitCreate, ProduitUpdate
from typing import List, Optional

router = APIRouter(prefix="/produits", tags=["Produits"])

@router.get("/", response_model=List[ProduitRead])
def read_produits(session: Session = Depends(get_session)):
    return get_all_produits(session)


@router.post("/", response_model=ProduitRead)
def create_produit(produit: ProduitCreate, session: Session = Depends(get_session)):
    # Utilisez la fonction creer_produit pour ajouter le produit à la base de données
    return creer_produit(produit, session)

@router.delete("/{produit_id}", response_model=ProduitRead)
def delete_produit(produit_id: int, session: Session = Depends(get_session)):
    produit = suppression_produit(produit_id, session)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return produit

@router.put("/{produit_id}", response_model=ProduitRead)
def update_produit(produit_id: int, produit: ProduitUpdate, session: Session = Depends(get_session)):
    produit_data = produit.model_dump(exclude_unset=True)
    updated_produit = modification_produit(produit_id, produit_data, session)
    if updated_produit is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return updated_produit

@router.get("/search", response_model=List[ProduitRead])
def recherche_produit(
    produit_id: Optional[int] = Query(None),
    prix: Optional[float] = Query(None),
    stock: Optional[int] = Query(None),
    session: Session = Depends(get_session)
):
    produits = rechercher_produits(session, produit_id, prix, stock)
    return produits