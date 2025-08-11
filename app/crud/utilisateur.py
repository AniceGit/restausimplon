from sqlmodel import Session, select
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate
from app.core.security import get_password_hash
from typing import List
from typing import Optional
from fastapi import HTTPException, status
from app.core.security import verify_password, get_password_hash

def get_all_utilisateurs(session: Session) -> List[Utilisateur]:
    statement = select(Utilisateur).where(Utilisateur.is_active == True)
    return session.exec(statement).all()

def get_utilisateur_by_id(utilisateur_id: int, session: Session) -> Optional[Utilisateur]:
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

def create_utilisateur(session: Session, utilisateur_data: UtilisateurCreate) -> Utilisateur:
    # Vérifie si l'utilisateur existe déjà
    statement = select(Utilisateur).where(Utilisateur.email == utilisateur_data.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un utilisateur avec cet email existe déjà."
        )

    # Crée l'utilisateur
    utilisateur = Utilisateur.model_validate(utilisateur_data)
    utilisateur.motdepasse = get_password_hash(utilisateur_data.motdepasse)
    session.add(utilisateur)
    session.commit()
    session.refresh(utilisateur)
    return utilisateur

def update_utilisateur(utilisateur_id: int, utilisateur_data: UtilisateurUpdate, session: Session) -> Utilisateur:
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    for key, value in utilisateur_data.model_dump(exclude_unset=True).items():
        setattr(utilisateur, key, value)

    session.commit()
    session.refresh(utilisateur)
    return utilisateur

def delete_utilisateur(utilisateur_id: int, session: Session) -> Utilisateur:
    utilisateur = session.get(Utilisateur, utilisateur_id)
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    utilisateur.is_active = False
    session.commit()
    session.refresh(utilisateur)
    return utilisateur