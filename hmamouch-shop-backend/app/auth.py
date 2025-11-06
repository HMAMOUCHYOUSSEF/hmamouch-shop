from datetime import datetime, timedelta
from jose import JWTError, jwt #for JWT -- JSON WEB TOKEN
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer # the security man = bounder
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
import os

SECRET_KEY = os.getenv("SECRET_KEY") # my signiture -- to make the acces token valid
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") # where the token is taken.
# verfiy if the password is correct
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
# hashing the password -- hashing is one directionnal whereas crypting is bidirectionnal --
def get_password_hash(password):
    return pwd_context.hash(password)
# create card num for subscription -- expiration is import to prevent be used by a hacker or force rechecking the subscripton user again.
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    # here we will create the valide suscription cart num
    # create the access tocken code
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# how from an access token get the user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
