# app/routers/user.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import List

from app.database import get_session
from app.schemas.utilisateur import UtilisateurRead, UtilisateurCreate
from app.models.utilisateur import Utilisateur
from app.crud.utilisateur import get_all_utilisateurs, create_utilisateur, get_utilisateur_by_id

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

@router.get("/", response_model=List[UtilisateurRead])
def read_utilisateurs(session: Session = Depends(get_session)):
    return get_all_utilisateurs(session)

@router.get("/{utilisateur_id}", response_model=UtilisateurRead)
def read_utilisateur(utilisateur_id: int, session: Session = Depends(get_session)):
    return get_utilisateur_by_id(utilisateur_id, session)

@router.post("/", response_model=UtilisateurRead)
def add_utilisateur(utilisateur_data: UtilisateurCreate, session: Session = Depends(get_session)):
    return create_utilisateur(session, utilisateur_data)
