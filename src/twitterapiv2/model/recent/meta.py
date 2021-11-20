from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.model.base_model import BaseModel


class Meta(BaseModel):
    count: int
    newest_id: int
    oldest_id: int
    next_token: Optional[str]

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Meta":
        """Build object"""
        new = cls()
        new.count = data.get("count", 0)
        new.newest_id = data.get("newest_id", 0)
        new.oldest_id = data.get("oldest_id", 0)
        new.next_token = data.get("next_token")
        return new
