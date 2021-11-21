from typing import Any
from typing import Dict

from twitterapiv2.model.base_model import BaseModel


class Meta(BaseModel):
    total_tweet_count: int
    next_token: str  # Used with Academic Research Only

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Meta":
        new = cls()
        new.total_tweet_count = data.get("total_tweet_count", 0)
        new.next_token = data.get("next_token", "")
        return new


class TweetCount(BaseModel):
    start: str
    end: str
    tweet_count: int
    meta: Meta

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "TweetCount":
        new = cls()
        new.start = data.get("start", 0)
        new.end = data.get("end", 0)
        new.tweet_count = data.get("tweet_count", 0)
        new.meta = Meta.build_from(data.get("meta") or {})
        return new
