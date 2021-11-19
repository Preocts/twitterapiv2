from typing import Any
from typing import Dict


class Annotations:
    start: int
    end: int
    probability: float
    type: str
    normalized_text: str

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Annotations":
        """Build object"""
        new = cls()
        new.start = obj.get("start", 0)
        new.end = obj.get("end", 0)
        new.probability = obj.get("probability", 0.0)
        new.type = obj.get("type", "")
        new.normalized_text = obj.get("normalized_text", "")
        return new
