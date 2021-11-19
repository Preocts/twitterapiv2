from typing import Any
from typing import Dict
from typing import List


class Withheld:
    copyright: bool
    country_code: List[Any]
    scope: int

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Withheld":
        """Build object"""
        new = cls()
        new.copyright = obj.get("copyright", False)
        new.country_code = obj.get("country_code", [])
        new.scope = obj.get("scope", 0)
        return new
