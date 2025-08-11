from fastapi import APIRouter, Depends,HTTPException, status
from sqlmodel import Session
from typing import List
from datetime import datetime

from app.database import get_session

from app.schemas.commande import CommandeRead, CommandeCreate, CommandeUpdate, CommandeWithLignes
from app.schemas.ligne_de_commande import LigneCommandeCreateWithoutCommandId
from app.crud.commande import get_all_commandes, get_commande_by_id, update_commande, delete_commande
from app.services.commande import create_commande_with_lignes_and_utilisateur, get_commandes_by_utilisateur_id, get_commandes_by_date

#gestion des autorisations : 
from app.core.security import get_current_user
from app.models.utilisateur import Utilisateur

router = APIRouter(prefix="/commandes", tags=["Commandes"])

#autorisation de tous lire si admin ou employé
@router.get("/", response_model=List[CommandeWithLignes])
def read_commandes(
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    # Admin et Employé peuvent voir toutes les commandes
    if current_user.role in ("admin", "employe"):
        return get_all_commandes(session)
    else:
        # Client ne peut voir que ses commandes
        return get_commandes_by_utilisateur_id(current_user.id, session)

#autorisation de lire les commande d'un id commande précis seulement pour les admin et employés
#autorisation pour les clients si c'est leur propre commande
@router.get("/{commande_id}", response_model=CommandeWithLignes)
def read_commande_by_id(
    commande_id: int,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    commande = get_commande_by_id(commande_id, session)
    if commande is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")

    # Admin et Employé peuvent voir n'importe quelle commande
    if current_user.role in ("admin", "employe"):
        return commande
    # Client ne peut voir que ses commandes
    if commande.utilisateur_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return commande

#récupère la liste des commandes d'un utilisateur précis
#autorisé pour tous les utilisateurs si fait par un admin ou employé
#autorisé pour un client seulement sur ses propres commandes
@router.get("/utilisateur/{utilisateur_id}", response_model=List[CommandeWithLignes])
def read_commande_by_utilisateur_id(
    utilisateur_id: int,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    # Admin et Employé peuvent voir commandes de n'importe quel utilisateur
    if current_user.role in ("admin", "employe"):
        return get_commandes_by_utilisateur_id(utilisateur_id, session)

    # Client ne peut voir que ses commandes
    if utilisateur_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")
    return get_commandes_by_utilisateur_id(utilisateur_id, session)

#récupère la liste des commandes d'une date précise
#autorisé pour toutes les commandes si fait par un admin ou employé
#autorisé pour un client seulement sur ses propres commandes
@router.get("/date/{date_commande}", response_model=List[CommandeWithLignes])
def read_commande_by_date(
    date_commande: datetime,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    commandes = get_commandes_by_date(date_commande, session)
    if commandes is None:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    # Seuls Admin et Employé peuvent accéder à cette route
    if current_user.role in ("admin", "employe"):
        return commandes
    # Client ne peut voir que ses commandes
    # Client voit uniquement ses commandes filtrées sur la date
    commandes_client = [c for c in commandes if c.utilisateur_id == current_user.id]
    if not commandes_client:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé ou aucune commande trouvée")
    return commandes_client

#admin et employé peuvent ajouter commande pour tous les utilisateurs
#client ne peut ajouter une commande que pour lui même
@router.post("/lignes/", response_model=CommandeWithLignes)
def add_commande_with_lignes_and_utilisateur(
    commande: CommandeCreate,
    lignes_commande: List[LigneCommandeCreateWithoutCommandId],
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    # Admin et Employé peuvent créer une commande pour n'importe quel client
    # Client peut créer une commande pour lui-même uniquement
    if current_user.role == "client" and commande.utilisateur_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

    return create_commande_with_lignes_and_utilisateur(commande, lignes_commande, session)


@router.put("/{commande_id}", response_model=CommandeWithLignes)
def modify_commande(
    commande_id: int,
    commande: CommandeUpdate,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    # Seuls admin et employé peuvent modifier le statut ou contenu
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

    return update_commande(commande_id, commande, session)

@router.delete("/{commande_id}")
def drop_commande(
    commande_id: int,
    session: Session = Depends(get_session),
    current_user: Utilisateur = Depends(get_current_user)
):
    # Seuls admin et employé peuvent supprimer une commande
    if current_user.role not in ("admin", "employe"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Accès refusé")

    return delete_commande(commande_id, session)