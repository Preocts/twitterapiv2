from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.domain import Domain
from twitterapiv2.model.recent.entity import Entity


class ContextAnnotations(BaseModel):
    domain: Domain | None
    entity: Entity | None

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> ContextAnnotations:
        """Build object"""
        new = cls()
        domain = data.get("domain")
        new.domain = Domain.build_from(domain) if domain else None
        entity = data.get("entity")
        new.entity = Entity.build_from(entity) if entity else None
        return new
