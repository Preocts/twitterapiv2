from typing import Any
from typing import Dict
from typing import List


class Includes:
    tweets: List[Any]
    users: List[Any]
    places: List[Any]
    media: List[Any]
    polls: str

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Includes":
        """Build object"""
        new = cls()
        new.tweets = obj.get("tweets", [])
        new.users = obj.get("users", [])
        new.places = obj.get("places", [])
        new.media = obj.get("media", [])
        new.polls = obj.get("polls", "")
        return new
