from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from haru.story import story_router
from haru.user import user_router
from haru.utils.db import init_database


def init_middlewares(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_routers(app: FastAPI):
    app.include_router(story_router)
    app.include_router(user_router)


def create_app() -> FastAPI:
    app = FastAPI()

    init_middlewares(app)
    init_routers(app)
    init_database()

    return app


app = create_app()
