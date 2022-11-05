import base64
import json
import os

import requests
from google.cloud.storage import Client
from pymongo import MongoClient

IMAGE_GENERATOR_HOST = os.environ.get("IMAGE_GENERATOR_HOST")
MONGODB_URI = os.environ.get("MONGODB_URI")

client = Client()
db = MongoClient(MONGODB_URI).haru


def upload_to_gcs(bucket: str, name: str, content: bytes, *, prefix: str = "") -> str:
    bucket_ = client.get_bucket(bucket)
    blob = bucket_.blob(f"{prefix}/{name}" if prefix else name)
    blob.upload_from_string(content)
    blob.make_public()
    return blob.public_url


def entrypoint(event, context):
    data = json.loads(base64.b64decode(event["data"]).decode())
    story_id = data["_id"]
    user_id = data["user_id"]
    title = data["title"]
    description = data["description"]

    content = {"title": title, "content": description}
    result = requests.post(f"{IMAGE_GENERATOR_HOST}/text2img", json=content)
    picture_url = upload_to_gcs(
        bucket="haru-image-store", prefix=user_id, name=f"picture_{story_id}", content=result.content
    )
    db.story.update_one({"_id": story_id}, {"$set": {"pictureUrl": picture_url}})
