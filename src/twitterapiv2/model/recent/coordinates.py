from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class Coordinates(BaseModel):
    type: str
    coordinates: list[float]

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Coordinates:
        """Build object"""
        new = cls()
        new.type = data.get("type", "")
        new.coordinates = [co for co in data.get("coordinates", [])]
        return new
