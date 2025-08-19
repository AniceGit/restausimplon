import pytest

from importlib import reload
import warnings
from app.models.utilisateur import Utilisateur

# Crée une base SQLite éphémère pour chaque test
@pytest.fixture
def session():
    from sqlmodel import Session, create_engine
    from app.models.utilisateur import SQLModel 
    engine = create_engine("sqlite:///:memory:", echo=False, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

# Donne un Settings réinitialisé après patch des envs
@pytest.fixture
def fresh_settings(monkeypatch):
    # valeurs par défaut (écrasables dans les tests si besoin)
    monkeypatch.setenv("SECRET_KEY", "test_secret_key")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    monkeypatch.setenv("REFRESH_TOKEN_EXPIRE_DAYS", "7")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("POSTGRES_DATA_PATH", "/tmp/data")
    monkeypatch.setenv("POSTGRES_CONFIG_PATH", "/tmp/config")
    monkeypatch.setenv("POSTGRES_LOGS_PATH", "/tmp/logs")
    monkeypatch.setenv("POSTGRES_BACKUPS_PATH", "/tmp/backups")
    monkeypatch.setenv("BACKUP_SCHEDULE", "0 0 * * *")
    monkeypatch.setenv("BACKUP_RETENTION_DAYS", "7")

    import app.core.config as config
    reload(config)  # re-crée settings
    return config.Settings()  # retourne une instance, pas le singleton

def pytest_configure():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
