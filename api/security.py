from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext

from typing import Annotated
from pydantic import BaseModel

SECRET_KEY = "ed14f4d0c23c0a176274d0994ed6c5cb0dd9722137d01351744b631a16c9ecbc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    
class User(BaseModel):
    username: str
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

EXCEPTIONS = {
    "wrongUsernamePassword": {
        "status_code": status.HTTP_401_UNAUTHORIZED,
        "detail": "Incorrect username or password",
        "headers": {"WWW-Authenticate": "Bearer"},
    },
    "credentialsError": {
        "status_code" :status.HTTP_401_UNAUTHORIZED,
        "detail": "Could not validate credentials",
        "headers": {"WWW-Authenticate": "Bearer"},
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "june": {
        "username": "june",
        "hashed_password": "$2a$12$Suv2uJW7e6aJexs4R/6agexH8WYhA3OLJwddrlpqkbK64gUKEaXqO",
        "disabled": False,
    }
}

def verifyPassword(plaintext, hash):
    return pwd_context.verify(plaintext, hash)

def getPasswordHash(plaintext: str):
    return pwd_context.hash(plaintext)

def getUser(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticateUser(fake_db, username: str, password: str):
    user = getUser(fake_db, username)
    if not user:
        return False
    if not verifyPassword(password, user.hashed_password):
        return False
    return user

def createAccessToken(data: dict, expirationDelta: timedelta | None = None):
    toEncode = data.copy()

    if expirationDelta:
        expire = datetime.now(timezone.utc) + expirationDelta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    toEncode.update({"exp": expire})
    encoded_jwt = jwt.encode(toEncode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def authenticateWithAccessToken(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(**EXCEPTIONS["credentialsError"])
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise HTTPException(**EXCEPTIONS["credentialsError"])
    user = get_user(fake_users_db, username=token_data.username) # type: ignore
    if user is None:
        raise HTTPException(**EXCEPTIONS["credentialsError"])
    return user
