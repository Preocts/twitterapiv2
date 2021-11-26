import re
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional
from typing import Union

from twitterapiv2.util.rules import is_ISO8601
from twitterapiv2.util.rules import to_ISO8601


class Fields:
    def __init__(self) -> None:
        """Internal: Abstracts all field builder methods for implimentations"""
        self._fields: Dict[str, Any] = {}

    @property
    def fields(self) -> Dict[str, Any]:
        """Returns fields"""
        return self._fields

    def start_time(self, start: Union[str, datetime, None]) -> None:
        """Define start_time of query. YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)"""
        if isinstance(start, datetime):
            start = to_ISO8601(start)
        elif start is not None and not is_ISO8601(start):
            raise ValueError("Datetime format expected: 'YYYY-MM-DDTHH:mm:ssZ'")
        self._fields["start_time"] = start

    def end_time(self, end: Union[str, datetime, None]) -> None:
        """
        Define end_time of query. YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)

        NOTE: The end_time cannot be less than 10 seconds from "now"
        """
        if isinstance(end, datetime):
            end = to_ISO8601(end)
        elif end is not None and not is_ISO8601(end):
            raise ValueError("Datetime format expected: 'YYYY-MM-DDTHH:mm:ssZ'")
        self._fields["end_time"] = end

    def since_id(self, since_id: Optional[str]) -> None:
        """Define since_id of query. Returns results with a Tweet ID greater than"""
        self._fields["since_id"] = since_id if since_id else None

    def until_id(self, until_id: Optional[str]) -> None:
        """Define until_id of query. Returns results with a Tweet ID less than"""
        self._fields["until_id"] = until_id if until_id else None

    def expansions(self, expansions: Optional[str]) -> None:
        """
        Define expansions of query. Comma seperated with no spaces:
            attachments.poll_ids, attachments.media_keys, author_id,
            entities.mentions.username, geo.place_id, in_reply_to_user_id,
            referenced_tweets.id, referenced_tweets.id.author_id
        """
        self._fields["expansions"] = expansions if expansions else None

    def media_fields(self, media_fields: Optional[str]) -> None:
        """
        Define media_fields of query. Comma seperated with no spaces:
            duration_ms, height, media_key, preview_image_url,
            type, url, width, public_metrics, non_public_metrics,
            organic_metrics, promoted_metrics, alt_text
        """
        self._fields["media.fields"] = media_fields if media_fields else None

    def place_fields(self, place_fields: Optional[str]) -> None:
        """
        Define place_fields of query. Comma seperated with no spaces:
            contained_within, country, country_code, full_name,
            geo, id, name, place_type
        """
        self._fields["place.fields"] = place_fields if place_fields else None

    def poll_fields(self, poll_fields: Optional[str]) -> None:
        """
        Define poll_fields of query. Comma seperated with no spaces:
            duration_minutes, end_datetime, id, options, voting_status
        """
        self._fields["poll.fields"] = poll_fields if poll_fields else None

    def tweet_fields(self, tweet_fields: Optional[str]) -> None:
        """
        Define tweet_fields of query. Comma seperated with no spaces:
            attachments, author_id, context_annotations, conversation_id,
            created_at, entities, geo, id, in_reply_to_user_id, lang,
            non_public_metrics, public_metrics, organic_metrics,
            promoted_metrics, possibly_sensitive, referenced_tweets,
            reply_settings, source, text, withheld
        """
        self._fields["tweet.fields"] = tweet_fields if tweet_fields else None

    def user_fields(self, user_fields: Optional[str]) -> None:
        """
        Define user_fields of query. Comma seperated with no spaces:
            created_at, description, entities, id, location, name,
            pinned_tweet_id, profile_image_url, protected,
            public_metrics, url, username, verified, withheld
        """
        self._fields["user.fields"] = user_fields if user_fields else None

    def max_results(self, max_results: Optional[int]) -> None:
        """A number between 10 and 100. By default, set at 10 results"""
        if max_results is not None and max_results not in range(10, 101):
            raise ValueError("max_results must be between 10 and 100")
        self._fields["max_results"] = max_results if max_results else None

    def granularity(
        self,
        granularity: Optional[Literal["minute", "hour", "day"]],
    ) -> None:
        """Define the granularity that you want the timeseries count data grouped"""
        self._fields["granularity"] = granularity if granularity else None

    def query(self, query: Optional[str]) -> None:
        """Sets a query string"""
        self._fields["query"] = query

    def ids(self, ids: Optional[str]) -> None:
        """A single or comma separated list of tweet ids. Max: 100"""
        if ids and len(ids.split(",")) > 100:
            raise ValueError("Maximum of 100 IDs can be provided.")
        elif ids:
            ids = re.sub(r"\s", "", ids)
        self._fields["ids"] = ids if ids else None
