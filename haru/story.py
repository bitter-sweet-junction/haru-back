from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import ASCENDING

from haru.model import Story, User
from haru.utils.auth import get_current_user
from haru.utils.db import get_database

story_router = APIRouter()


def _story_to_dto(story: Story) -> dict:
    s = dict(**story)
    s["id"] = s.pop("_id")
    s.pop("user_id")
    return s


@story_router.get("/stories")
def get_stories(user: User = Depends(get_current_user)):
    stories = get_database().story.find({"user_id": user["_id"]}).sort("createTime", ASCENDING)
    return [_story_to_dto(story) for story in stories]


@story_router.post("/stories")
def post_stories(user: User = Depends(get_current_user)):
    pass


@story_router.get("/stories/<story_id>")
def get_story(story_id: int, user: User = Depends(get_current_user)):
    story: Story = get_database().story.find({"story_id": story_id, "user_id": user["_id"]})
    if story is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="story not found")

    return {"story": _story_to_dto(story)}


@story_router.delete("/stories/<story_id>")
def delete_story(story_id: int, user: User = Depends(get_current_user)):
    story: Story = get_database().story.find_one_and_delete({"story_id": story_id, "user_id": user["_id"]})
    if story is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="story not found")

    return {"story": {"id": story["_id"]}}
