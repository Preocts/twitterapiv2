from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class Meta(BaseModel):
    count: int
    newest_id: int
    oldest_id: int
    next_token: str | None

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Meta:
        """Build object"""
        new = cls()
        new.count = data.get("count", 0)
        new.newest_id = data.get("newest_id", 0)
        new.oldest_id = data.get("oldest_id", 0)
        new.next_token = data.get("next_token")
        return new
