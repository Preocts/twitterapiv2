from typing import Any
from typing import Dict


class ReferencedTweets:
    id: str
    type: int

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "ReferencedTweets":
        """Build object"""
        new = cls()
        new.id = obj.get("id", "")
        new.type = obj.get("type", 0)
        return new
