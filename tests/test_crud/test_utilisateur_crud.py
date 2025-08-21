import pytest
from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate
from app.crud.utilisateur import (
    create_utilisateur,
)

@pytest.fixture
def utilisateur_data():
    return UtilisateurCreate(
        email="test@example.com",
        nom="Dupont",
        prenom="Jean",
        adresse="10 rue de Paris, 75001 Paris",
        telephone="0612345678",
        motdepasse="password123",
        role="client",
        is_active=True
    )

def test_create_utilisateur(session: Session, utilisateur_data):
    utilisateur = create_utilisateur(session, utilisateur_data)
    assert utilisateur.id is not None
    assert utilisateur.email == "test@example.com"
    assert utilisateur.is_active is True
