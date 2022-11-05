from fastapi import APIRouter, Depends

from haru.utils.auth import get_current_user
from haru.model import User

user_router = APIRouter()


@user_router.post("/authorize/google")
def authorize():
    pass


@user_router.get("/user")
def get_user(user: User = Depends(get_current_user)):
    pass
