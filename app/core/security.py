from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "secret-key-for-jwt"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> bool:
    try:
        # Décodez et vérifiez le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Vérifiez que le token contient un subject (utilisateur)
        email : str = payload.get("sub")
        if email is None:
            print("Token verification failed: No subject found")
            return False
            
        # Si le token est valide, vous pouvez accéder aux claims
        expiration_timestamp = payload.get("exp")
        if expiration_timestamp:
            expiration_time = datetime.fromtimestamp(expiration_timestamp)
            print(f"Token expires at: {expiration_time}")
            
            # Vérifiez que le token n'est pas expiré
            if datetime.utcnow() > expiration_time:
                print("Token verification failed: Token has expired")
                return False
                
        return True
        
    except JWTError as e:
        # Gestion des erreurs : token invalide ou expiré
        print(f"Token verification failed: {e}")
        return False
