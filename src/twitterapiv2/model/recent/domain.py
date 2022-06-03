from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class Domain(BaseModel):
    id: str  # noqa: A003
    name: str
    description: str

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Domain:
        """Build object"""
        new = cls()
        new.id = data.get("id", "")
        new.name = data.get("name", "")
        new.description = data.get("description", "")
        return new
