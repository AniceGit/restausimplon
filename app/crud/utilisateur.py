from sqlmodel import Session, select
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate
from app.core.security import get_password_hash
from typing import List, Optional
from fastapi import HTTPException, status
from app.core.security import verify_password, get_password_hash


def get_all_utilisateurs(session: Session) -> List[Utilisateur]:
    """
    Récupère tous les utilisateurs actifs.

    Args:
        session (Session): La session SQLModel pour interagir avec la base de données.

    Returns:
        List[Utilisateur]: La liste des utilisateurs actifs.
    """
    statement = select(Utilisateur).where(Utilisateur.is_active == True)
    return session.exec(statement).all()


def get_utilisateur_by_id(utilisateur_id: int, session: Session) -> Optional[Utilisateur]:
    """
    Récupère un utilisateur par son identifiant unique.

    Args:
        utilisateur_id (int): L’identifiant de l’utilisateur.
        session (Session): La session SQLModel pour interagir avec la base.

    Returns:
        Utilisateur | None: L’utilisateur correspondant à l’ID.

    Raises:
        HTTPException (404): Si aucun utilisateur n’existe avec cet identifiant.
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur


def create_utilisateur(session: Session, utilisateur_data: UtilisateurCreate) -> Utilisateur:
    """
    Crée un nouvel utilisateur après avoir vérifié l’unicité de son email.
    Le mot de passe est automatiquement hashé avant l’insertion en base.

    Args:
        session (Session): La session SQLModel pour interagir avec la base.
        utilisateur_data (UtilisateurCreate): Les données de l’utilisateur à créer.

    Returns:
        Utilisateur: Le nouvel utilisateur inséré en base.

    Raises:
        HTTPException (400): Si un utilisateur avec le même email existe déjà.
    """
    # Vérifie si l'email est déjà utilisé
    statement = select(Utilisateur).where(Utilisateur.email == utilisateur_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà."
        )

    utilisateur = Utilisateur.model_validate(utilisateur_data)
    utilisateur.motdepasse = get_password_hash(utilisateur_data.motdepasse)

    session.add(utilisateur)
    session.commit()
    session.refresh(utilisateur)
    return utilisateur


def update_utilisateur(utilisateur_id: int, utilisateur_data: UtilisateurUpdate, session: Session) -> Utilisateur:
    """
    Met à jour les informations d’un utilisateur existant.

    Args:
        utilisateur_id (int): L’identifiant de l’utilisateur à mettre à jour.
        utilisateur_data (UtilisateurUpdate): Les nouvelles données (champs optionnels).
        session (Session): La session SQLModel pour interagir avec la base.

    Returns:
        Utilisateur: L’utilisateur mis à jour.

    Raises:
        HTTPException (404): Si l’utilisateur n’existe pas.
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    for key, value in utilisateur_data.model_dump(exclude_unset=True).items():
        setattr(utilisateur, key, value)

    session.commit()
    session.refresh(utilisateur)
    return utilisateur


def delete_utilisateur(utilisateur_id: int, session: Session) -> Utilisateur:
    """
    Désactive (soft delete) un utilisateur en mettant son statut `is_active` à False.

    Args:
        utilisateur_id (int): L’identifiant de l’utilisateur à désactiver.
        session (Session): La session SQLModel pour interagir avec la base.

    Returns:
        Utilisateur: L’utilisateur désactivé.

    Raises:
        HTTPException (404): Si l’utilisateur n’existe pas.
    """
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    utilisateur.is_active = False
    session.commit()
    session.refresh(utilisateur)
    return utilisateur
