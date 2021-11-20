from typing import Any
from typing import Dict
from typing import List
from typing import Optional

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

    id: str
    text: str
    created_at: Optional[str]
    author_id: Optional[str]
    conversation_id: Optional[str]
    in_reply_to_user_id: Optional[str]
    referenced_tweets: List[ReferencedTweets]
    attachments: Optional[Attachments]
    geo: Optional[Geo]
    context_annotations: Optional[ContextAnnotations]
    entities: Optional[Entities]
    withheld: Optional[Withheld]
    public_metrics: Optional[PublicMetrics]
    non_public_metrics: Optional[NonPublicMetrics]
    organic_metrics: Optional[OrganicMetrics]
    promoted_metrics: Optional[PromotedMetrics]
    possibly_sensitive: Optional[bool]
    lang: Optional[str]
    reply_settings: Optional[str]
    source: Optional[str]
    includes: Optional[Includes]

    @classmethod
    def build_from(cls, data: Dict[str, Any]) -> "Data":
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
        tweet.reply_settings = data.get("replay_settings")
        tweet.source = data.get("source")

        # Process nested arrays
        nested_array: Dict[str, Any] = {
            "referenced_tweets": ReferencedTweets,
        }
        for key, model in nested_array.items():
            setattr(tweet, key, [model.build_from(x) for x in data.get(key, [])])

        # Process Nested Objects
        nested_obj: Dict[str, Any] = {
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
