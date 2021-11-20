from typing import Any
from typing import Dict
from typing import List

from twitterapiv2.model.base_model import BaseModel


class Coordinates(BaseModel):
    type: str
    coordinates: List[float]

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Coordinates":
        """Build object"""
        new = cls()
        new.type = data.get("type", "")
        new.coordinates = [co for co in data.get("coordinates", [])]
        return new
