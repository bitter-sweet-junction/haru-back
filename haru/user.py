from fastapi import APIRouter

user_router = APIRouter()


@user_router.post("/authorize/google")
def authorize():
    pass


@user_router.get("/user")
def get_user():
    pass
