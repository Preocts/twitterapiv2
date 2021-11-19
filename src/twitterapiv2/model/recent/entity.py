from typing import Any
from typing import Dict


class Entity:
    id: str
    name: str
    description: str

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Entity":
        """Build object"""
        new = cls()
        new.id = obj.get("id", "")
        new.name = obj.get("name", "")
        new.description = obj.get("description", "")
        return new
