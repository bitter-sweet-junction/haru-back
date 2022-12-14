import base64
import json
import os

from google.cloud.storage import Client
from pymongo import MongoClient
from stability_sdk.client import StabilityInference

STABILITY_KEY = os.environ.get("STABILITY_KEY")
MONGODB_URI = os.environ.get("MONGODB_URI")

client = Client()
db = MongoClient(MONGODB_URI).haru


def upload_to_gcs(bucket: str, name: str, content: bytes, *, prefix: str = "") -> str:
    bucket_ = client.get_bucket(bucket)
    blob = bucket_.blob(f"{prefix}/{name}" if prefix else name)
    blob.upload_from_string(content)
    blob.make_public()
    return blob.public_url


def inference(title: str, content: str) -> bytes:
    prompt = f"A Cosy image of {title}. highly detailed, art by Makoto Shinkai, Trending on artstation"
    inf = StabilityInference(key=STABILITY_KEY, engine="stable-diffusion-512-v2-0")
    answers = inf.generate(prompt=prompt, height=512, width=512)
    for resp in list(answers):
        for artifact in resp.artifacts:
            if artifact.type == 1:  # generation.ARTIFACT_IMAGE
                return artifact.binary

    return b""


def entrypoint(event, context):
    data = json.loads(base64.b64decode(event["data"]).decode())
    story_id = data["_id"]
    user_id = data["user_id"]
    title = data["title"]
    description = data["description"]

    content = inference(title=title, content=description)
    picture_url = upload_to_gcs(bucket="haru-today-image", prefix=user_id, name=f"picture_{story_id}", content=content)
    db.story.update_one({"_id": story_id}, {"$set": {"pictureUrl": picture_url}})
