from abc import ABC
from typing import Any
from typing import Dict


class BaseModel(ABC):
    """An empty model object"""

    def build_from(self, data: Dict[str, Any]) -> "BaseModel":
        raise NotImplementedError  # pragma: no cover
