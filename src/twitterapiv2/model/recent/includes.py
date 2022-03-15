from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class Includes(BaseModel):
    tweets: list[Any]
    users: list[Any]
    places: list[Any]
    media: list[Any]
    polls: str

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Includes:
        """Build object"""
        new = cls()
        new.tweets = data.get("tweets", [])
        new.users = data.get("users", [])
        new.places = data.get("places", [])
        new.media = data.get("media", [])
        new.polls = data.get("polls", "")
        return new
