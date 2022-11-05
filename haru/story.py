from fastapi import APIRouter

story_router = APIRouter()


@story_router.get("/stories")
def get_stories():
    pass


@story_router.post("/stories")
def post_stories():
    pass


@story_router.get("/stories/<story_id>")
def get_story(story_id: int):
    pass


@story_router.delete("/stories/<story_id>")
def delete_story(story_id: int):
    pass
