from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.coordinates import Coordinates


class Geo(BaseModel):
    coordinates: Coordinates | None
    place_id: str

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Geo:
        """Build object"""
        new = cls()
        coord = data.get("coordinates")
        new.coordinates = Coordinates.build_from(coord) if coord else None
        new.place_id = data.get("place_id", "")
        return new
