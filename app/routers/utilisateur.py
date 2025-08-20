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
def read_utilisateurs(_: Utilisateur = Depends(require_admin), session: Session = Depends(get_session)):
    """
    Récupère la liste de tous les utilisateurs.

    Autorisation :
        - Réservée aux administrateurs uniquement.

    Args:
        _: Utilisateur authentifié (vérifié par require_admin).
        session (Session): Session de base de données SQLModel.

    Returns:
        List[UtilisateurRead]: Liste de tous les utilisateurs.
    """
    return get_all_utilisateurs(session)


@router.get("/{utilisateur_id}", response_model=UtilisateurRead)
def read_utilisateur(utilisateur_id: int, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Récupère un utilisateur par son ID.

    Autorisation :
        - L'utilisateur peut accéder à son propre profil.
        - Les administrateurs peuvent accéder à tous les profils.

    Args:
        utilisateur_id (int): ID de l'utilisateur à récupérer.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        UtilisateurRead: Données de l'utilisateur demandé.

    Raises:
        HTTPException 403: Si un utilisateur non-admin tente d'accéder au profil d'un autre utilisateur.
        HTTPException 404: Si l'utilisateur n'existe pas.
    """
    if current_user.role != "admin" and current_user.id != utilisateur_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Accès refusé : vous ne pouvez consulter que votre propre profil."
        )
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur


@router.post("/", response_model=UtilisateurRead)
def add_utilisateur(utilisateur_data: UtilisateurCreate, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Crée un nouvel utilisateur.

    Autorisation :
        - Réservée aux administrateurs uniquement.

    Args:
        utilisateur_data (UtilisateurCreate): Données pour créer le nouvel utilisateur.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        UtilisateurRead: L'utilisateur nouvellement créé.

    Raises:
        HTTPException 403: Si l'utilisateur courant n'est pas un administrateur.
    """
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return create_utilisateur(session, utilisateur_data)


@router.put("/{utilisateur_id}", response_model=UtilisateurRead)
def edit_utilisateur(
    utilisateur_id: int,
    utilisateur_data: UtilisateurUpdate,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    """
    Met à jour un utilisateur existant.

    Autorisation :
        - L'utilisateur peut modifier son propre compte.
        - Les administrateurs peuvent modifier tous les comptes.

    Args:
        utilisateur_id (int): ID de l'utilisateur à mettre à jour.
        utilisateur_data (UtilisateurUpdate): Données mises à jour.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        UtilisateurRead: Utilisateur mis à jour.

    Raises:
        HTTPException 404: Si l'utilisateur n'existe pas.
        HTTPException 403: Si l'utilisateur courant n'est pas autorisé.
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if current_user.role != "admin" and current_user.id != utilisateur_id:
        raise HTTPException(status_code=403, detail="Accès refusé")

    return update_utilisateur(utilisateur_id, utilisateur_data, session)


@router.delete("/{utilisateur_id}", response_model=UtilisateurRead)
def remove_utilisateur(
    utilisateur_id: int,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    """
    Supprime un utilisateur existant.

    Autorisation :
        - L'utilisateur peut supprimer son propre compte.
        - Les administrateurs peuvent supprimer tous les comptes.

    Args:
        utilisateur_id (int): ID de l'utilisateur à supprimer.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        UtilisateurRead: Utilisateur supprimé.

    Raises:
        HTTPException 404: Si l'utilisateur n'existe pas.
        HTTPException 403: Si l'utilisateur courant n'est pas autorisé.
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    if current_user.role != "admin" and current_user.id != utilisateur_id:
        raise HTTPException(status_code=403, detail="Accès refusé")

    return delete_utilisateur(utilisateur_id, session)
