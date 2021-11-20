from typing import Any
from typing import Dict

from twitterapiv2.model.base_model import BaseModel


class Entity(BaseModel):
    id: str
    name: str
    description: str

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Entity":
        """Build object"""
        new = cls()
        new.id = data.get("id", "")
        new.name = data.get("name", "")
        new.description = data.get("description", "")
        return new
