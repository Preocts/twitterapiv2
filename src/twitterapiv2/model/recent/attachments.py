from typing import Any
from typing import Dict
from typing import List

from twitterapiv2.model.base_model import BaseModel


class Attachments(BaseModel):
    media_keys: List[Any]
    poll_id: List[Any]

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Attachments":
        """Build object"""
        new = cls()
        new.media_keys = [key for key in data.get("media_keys", [])]
        new.poll_id = [pid for pid in data.get("poll_id", [])]
        return new
