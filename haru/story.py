import json
import time
import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from pymongo import ASCENDING

from haru.model import Story, User
from haru.utils.auth import get_current_user
from haru.utils.db import get_database
from haru.utils.gcp import publish_pubsub, upload_to_gcs

story_router = APIRouter()

REQUEST_GENERATE_IMAGE_PUBSUB_TOPIC = "haru-back-generate-image"


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
def post_stories(
    user: User = Depends(get_current_user),
    date: str = Form(),
    title: str = Form(),
    description: str | None = Form(default=None),
    weather: str | None = Form(default=None),
    feeling: str | None = Form(default=None),
    image: UploadFile | None = File(default=None),
):
    story_id = uuid.uuid4().hex
    image_url = None
    if image is not None:
        image_url = upload_to_gcs(
            bucket="haru-image-store", prefix=user["_id"], name=f"image_{story_id}", content=image.file.read()
        )

    story: Story = {
        "_id": story_id,
        "user_id": user["_id"],
        "date": date,
        "createTime": time.time() * 1000,
        "title": title,
        "description": description,
        "weather": weather,
        "feeling": feeling,
        "imageUrl": image_url,
        "pictureUrl": None,
    }
    result = get_database().story.insert_one(story)
    if result is None or result.inserted_id != story["_id"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="story insertion failed")

    publish_pubsub(REQUEST_GENERATE_IMAGE_PUBSUB_TOPIC, json.dumps(story))

    return {"story": _story_to_dto(story)}


@story_router.get("/stories/{story_id}")
def get_story(story_id: str, user: User = Depends(get_current_user)):
    story: Story = get_database().story.find_one({"_id": story_id, "user_id": user["_id"]})
    if story is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="story not found")

    return {"story": _story_to_dto(story)}


@story_router.delete("/stories/{story_id}")
def delete_story(story_id: str, user: User = Depends(get_current_user)):
    story: Story = get_database().story.find_one_and_delete({"_id": story_id, "user_id": user["_id"]})
    if story is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="story not found")

    return {"story": {"id": story["_id"]}}
