from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.schemas.auth import TokenData
from fastapi.security import OAuth2PasswordBearer

#récupération utilisateur connecté et gestion du rôle (autorisations)
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.utilisateur import Utilisateur
from app.core.config import settings  # import de la config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

#Vérification du l'état du token access
def verify_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise ValueError("Missing subject")
        return TokenData(email=email)
    except JWTError:
        raise


# -----récupération utilisateur connecté-----
def get_current_user(token: str = Depends(oauth2_scheme),session: Session = Depends(get_session)) -> Utilisateur:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token invalide")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

    statement = select(Utilisateur).where(Utilisateur.email == email)
    user = session.exec(statement).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user

# ----vérification rôle admin----
def require_admin(current_user: Utilisateur = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Accès réservé aux administrateurs.")
    return current_user
