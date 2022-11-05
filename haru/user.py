from fastapi import APIRouter, Depends

from haru.model import User
from haru.utils.auth import get_current_user

user_router = APIRouter()


@user_router.post("/authorize/google")
def authorize():
    pass


@user_router.get("/user")
def get_user(user: User = Depends(get_current_user)):
    pass
