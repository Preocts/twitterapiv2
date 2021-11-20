from typing import Any
from typing import Dict

from twitterapiv2.model.base_model import BaseModel


class Urls(BaseModel):
    start: int
    end: int
    url: str
    expanded_url: str
    display_url: str
    unwound_url: str

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Urls":
        """Build object"""
        new = cls()
        new.start = data.get("start", 0)
        new.end = data.get("end", 0)
        new.url = data.get("url", "")
        new.expanded_url = data.get("expanded_url", "")
        new.display_url = data.get("display_url", "")
        new.unwound_url = data.get("unwound_url", "")
        return new
