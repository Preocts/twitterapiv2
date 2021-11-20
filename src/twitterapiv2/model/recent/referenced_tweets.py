from typing import Any
from typing import Dict

from twitterapiv2.model.base_model import BaseModel


class ReferencedTweets(BaseModel):
    id: str
    type: int

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "ReferencedTweets":
        """Build object"""
        new = cls()
        new.id = data.get("id", "")
        new.type = data.get("type", 0)
        return new
