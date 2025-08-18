import pytest
from sqlmodel import Session, create_engine
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate
from app.crud.utilisateur import (
    get_all_utilisateurs,
    get_utilisateur_by_id,
    create_utilisateur,
    update_utilisateur,
    delete_utilisateur
)

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    return Session()

def test_create_utilisateur(session):
    utilisateur_data = UtilisateurCreate(
        email="test@example.com",
        motdepasse="password123",
        nom="Test",
        prenom="User"
    )
    utilisateur = create_utilisateur(session, utilisateur_data)
    assert utilisateur.email == "test@example.com"
    assert utilisateur.is_active is True

def test_get_utilisateur_by_id(session):
    utilisateur_data = UtilisateurCreate(
        email="test@example.com",
        motdepasse="password123",
        nom="Test",
        prenom="User"
    )
    utilisateur = create_utilisateur(session, utilisateur_data)
    fetched = get_utilisateur_by_id(utilisateur.id, session)
    assert fetched.email == "test@example.com"

# Ajoute d'autres tests pour update_utilisateur, delete_utilisateur, etc.
