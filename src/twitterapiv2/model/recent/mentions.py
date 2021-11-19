from typing import Any
from typing import Dict


class Mentions:
    start: int
    end: int
    username: str

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Mentions":
        """Build object"""
        new = cls()
        new.start = obj.get("start", 0)
        new.end = obj.get("end", 0)
        new.username = obj.get("username", "")
        return new
