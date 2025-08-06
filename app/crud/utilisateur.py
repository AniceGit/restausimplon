from sqlmodel import Session, select
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurRead
from typing import List
from typing import Optional
from fastapi import HTTPException, status

def get_all_utilisateurs(session: Session) -> List[Utilisateur]:
    statement = select(Utilisateur)
    return session.exec(statement).all()

def get_utilisateur_by_id(utilisateur_id: int, session: Session) -> Optional[Utilisateur]:
    return session.get(Utilisateur, utilisateur_id)

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
    session.add(utilisateur)
    session.commit()
    session.refresh(utilisateur)
    return utilisateur

