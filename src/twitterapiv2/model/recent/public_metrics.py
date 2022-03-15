from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class PublicMetrics(BaseModel):
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> PublicMetrics:
        """Build object"""
        new = cls()
        new.retweet_count = data.get("retweet_count", 0)
        new.reply_count = data.get("reply_count", 0)
        new.like_count = data.get("like_count", 0)
        new.quote_count = data.get("quote_count", 0)
        return new
