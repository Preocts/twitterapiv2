from typing import Any
from typing import Dict


class Urls:
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str
    unwound_url: str

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Urls":
        """Build object"""
        new = cls()
        new.start = obj.get("start", 0)
        new.end = obj.get("end", 0)
        new.url = obj.get("url", "")
        new.expanded_url = obj.get("expanded_url", "")
        new.display_url = obj.get("display_url", "")
        new.unwound_url = obj.get("unwound_url", "")
        return new
