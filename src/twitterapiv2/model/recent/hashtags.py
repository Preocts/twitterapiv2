from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class Hashtags(BaseModel):
    start: int
    end: int
    tag: str

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Hashtags:
        """Build object"""
        new = cls()
        new.start = data.get("start", 0)
        new.end = data.get("end", 0)
        new.tag = data.get("tag", "")
        return new
