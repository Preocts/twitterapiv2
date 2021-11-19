from typing import Any
from typing import Dict
from typing import List

from twitterapiv2.model.recent.annotations import Annotations
from twitterapiv2.model.recent.cashtags import Cashtags
from twitterapiv2.model.recent.hashtags import Hashtags
from twitterapiv2.model.recent.mentions import Mentions
from twitterapiv2.model.recent.urls import Urls


class Entities:
    annotations: List[Annotations]
    urls: List[Urls]
    hashtags: List[Hashtags]
    mentions: List[Mentions]
    cashtags: List[Cashtags]

    @classmethod
    def build_obj(cls, obj: Dict[str, Any]) -> "Entities":
        """Build object"""
        new = cls()
        new.annotations = [Annotations.build_obj(o) for o in obj.get("annotations", [])]
        new.urls = [Urls.build_obj(o) for o in obj.get("urls", [])]
        new.hashtags = [Hashtags.build_obj(o) for o in obj.get("hashtags", [])]
        new.mentions = [Mentions.build_obj(o) for o in obj.get("mentions", [])]
        new.cashtags = [Cashtags.build_obj(o) for o in obj.get("cashtags", [])]
        return new
