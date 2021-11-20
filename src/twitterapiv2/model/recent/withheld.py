from typing import Any
from typing import Dict
from typing import List

from twitterapiv2.model.base_model import BaseModel


class Withheld(BaseModel):
    copyright: bool
    country_code: List[Any]
    scope: int

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Withheld":
        """Build object"""
        new = cls()
        new.copyright = data.get("copyright", False)
        new.country_code = data.get("country_code", [])
        new.scope = data.get("scope", 0)
        return new
