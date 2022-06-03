from __future__ import annotations

from typing import Any

from twitterapiv2.model.base_model import BaseModel
from twitterapiv2.model.recent.attachments import Attachments
from twitterapiv2.model.recent.context_annotations import ContextAnnotations
from twitterapiv2.model.recent.entities import Entities
from twitterapiv2.model.recent.geo import Geo
from twitterapiv2.model.recent.includes import Includes
from twitterapiv2.model.recent.non_public_metrics import NonPublicMetrics
from twitterapiv2.model.recent.organic_metrics import OrganicMetrics
from twitterapiv2.model.recent.promoted_metrics import PromotedMetrics
from twitterapiv2.model.recent.public_metrics import PublicMetrics
from twitterapiv2.model.recent.referenced_tweets import ReferencedTweets
from twitterapiv2.model.recent.withheld import Withheld


class Data(BaseModel):
    """Defines an empty Data object"""

    id: str  # noqa: A003
    text: str
    created_at: str | None
    author_id: str | None
    conversation_id: str | None
    in_reply_to_user_id: str | None
    referenced_tweets: list[ReferencedTweets]
    attachments: Attachments | None
    geo: Geo | None
    context_annotations: ContextAnnotations | None
    entities: Entities | None
    withheld: Withheld | None
    public_metrics: PublicMetrics | None
    non_public_metrics: NonPublicMetrics | None
    organic_metrics: OrganicMetrics | None
    promoted_metrics: PromotedMetrics | None
    possibly_sensitive: bool | None
    lang: str | None
    reply_settings: str | None
    source: str | None
    includes: Includes | None

    @classmethod
    def build_from(cls, data: dict[str, Any]) -> Data:
        """Builds object from dictionary"""
        tweet = cls()
        tweet.id = data["id"]
        tweet.text = data["text"]
        tweet.created_at = data.get("created_at")
        tweet.author_id = data.get("author_id")
        tweet.conversation_id = data.get("conversation_id")
        tweet.in_reply_to_user_id = data.get("in_reply_to_user_id")
        tweet.possibly_sensitive = data.get("possibly_sensitive")
        tweet.lang = data.get("lang")
        tweet.reply_settings = data.get("reply_settings")
        tweet.source = data.get("source")

        # Process nested arrays
        nested_array: dict[str, Any] = {
            "referenced_tweets": ReferencedTweets,
        }
        for key, model in nested_array.items():
            setattr(tweet, key, [model.build_from(x) for x in data.get(key, [])])

        # Process Nested Objects
        nested_obj: dict[str, Any] = {
            "attachments": Attachments,
            "geo": Geo,
            "context_annotations": ContextAnnotations,
            "entities": Entities,
            "withheld": Withheld,
            "public_metrics": PublicMetrics,
            "non_public_metrics": NonPublicMetrics,
            "organic_metrics": OrganicMetrics,
            "promoted_metrics": PromotedMetrics,
            "includes": Includes,
        }
        for key, model in nested_obj.items():
            content = data.get(key)
            setattr(tweet, key, model.build_from(content) if content else None)

        return tweet
