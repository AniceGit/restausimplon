import pytest
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from sqlmodel import Session, select
from unittest.mock import MagicMock, patch
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
    require_admin,
)
from app.schemas.auth import TokenData
from app.models.utilisateur import Utilisateur

# Fixture pour un mot de passe de test
@pytest.fixture
def test_password():
    return "mon_mot_de_passe_securise"

# Fixture pour un utilisateur de test
@pytest.fixture
def test_user():
    return Utilisateur(email="test@example.com", role="admin", id=1)

# Fixture pour une session mockée
@pytest.fixture
def mock_session(test_user):
    session = MagicMock(spec=Session)
    session.exec.return_value.first.return_value = test_user
    return session

# Fixture pour une config mockée
@pytest.fixture
def mock_settings():
    with patch("app.core.security.settings") as mock_settings:
        mock_settings.SECRET_KEY = "secret"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.REFRESH_TOKEN_EXPIRE_DAYS = 7
        yield mock_settings

# Test pour verify_password et get_password_hash
def test_verify_password_and_hash(test_password):
    hashed_password = get_password_hash(test_password)
    assert verify_password(test_password, hashed_password) is True
    assert verify_password("mauvais_mot_de_passe", hashed_password) is False

# Test pour create_access_token
def test_create_access_token(mock_settings):
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)
    payload = jwt.decode(token, mock_settings.SECRET_KEY, algorithms=[mock_settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload

# Test pour create_refresh_token
def test_create_refresh_token(mock_settings):
    data = {"sub": "test@example.com"}
    token = create_refresh_token(data)
    assert isinstance(token, str)
    payload = jwt.decode(token, mock_settings.SECRET_KEY, algorithms=[mock_settings.ALGORITHM])
    assert payload["sub"] == "test@example.com"
    assert "exp" in payload

# Test pour verify_token
def test_verify_token(mock_settings):
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    token_data = verify_token(token)
    assert token_data.email == "test@example.com"

# Test pour verify_token avec un token invalide
def test_verify_token_invalid(mock_settings):
    with pytest.raises(JWTError):
        verify_token("invalid_token")

# Test pour get_current_user
def test_get_current_user(mock_settings, mock_session, test_user):
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    user = get_current_user(token, mock_session)
    assert user.email == "test@example.com"

# Test pour get_current_user avec un token invalide
def test_get_current_user_invalid_token(mock_settings, mock_session):
    with pytest.raises(HTTPException) as excinfo:
        get_current_user("invalid_token", mock_session)
    assert excinfo.value.status_code == 401

# Test pour get_current_user avec un utilisateur introuvable
def test_get_current_user_not_found(mock_settings, mock_session):
    mock_session.exec.return_value.first.return_value = None
    data = {"sub": "unknown@example.com"}
    token = create_access_token(data)
    with pytest.raises(HTTPException) as excinfo:
        get_current_user(token, mock_session)
    assert excinfo.value.status_code == 404

# Test pour require_admin
def test_require_admin(mock_settings, mock_session, test_user):
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    current_user = get_current_user(token, mock_session)
    admin_user = require_admin(current_user)
    assert admin_user.role == "admin"

# Test pour require_admin avec un utilisateur non-admin
def test_require_admin_not_admin(mock_settings, mock_session, test_user):
    test_user.role = "user"
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    current_user = get_current_user(token, mock_session)
    with pytest.raises(HTTPException) as excinfo:
        require_admin(current_user)
    assert excinfo.value.status_code == status.HTTP_403_FORBIDDEN
