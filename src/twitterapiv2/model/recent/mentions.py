from typing import Any
from typing import Dict

from twitterapiv2.model.base_model import BaseModel


class Mentions(BaseModel):
    start: int
    end: int
    username: str

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Mentions":
        """Build object"""
        new = cls()
        new.start = data.get("start", 0)
        new.end = data.get("end", 0)
        new.username = data.get("username", "")
        return new
