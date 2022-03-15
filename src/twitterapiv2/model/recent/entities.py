from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.annotations import Annotations
from twitterapiv2.model.recent.cashtags import Cashtags
from twitterapiv2.model.recent.hashtags import Hashtags
from twitterapiv2.model.recent.mentions import Mentions
from twitterapiv2.model.recent.urls import Urls


class Entities(BaseModel):
    annotations: list[Annotations]
    urls: list[Urls]
    hashtags: list[Hashtags]
    mentions: list[Mentions]
    cashtags: list[Cashtags]

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Entities:
        """Build object"""
        new = cls()
        new.annotations = [
            Annotations.build_from(o) for o in data.get("annotations", [])
        ]
        new.urls = [Urls.build_from(o) for o in data.get("urls", [])]
        new.hashtags = [Hashtags.build_from(o) for o in data.get("hashtags", [])]
        new.mentions = [Mentions.build_from(o) for o in data.get("mentions", [])]
        new.cashtags = [Cashtags.build_from(o) for o in data.get("cashtags", [])]
        return new
