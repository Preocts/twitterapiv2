from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.tweet_count.meta import Meta


class TweetCount(BaseModel):
    start: str
    end: str
    tweet_count: int
    meta: Meta

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> TweetCount:
        new = cls()
        new.start = data.get("start", 0)
        new.end = data.get("end", 0)
        new.tweet_count = data.get("tweet_count", 0)
        new.meta = Meta.build_from(data.get("meta") or {})
        return new
