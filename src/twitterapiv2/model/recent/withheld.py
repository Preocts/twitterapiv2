from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel


class Withheld(BaseModel):
    copyright: bool
    country_code: list[Any]
    scope: int

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Withheld:
        """Build object"""
        new = cls()
        new.copyright = data.get("copyright", False)
        new.country_code = data.get("country_code", [])
        new.scope = data.get("scope", 0)
        return new
