from typing import TypedDict


class User(TypedDict):
    _id: str | None
    google_email: str
    google_name: str
    google_picture: str
