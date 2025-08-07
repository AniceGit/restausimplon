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

@router.post("/login", response_model=Token)
async def login_for_access_token(
    email: str = Form(...),
    motdepasse: str = Form(...),
    session: Session = Depends(get_session)
):
    user = session.exec(select(Utilisateur).where(Utilisateur.email == email)).first()
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
    

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}



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