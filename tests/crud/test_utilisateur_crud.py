from sqlmodel import SQLModel, Session, create_engine
from app.models.utilisateur import Utilisateur
from app.crud.utilisateur import create_utilisateur, get_all_utilisateurs
from app.schemas.utilisateur import UtilisateurCreate

import os

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)

def setup_database():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

def test_create_and_get_utilisateur():
    setup_database()
    with Session(engine) as session:
        user_data = UtilisateurCreate(
            nom="TestNom",
            prenom="TestPrenom",
            adresse="123 rue Test",
            telephone="0123456789",
            email="test@example.com",
            motdepasse="password123",
            role="client",
            is_active=True
        )

        user = create_utilisateur(session, user_data)
        assert user.id is not None

        utilisateurs = get_all_utilisateurs(session)
        assert len(utilisateurs) == 1
        assert utilisateurs[0].email == "test@example.com"
