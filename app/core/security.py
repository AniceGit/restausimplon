from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.schemas.auth import TokenData
from fastapi.security import OAuth2PasswordBearer

# récupération utilisateur connecté et gestion du rôle (autorisations)
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.utilisateur import Utilisateur
from app.core.config import settings  # import de la config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe en clair correspond à son empreinte bcrypt.

    Args:
        plain_password (str): Le mot de passe fourni par l'utilisateur.
        hashed_password (str): Le mot de passe déjà haché stocké en base.

    Returns:
        bool: True si les mots de passe correspondent, sinon False.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Génère un hash bcrypt à partir d'un mot de passe en clair.

    Args:
        password (str): Le mot de passe en clair.

    Returns:
        str: Le mot de passe haché.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token d'accès JWT avec une date d’expiration.

    Args:
        data (dict): Les données à encoder dans le token (ex: {"sub": email}).
        expires_delta (Optional[timedelta]): Durée personnalisée avant expiration.
                                             Par défaut : 15 minutes.

    Returns:
        str: Le token JWT encodé.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un refresh token JWT avec une date d’expiration.

    Args:
        data (dict): Les données à encoder dans le token (ex: {"sub": email}).
        expires_delta (Optional[timedelta]): Durée personnalisée avant expiration.
                                             Par défaut : REFRESH_TOKEN_EXPIRE_DAYS.

    Returns:
        str: Le refresh token JWT encodé.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> TokenData:
    """
    Vérifie la validité d’un token JWT d’accès et en extrait l'email (sub).

    Args:
        token (str): Le token JWT fourni par le client.

    Returns:
        TokenData: Objet contenant l'email extrait du token.

    Raises:
        ValueError: Si le token ne contient pas de champ `sub`.
        JWTError: Si le token est invalide ou expiré.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise ValueError("Missing subject")
        return TokenData(email=email)
    except JWTError:
        raise


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> Utilisateur:
    """
    Récupère l’utilisateur actuellement authentifié à partir du token JWT.

    Args:
        token (str): Le token JWT fourni par l'utilisateur (Bearer token).
        session (Session): Session SQLModel pour interagir avec la base.

    Returns:
        Utilisateur: L’objet utilisateur correspondant au token.

    Raises:
        HTTPException 401: Si le token est invalide ou expiré.
        HTTPException 404: Si aucun utilisateur ne correspond à l'email.
    """
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


def require_admin(current_user: Utilisateur = Depends(get_current_user)) -> Utilisateur:
    """
    Vérifie que l’utilisateur connecté est un administrateur.

    Args:
        current_user (Utilisateur): Utilisateur connecté, injecté par dépendance.

    Returns:
        Utilisateur: L’utilisateur validé comme administrateur.

    Raises:
        HTTPException 403: Si l’utilisateur n’a pas le rôle "admin".
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Accès réservé aux administrateurs."
        )
    return current_user
