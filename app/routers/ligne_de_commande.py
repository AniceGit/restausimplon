from fastapi import APIRouter, HTTPException, Depends, status
from sqlmodel import Session
from typing import List

from app.database import get_session

from app.schemas.ligne_de_commande import LigneCommandeRead, LigneCommandeCreate, LigneCommandeUpdate
from app.crud.ligne_de_commande import get_all_lignes_commande, get_ligne_commande_by_id, create_ligne_commande, update_ligne_commande, delete_ligne_commande
from app.services.ligne_de_commande import get_lignes_commandes_by_commande
from app.schemas.commande import CommandeWithLignes

#gestion des autorisations : 
from app.core.security import get_current_user
from app.models.utilisateur import Utilisateur

"""
Module de gestion des lignes de commande via API REST.

Ce module fournit des routes pour créer, lire, mettre à jour et supprimer des lignes de commande,
ainsi que pour récupérer les lignes associées à une commande spécifique.  
L'accès aux routes est limité aux utilisateurs ayant le rôle "admin" ou "employe".

Routes principales :
- GET /lignes-de-commande/ : Récupère toutes les lignes de commande.
  - Autorisé uniquement pour les admin et employé.

- GET /lignes-de-commande/{ligne_commande_id} : Récupère une ligne de commande par son ID.
  - Autorisé uniquement pour les admin et employé.

- GET /lignes-de-commande/commande/{commande_id} : Récupère toutes les lignes pour une commande spécifique.
  - Autorisé uniquement pour les admin et employé.

- POST /lignes-de-commande/ : Crée une nouvelle ligne de commande.
  - Autorisé uniquement pour les admin et employé.

- PUT /lignes-de-commande/{ligne_commande_id} : Met à jour une ligne de commande existante.
  - Autorisé uniquement pour les admin et employé.

- DELETE /lignes-de-commande/{ligne_commande_id} : Supprime une ligne de commande.
  - Autorisé uniquement pour les admin et employé.

Chaque route utilise SQLModel pour l'accès à la base de données via `Session`.  
L'authentification et l'autorisation sont gérées par la dépendance `get_current_user`.
"""
router = APIRouter(prefix="/lignes-de-commande", tags=["Lignes de commande"])

@router.get("/", response_model=List[LigneCommandeRead])
def read_lignes_commande(session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Récupère toutes les lignes de commande.

    Autorisation :
        - Admin et Employé uniquement.

    Args:
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        List[LigneCommandeRead]: Liste de toutes les lignes de commande.
    
    Raises:
        HTTPException: Si l'utilisateur n'a pas le rôle admin ou employé.
    """
    # Seuls admin et employé peuvent voir les lignes de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return get_all_lignes_commande(session)

@router.get("/{ligne_commande_id}", response_model=LigneCommandeRead)
def read_ligne_commande_by_id(ligne_commande_id: int, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Récupère une ligne de commande par son ID.

    Autorisation :
        - Admin et Employé uniquement.

    Args:
        ligne_commande_id (int): ID de la ligne de commande.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        LigneCommandeRead: Ligne de commande correspondante.
    
    Raises:
        HTTPException: Si l'utilisateur n'a pas le rôle admin ou employé.
    """
    # Seuls admin et employé peuvent voir les lignes de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return get_ligne_commande_by_id(ligne_commande_id, session)

@router.get("/commande/{commande_id}", response_model=List[LigneCommandeRead])
def read_lignes_commandes_by_commande(commande_id: int, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Récupère toutes les lignes associées à une commande spécifique.

    Autorisation :
        - Admin et Employé uniquement.

    Args:
        commande_id (int): ID de la commande.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        List[LigneCommandeRead]: Liste des lignes de commande pour la commande spécifiée.
    
    Raises:
        HTTPException: Si l'utilisateur n'a pas le rôle admin ou employé.
    """
    # Seuls admin et employé peuvent voir les lignes de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return get_lignes_commandes_by_commande(commande_id, session)

@router.post("/", response_model=CommandeWithLignes)
def add_ligne_commande(ligne_commande: LigneCommandeCreate, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Crée une nouvelle ligne de commande.

    Autorisation :
        - Admin et Employé uniquement.

    Args:
        ligne_commande (LigneCommandeCreate): Données de la ligne de commande à créer.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        CommandeWithLignes: Commande avec ses lignes mises à jour après création.
    
    Raises:
        HTTPException: Si l'utilisateur n'a pas le rôle admin ou employé.
    """
    # Seuls admin et employé peuvent créer une ligne de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    
    return create_ligne_commande(ligne_commande, session)

@router.put("/{ligne_commande_id}", response_model=CommandeWithLignes)
def modify_ligne_commande(ligne_commande_id: int, ligne_commande: LigneCommandeUpdate, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Met à jour une ligne de commande existante.

    Autorisation :
        - Admin et Employé uniquement.

    Args:
        ligne_commande_id (int): ID de la ligne de commande à mettre à jour.
        ligne_commande (LigneCommandeUpdate): Données mises à jour de la ligne de commande.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        CommandeWithLignes: Commande avec ses lignes mises à jour après modification.
    
    Raises:
        HTTPException: Si l'utilisateur n'a pas le rôle admin ou employé.
    """
    # Seuls admin et employé peuvent modifier une ligne de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

    return update_ligne_commande(ligne_commande_id, ligne_commande, session)

@router.delete("/{ligne_commande_id}")
def drop_ligne_commande(ligne_commande_id: int, session: Session = Depends(get_session), current_user: Utilisateur = Depends(get_current_user)):
    """
    Supprime une ligne de commande existante.

    Autorisation :
        - Admin et Employé uniquement.

    Args:
        ligne_commande_id (int): ID de la ligne de commande à supprimer.
        session (Session): Session de base de données SQLModel.
        current_user (Utilisateur): Utilisateur authentifié.

    Returns:
        dict: Message de confirmation de suppression.
    
    Raises:
        HTTPException: Si l'utilisateur n'a pas le rôle admin ou employé.
    """
    # Seuls admin et employé peuvent supprimer une ligne de commabde
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

    return delete_ligne_commande(ligne_commande_id, session)