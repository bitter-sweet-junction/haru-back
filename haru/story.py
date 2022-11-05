from fastapi import APIRouter, Depends

from haru.utils.auth import get_current_user
from haru.model import User

story_router = APIRouter()


@story_router.get("/stories")
def get_stories(user: User = Depends(get_current_user)):
    pass


@story_router.post("/stories")
def post_stories(suer: User = Depends(get_current_user)):
    pass


@story_router.get("/stories/<story_id>")
def get_story(story_id: int, user: User = Depends(get_current_user)):
    pass


@story_router.delete("/stories/<story_id>")
def delete_story(story_id: int, user: User = Depends(get_current_user)):
    pass
