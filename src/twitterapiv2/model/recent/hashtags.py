from typing import Any
from typing import Dict


class Hashtags:
    start: int
    end: int
    tag: str

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Hashtags":
        """Build object"""
        new = cls()
        new.start = obj.get("start", 0)
        new.end = obj.get("end", 0)
        new.tag = obj.get("tag", "")
        return new
