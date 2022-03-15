"""
https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#Default
"""
from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.data import Data
from twitterapiv2.model.recent.meta import Meta


class Recent(BaseModel):
    """Defines an empty search/recent object"""

    data: list[Data]
    meta: Meta
    errors: dict[str, Any] | None

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Recent:
        """Builds object from dictionary"""
        new = cls()
        new.errors = data.get("errors")
        new.data = [Data.build_from(x) for x in data.get("data", [])]
        new.meta = Meta.build_from(data.get("meta", {}))
        return new
