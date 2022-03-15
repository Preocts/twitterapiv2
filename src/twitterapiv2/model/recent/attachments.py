from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class Attachments(BaseModel):
    media_keys: list[Any]
    poll_id: list[Any]

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Attachments:
        """Build object"""
        new = cls()
        new.media_keys = [key for key in data.get("media_keys", [])]
        new.poll_id = [pid for pid in data.get("poll_id", [])]
        return new
