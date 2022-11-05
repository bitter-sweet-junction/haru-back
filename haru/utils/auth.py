import os
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from haru.utils.db import get_database
from haru.model import User

JWT_TOKEN = os.environ.get("HARU_JWT_TOKEN")
oauth2 = OAuth2PasswordBearer(tokenUrl="/authorize/google")


def create_token(user_id: str) -> str:
    return jwt.encode({"user_id": user_id}, JWT_TOKEN, algorithm="HS256")


def get_current_user(token: str = Depends(oauth2)) -> User:
    user = None
    try:
        result = jwt.decode(token, JWT_TOKEN, algorithms="HS256")
        user_id = result.get("user_id")
        user = get_database().user.find_one({"_id": user_id})
    except:
        pass

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Auth failed",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
