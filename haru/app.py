from fastapi import FastAPI

from haru.story import story_router
from haru.user import user_router
from haru.utils.db import init_database


def init_routers(app: FastAPI):
    app.include_router(story_router)
    app.include_router(user_router)


def create_app() -> FastAPI:
    app = FastAPI()

    init_routers(app)
    init_database()

    return app


app = create_app()
