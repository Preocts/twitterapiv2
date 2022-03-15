from __future__ import annotations

import json
from abc import ABC
from typing import Any


class BaseModelEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        return o.__dict__


class BaseModel(ABC):
    """An empty model object"""

    def __repr__(self) -> str:
        return json.dumps(self, cls=BaseModelEncoder)

    def to_json(self) -> dict[str, Any]:
        """Returns objects as serialized dictionary (JSON)"""
        return json.loads(self.__repr__())

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> BaseModel:
        raise NotImplementedError  # pragma: no cover
