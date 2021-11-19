from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.model.recent.domain import Domain
from twitterapiv2.model.recent.entity import Entity


class ContextAnnotations:
    domain: Optional[Domain]
    entity: Optional[Entity]

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "ContextAnnotations":
        """Build object"""
        new = cls()
        domain = obj.get("domain")
        new.domain = Domain.build_obj(domain) if domain else None
        entity = obj.get("entity")
        new.entity = Entity.build_obj(entity) if entity else None
        return new
