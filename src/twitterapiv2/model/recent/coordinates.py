from typing import Any
from typing import Dict
from typing import List


class Coordinates:
    type: str
    coordinates: List[float]

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Coordinates":
        """Build object"""
        new = cls()
        new.type = obj.get("type", "")
        new.coordinates = [co for co in obj.get("coordinates", [])]
        return new
