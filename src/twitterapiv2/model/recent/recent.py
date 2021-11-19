"""
https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent#Default
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from twitterapiv2.model.recent.data import Data
from twitterapiv2.model.recent.meta import Meta


class Recent:
    """Defines an empty search/recent object"""

    data: List[Data]
    meta: Meta
    errors: Optional[Dict[str, Any]]

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Recent":
        """Builds object from dictionary"""
        new = cls()
        new.errors = obj.get("errors")
        new.data = [Data.build_obj(x) for x in obj.get("data", [])]
        new.meta = Meta.build_obj(obj.get("meta", {}))
        return new
