from typing import Any
from typing import Dict


class NonPublicMetrics:
    impression_count: int
    url_link_click: int
    user_profile_click: int

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "NonPublicMetrics":
        """Build object"""
        new = cls()
        new.impression_count = obj.get("impression_count", 0)
        new.url_link_click = obj.get("url_link_click", 0)
        new.user_profile_click = obj.get("user_profile_click", 0)
        return new
