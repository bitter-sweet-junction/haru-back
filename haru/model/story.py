from typing import Literal, Optional, TypedDict


class Story(TypedDict):
    _id: Optional[str]
    name: str
    date: str
    weather: Literal["SUNNY", "RAIN", "CLOUD"]
    createTime: float
    imageUrl: Optional[str]
    title: str
    description: Optional[str]
    feeling: Literal["HAPPY", "ANGRY", "SAD"]
