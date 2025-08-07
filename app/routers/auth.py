from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from datetime import timedelta
from app.database import get_session
from app.schemas.auth import Token
from app.schemas.utilisateur import UtilisateurRead, UtilisateurCreate
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    verify_token as verify_jwt_token  # Renommez l'import pour éviter le conflit
)
from app.models.utilisateur import Utilisateur

router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/register", response_model=UtilisateurRead)
def register_user(user: UtilisateurCreate, session: Session = Depends(get_session)):
    db_user = Utilisateur.model_validate(user)
    db_user.motdepasse = get_password_hash(user.motdepasse)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    email: str = Form(...),
    motdepasse: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(Utilisateur)).filter(Utilisateur.email == email).first()
    if not user or not verify_password(motdepasse, user.motdepasse):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    # Mettez à jour les tokens dans la base de données
    user.access_token = access_token
    user.refresh_token = refresh_token
    session.add(user)
    session.commit()
    
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/login", response_model=UtilisateurRead)
def login_utilisateur(email: str, motdepasse: str, session: Session = Depends(get_session)):
    # Recherchez l'utilisateur dans la base de données
    utilisateur = session.exec(select(Utilisateur).where(Utilisateur.email == email)).first()
    
    # Vérifiez si l'utilisateur existe et si le mot de passe est correct
    if not utilisateur or not verify_password(motdepasse, utilisateur.motdepasse):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return utilisateur

@router.get("/verify-token")
async def verify_token_endpoint(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    is_valid = verify_jwt_token(token)  # Utilisez la fonction renommée
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"message": "Token is valid"}