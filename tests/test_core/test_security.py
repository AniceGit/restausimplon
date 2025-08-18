import pytest
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
    require_admin,
)
from app.models.utilisateur import Utilisateur
from app.core import config  # pour récupérer le singleton settings utilisé en signature

@pytest.fixture
def test_password():
    return "mon_mot_de_passe_securise"

@pytest.fixture
def test_user():
    return Utilisateur(
        email="test@example.com",
        nom="Test",
        prenom="User",
        telephone=  "0123456789",  
        role="admin",
        id=1,
        motdepasse="hashed_password",
        is_active=True,
        adresse="1 rue du test",  # champ NOT NULL obligatoire
    )

def test_verify_password_and_hash(test_password):
    hashed = get_password_hash(test_password)
    assert verify_password(test_password, hashed)
    assert not verify_password("mauvais_mdp", hashed)

def test_create_access_token():
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    token_data = verify_token(token)   # <-- utilise la logique réelle de l'app
    assert token_data.email == "test@example.com"

def test_create_refresh_token():
    data = {"sub": "test@example.com"}
    token = create_refresh_token(data)
    token_data = verify_token(token)
    assert token_data.email == "test@example.com"

def test_verify_token():
    token = create_access_token({"sub": "test@example.com"})
    token_data = verify_token(token)
    assert token_data.email == "test@example.com"

def test_verify_token_invalid():
    with pytest.raises((JWTError, HTTPException)):
        verify_token("invalid_token")

def test_get_current_user(session, test_user):
    session.add(test_user)
    session.commit()
    token = create_access_token({"sub": test_user.email})
    user = get_current_user(token, session)
    assert user.email == test_user.email

def test_get_current_user_invalid_token(session):
    with pytest.raises(HTTPException) as exc:
        get_current_user("invalid_token", session)
    assert exc.value.status_code == 401

def test_get_current_user_not_found(session):
    token = create_access_token({"sub": "unknown@example.com"})
    with pytest.raises(HTTPException) as exc:
        get_current_user(token, session)
    assert exc.value.status_code == 404

def test_require_admin(session, test_user):
    session.add(test_user)
    session.commit()
    token = create_access_token({"sub": test_user.email})
    user = get_current_user(token, session)
    admin = require_admin(user)
    assert admin.role == "admin"

def test_require_admin_not_admin(session, test_user):
    test_user.role = "client"  # rôle valide qui n'est pas admin
    session.add(test_user)
    session.commit()
    token = create_access_token({"sub": test_user.email})
    user = get_current_user(token, session)
    with pytest.raises(HTTPException) as exc:
        require_admin(user)
    assert exc.value.status_code == status.HTTP_403_FORBIDDEN
