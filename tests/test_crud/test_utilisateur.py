import pytest
from sqlmodel import Session
from fastapi import HTTPException, status
from app.models.utilisateur import Utilisateur
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurUpdate
from app.crud.utilisateur import (
    get_all_utilisateurs,
    get_utilisateur_by_id,
    create_utilisateur,
    update_utilisateur,
    delete_utilisateur,
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

def test_create_utilisateur_email_duplique(session: Session, utilisateur_data):
    create_utilisateur(session, utilisateur_data)  # premier utilisateur
    with pytest.raises(HTTPException) as exc:
        create_utilisateur(session, utilisateur_data)  # doublon
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST

def test_get_utilisateur_by_id(session: Session, utilisateur_data):
    utilisateur = create_utilisateur(session, utilisateur_data)
    fetched = get_utilisateur_by_id(utilisateur.id, session)
    assert fetched.email == utilisateur.email

def test_get_utilisateur_by_id_inexistant(session: Session):
    with pytest.raises(HTTPException) as exc:
        get_utilisateur_by_id(999, session)
    assert exc.value.status_code == 404

def test_get_all_utilisateurs(session: Session, utilisateur_data):
    u1 = create_utilisateur(session, utilisateur_data)
    u2 = create_utilisateur(session, utilisateur_data.copy(update={"email": "autre@example.com"}))
    utilisateurs = get_all_utilisateurs(session)
    assert len(utilisateurs) == 2
    assert all(u.is_active for u in utilisateurs)

def test_update_utilisateur(session: Session, utilisateur_data):
    utilisateur = create_utilisateur(session, utilisateur_data)
    update_data = UtilisateurUpdate(nom="Durand", prenom="Paul")
    utilisateur_modifie = update_utilisateur(utilisateur.id, update_data, session)
    assert utilisateur_modifie.nom == "Durand"
    assert utilisateur_modifie.prenom == "Paul"

def test_update_utilisateur_inexistant(session: Session):
    update_data = UtilisateurUpdate(nom="Fantome")
    with pytest.raises(HTTPException) as exc:
        update_utilisateur(999, update_data, session)
    assert exc.value.status_code == 404

def test_delete_utilisateur(session: Session, utilisateur_data):
    utilisateur = create_utilisateur(session, utilisateur_data)
    utilisateur_supprime = delete_utilisateur(utilisateur.id, session)
    assert utilisateur_supprime.is_active is False
    # Et il n'apparait plus dans get_all
    utilisateurs = get_all_utilisateurs(session)
    assert utilisateur_supprime not in utilisateurs

def test_delete_utilisateur_inexistant(session: Session):
    with pytest.raises(HTTPException) as exc:
        delete_utilisateur(999, session)
    assert exc.value.status_code == 404
