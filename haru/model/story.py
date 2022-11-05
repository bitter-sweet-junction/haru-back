from typing import Literal, TypedDict


class Story(TypedDict):
    _id: str | None
    user_id: str
    name: str
    date: str
    weather: Literal["SUNNY", "RAIN", "CLOUD"]
    createTime: float
    imageUrl: str | None
    title: str
    description: str | None
    feeling: Literal["HAPPY", "ANGRY", "SAD"]
