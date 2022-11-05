import os
import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

JWT_TOKEN = os.environ.get("HARU_JWT_TOKEN")
oauth2 = OAuth2PasswordBearer(tokenUrl="/authorize/google")


def create_token(user_id: str) -> str:
    return jwt.encode({"user_id": user_id}, JWT_TOKEN, algorithm="HS256")


def get_current_user_id(token: str = Depends(oauth2)) -> str:
    try:
        result = jwt.decode(token, JWT_TOKEN, algorithms="HS256")
        return result.get("user_id")
    except:
        pass

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Auth failed",
        headers={"WWW-Authenticate": "Bearer"},
    )

