from typing import Any
from typing import Dict
from typing import List

from twitterapiv2.model.base_model import BaseModel


class Includes(BaseModel):
    tweets: List[Any]
    users: List[Any]
    places: List[Any]
    media: List[Any]
    polls: str

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Includes":
        """Build object"""
        new = cls()
        new.tweets = data.get("tweets", [])
        new.users = data.get("users", [])
        new.places = data.get("places", [])
        new.media = data.get("media", [])
        new.polls = data.get("polls", "")
        return new
