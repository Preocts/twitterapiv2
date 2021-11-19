from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.model.recent.coordinates import Coordinates


class Geo:
    coordinates: Optional[Coordinates]
    place_id: str

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Geo":
        """Build object"""
        new = cls()
        coord = obj.get("coordinates")
        new.coordinates = Coordinates.build_obj(coord) if coord else None
        new.place_id = obj.get("place_id", "")
        return new
