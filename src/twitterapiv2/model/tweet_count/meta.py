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
