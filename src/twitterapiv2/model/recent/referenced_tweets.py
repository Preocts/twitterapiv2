from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class ReferencedTweets(BaseModel):
    id: str
    type: int

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> ReferencedTweets:
        """Build object"""
        new = cls()
        new.id = data.get("id", "")
        new.type = data.get("type", 0)
        return new
