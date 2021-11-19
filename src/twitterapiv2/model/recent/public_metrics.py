from typing import Any
from typing import Dict


class PublicMetrics:
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "PublicMetrics":
        """Build object"""
        new = cls()
        new.retweet_count = obj.get("retweet_count", 0)
        new.reply_count = obj.get("reply_count", 0)
        new.like_count = obj.get("like_count", 0)
        new.quote_count = obj.get("quote_count", 0)
        return new
