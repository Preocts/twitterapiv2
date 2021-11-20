from typing import Any
from typing import Dict
from typing import Optional


class Meta:
    count: int
    newest_id: int
    oldest_id: int
    next_token: Optional[str]

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Meta":
        """Build object"""
        new = cls()
        new.count = obj.get("count", 0)
        new.newest_id = obj.get("newest_id", 0)
        new.oldest_id = obj.get("oldest_id", 0)
        new.next_token = obj.get("next_token")
        return new
