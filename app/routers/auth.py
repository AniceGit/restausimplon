from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select
from datetime import timedelta

from app.models.utilisateur import Utilisateur, RoleEnum
from app.schemas.auth import Token
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurRead
from app.database import get_session
from app.core.security import get_password_hash,verify_password,create_access_token,create_refresh_token,ACCESS_TOKEN_EXPIRE_MINUTES, verify_token, oauth2_scheme

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UtilisateurRead)
def register(utilisateur_data: UtilisateurCreate,session: Session = Depends(get_session)):
    existing_user = session.exec(select(Utilisateur).where(Utilisateur.email == utilisateur_data.email)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email déjà enregistré")

    user = Utilisateur(
        email=utilisateur_data.email,
        nom=utilisateur_data.nom,
        prenom=utilisateur_data.prenom,
        adresse=utilisateur_data.adresse,
        telephone=utilisateur_data.telephone,
        motdepasse=get_password_hash(utilisateur_data.motdepasse),
        role=utilisateur_data.role,
        is_active=utilisateur_data.is_active
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),session: Session = Depends(get_session)):

    user = session.exec(select(Utilisateur).where(Utilisateur.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.motdepasse):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    access_token = create_access_token(data={"sub": user.email},expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.email})

    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )

@router.get("/verify-token")
def verify_token_route(token: str = Depends(oauth2_scheme)):
    try:
        print(f"Token reçu: {token}")
        token_data = verify_token(token)  # Vérifie signature, expiration, "sub"
        return {
            "message": "Token valide ✅",
            "email": token_data.email
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

