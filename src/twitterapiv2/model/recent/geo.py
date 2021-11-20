from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.coordinates import Coordinates


class Geo(BaseModel):
    coordinates: Optional[Coordinates]
    place_id: str

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Geo":
        """Build object"""
        new = cls()
        coord = data.get("coordinates")
        new.coordinates = Coordinates.build_from(coord) if coord else None
        new.place_id = data.get("place_id", "")
        return new
