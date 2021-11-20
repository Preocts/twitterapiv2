from typing import Any
from typing import Dict

from twitterapiv2.model.base_model import BaseModel


class NonPublicMetrics(BaseModel):
    impression_count: int
    url_link_click: int
    user_profile_click: int

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "NonPublicMetrics":
        """Build object"""
        new = cls()
        new.impression_count = data.get("impression_count", 0)
        new.url_link_click = data.get("url_link_click", 0)
        new.user_profile_click = data.get("user_profile_click", 0)
        return new
