from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class OrganicMetrics(BaseModel):
    impression_count: int
    url_link_click: int
    user_profile_click: int
    retweet_count: int
    reply_count: int
    like_count: int

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> OrganicMetrics:
        """Build object"""
        new = cls()
        new.impression_count = data.get("impression_count", 0)
        new.url_link_click = data.get("url_link_click", 0)
        new.user_profile_click = data.get("user_profile_click", 0)
        new.retweet_count = data.get("retweet_count", 0)
        new.reply_count = data.get("reply_count", 0)
        new.like_count = data.get("like_count", 0)
        return new
