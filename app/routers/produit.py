from sqlmodel import SQLModel, create_engine, Session
from fastapi import APIRouter, Depends, Query
from typing import List
from app.crud.produit import creer_produit, get_all_produits, suppression_produit, modification_produit, rechercher_produits
from app.database import get_session
from app.schemas.produit import ProduitRead, ProduitCreate, ProduitUpdate
from typing import List, Optional

#gestion des autorisations :
from fastapi import HTTPException, status
from app.core.security import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(prefix="/produits", tags=["Produits"])

@router.get("/", response_model=List[ProduitRead])
def read_produits(session: Session = Depends(get_session)):
    return get_all_produits(session)

#autorisé pour admin et employé
@router.post("/", response_model=ProduitRead)
def create_produit(
    produit: ProduitCreate,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return creer_produit(produit, session)

#autorisé pour admin et employé
@router.delete("/{produit_id}", response_model=ProduitRead)
def delete_produit(
    produit_id: int,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    produit = suppression_produit(produit_id, session)
    return produit

#autorisé pour admin et employé
@router.put("/{produit_id}", response_model=ProduitRead)
def update_produit(
    produit_id: int,
    produit: ProduitUpdate,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    produit_data = produit.model_dump(exclude_unset=True)
    updated_produit = modification_produit(produit_id, produit_data, session)
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