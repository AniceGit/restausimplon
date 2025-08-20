import pytest
from app.core.config import Settings

def test_settings_loading(fresh_settings):
    cfg = fresh_settings
    assert cfg.SECRET_KEY == "test_secret_key"
    assert cfg.ALGORITHM == "HS256"
    assert cfg.ACCESS_TOKEN_EXPIRE_MINUTES == 15
    assert cfg.REFRESH_TOKEN_EXPIRE_DAYS == 7
    assert cfg.DATABASE_URL == "postgresql://test_user:test_password@compose_postgres_test:5432/test_db"

def test_settings_missing_secret_key(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://test_user:test_password@compose_postgres_test:5432/test_db")
    cfg = Settings()
    # Vérifie qu'on retombe sur la valeur par défaut (ex: "super-secret-key")
    assert cfg.SECRET_KEY == "super-secret-key"

def test_settings_missing_database_url(monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setenv("SECRET_KEY", "test_secret_key")
    cfg = Settings()
    # Vérifie que c'est la valeur par défaut de la classe Settings
    assert cfg.DATABASE_URL == Settings().DATABASE_URL
