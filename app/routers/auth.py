from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select
from datetime import timedelta

from app.models.utilisateur import Utilisateur, RoleEnum
from app.schemas.auth import Token
from app.schemas.utilisateur import UtilisateurCreate, UtilisateurRead
from app.database import get_session
from app.core.security import get_password_hash,verify_password,create_access_token,create_refresh_token, verify_token, oauth2_scheme
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UtilisateurRead)
def register(utilisateur_data: UtilisateurCreate,session: Session = Depends(get_session)):
    """
    Enregistre un nouvel utilisateur.

    Vérifie que l'email fourni n'est pas déjà enregistré dans la base de données. 
    Si l'email est unique, crée l'utilisateur avec le mot de passe haché et l'ajoute à la base de données.

    Args:
        utilisateur_data (UtilisateurCreate): Données de l'utilisateur à créer.
        session (Session, optional): Session SQLModel pour la base de données. Par défaut, dépend de get_session.

    Raises:
        HTTPException: 
            - 400 si l'email est déjà utilisé.

    Returns:
        UtilisateurRead: L'utilisateur créé.
    """
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
    """
    Authentifie un utilisateur et retourne un access token et refresh token.

    Vérifie que l'email et le mot de passe fournis correspondent à un utilisateur existant.
    Génère un JWT d'accès et un JWT de rafraîchissement.

    Args:
        form_data (OAuth2PasswordRequestForm, optional): Formulaire contenant 'username' (email) et 'password'.
        session (Session, optional): Session SQLModel pour la base de données. Par défaut, dépend de get_session.

    Raises:
        HTTPException: 
            - 401 si les identifiants sont invalides.

    Returns:
        Token: Objet contenant l'access token, le type de token, et le refresh token.
    """

    user = session.exec(select(Utilisateur).where(Utilisateur.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.motdepasse):
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    access_token = create_access_token(data={"sub": user.email},expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(data={"sub": user.email})

    return Token(
        access_token=access_token,
        token_type="bearer",
        refresh_token=refresh_token
    )

@router.get("/verify-token")
def verify_token_route(token: str = Depends(oauth2_scheme)):
    """
    Vérifie la validité d'un token JWT.

    Cette route décode le token JWT fourni via OAuth2PasswordBearer et renvoie l'email de l'utilisateur si le token est valide.
    Si le token est invalide ou expiré, une exception est levée.

    Args:
        token (str, optional): Token JWT à vérifier. Par défaut, fourni par le header Authorization.

    Raises:
        HTTPException:
            - 401 si le token est invalide ou expiré.

    Returns:
        dict: Message de succès et email associé au token.
    """
    try:
        print(f"Token reçu: {token}")
        token_data = verify_token(token) 
        return {
            "message": "Token valide !",
            "email": token_data.email
        }
    except Exception:
        raise HTTPException(status_code=401, detail="Token invalide ou expiré")

