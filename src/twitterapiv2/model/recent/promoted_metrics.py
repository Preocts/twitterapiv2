from typing import Any
from typing import Dict


class PromotedMetrics:
    impression_count: int
    url_link_click: int
    user_profile_click: int
    retweet_count: int
    reply_count: int
    like_count: int

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "PromotedMetrics":
        """Build object"""
        new = cls()
        new.impression_count = obj.get("impression_count", 0)
        new.url_link_click = obj.get("url_link_click", 0)
        new.user_profile_click = obj.get("user_profile_click", 0)
        new.retweet_count = obj.get("retweet_count", 0)
        new.reply_count = obj.get("reply_count", 0)
        new.like_count = obj.get("like_count", 0)
        return new
