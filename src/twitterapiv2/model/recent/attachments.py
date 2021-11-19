from typing import Any
from typing import Dict
from typing import List


class Attachments:
    media_keys: List[Any]
    poll_id: List[Any]

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Attachments":
        """Build object"""
        new = cls()
        new.media_keys = [key for key in obj.get("media_keys", [])]
        new.poll_id = [pid for pid in obj.get("poll_id", [])]
        return new
