# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app.core.security import get_password_hash,verify_password

from app.database import get_session
from app.schemas.utilisateur import UtilisateurRead, UtilisateurCreate, UtilisateurUpdate
from app.models.utilisateur import Utilisateur, RoleEnum
from app.crud.utilisateur import get_all_utilisateurs, create_utilisateur, get_utilisateur_by_id, update_utilisateur, delete_utilisateur

#Autorisations : 
from app.core.security import require_admin, get_current_user

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])

#La lecture de tous les utilisateurs est réservée aux admin
@router.get("/", response_model=List[UtilisateurRead])
def read_utilisateurs(_: Utilisateur = Depends(require_admin),session: Session = Depends(get_session)):
    return get_all_utilisateurs(session)

@router.get("/{utilisateur_id}", response_model=UtilisateurRead)
def read_utilisateur(utilisateur_id: int, session: Session = Depends(get_session),current_user: Utilisateur = Depends(get_current_user)):
    # Si utilisateur non admin et qu'il essaie d'accéder à un profil autre que le sien
    if current_user.role != "admin" and current_user.id != utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Accès refusé : vous ne pouvez consulter que votre propre profil."
        )
    utilisateur = session.get(Utilisateur, utilisateur_id)

    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

#Fonction à revoir, néanmoins réservé aux admin
@router.post("/", response_model=UtilisateurRead)
def add_utilisateur(utilisateur_data: UtilisateurCreate, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    # Autorisation : seul admin peut créer un utilisateur
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return create_utilisateur(session, utilisateur_data)

#update de tous les comptes autorisé que pour l'admin et l'utilisateur que sur son propre compte
@router.put("/{utilisateur_id}", response_model=UtilisateurRead)
def edit_utilisateur(
    utilisateur_id: int,
    utilisateur_data: UtilisateurUpdate,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    # Vérifier si l'utilisateur existe
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Autorisation : admin ou utilisateur lui-même
    if current_user.role != "admin" and current_user.id != utilisateur_id:
        raise HTTPException(status_code=403, detail="Accès refusé")

    # Appeler la fonction update (implémente ta logique dans update_utilisateur)
    return update_utilisateur(utilisateur_id, utilisateur_data, session)

#suppression de tous les comptes autorisé que pour l'admin et l'utilisateur que sur son propre compte
@router.delete("/{utilisateur_id}", response_model=UtilisateurRead)
def remove_utilisateur(
    utilisateur_id: int,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Autorisation : admin ou utilisateur lui-même
    if current_user.role != "admin" and current_user.id != utilisateur_id:
        raise HTTPException(status_code=403, detail="Accès refusé")

    # Soft delete : passer is_active à False
    utilisateur.is_active = False
    session.add(utilisateur)
    session.commit()
    session.refresh(utilisateur)
    return utilisateur