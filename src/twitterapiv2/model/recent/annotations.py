from typing import Any
from typing import Dict

from twitterapiv2.model.base_model import BaseModel


class Annotations(BaseModel):
    start: int
    end: int
    probability: float
    type: str
    normalized_text: str

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Annotations":
        """Build object"""
        new = cls()
        new.start = data.get("start", 0)
        new.end = data.get("end", 0)
        new.probability = data.get("probability", 0.0)
        new.type = data.get("type", "")
        new.normalized_text = data.get("normalized_text", "")
        return new
