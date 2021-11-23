from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union

from twitterapiv2.http import Http
from twitterapiv2.model.recent.recent import Recent
from twitterapiv2.util.rules import is_ISO8601
from twitterapiv2.util.rules import to_ISO8601


class SearchRecent:

    URL = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self) -> None:
        """
        Create Search Recent client. Use methods to build query a .search() to run

        The environment variable "TW_BEARER_TOKEN" is required; define with the
        applicaton bearer token. This can be defined manually or loaded with the
        use of AuthClient.set_bearer_token().
        """
        self.http = Http()
        self._fields: Dict[str, Any] = {}
        self._next_token: Optional[str] = None

    @property
    def fields(self) -> Dict[str, Any]:
        """Returns fields that have been defined"""
        return {key: str(value) for key, value in self._fields.items() if value}

    @property
    def next_token(self) -> Optional[str]:
        """Return next_token for pagination or `None` when all results are polled"""
        return self._next_token

    def start_time(self, start: Union[str, datetime, None]) -> "SearchRecent":
        """Define start_time of query. YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)"""
        if isinstance(start, datetime):
            start = to_ISO8601(start)
        elif start is not None and not is_ISO8601(start):
            raise ValueError("Datetime format expected: 'YYYY-MM-DDTHH:mm:ssZ'")
        self._fields["start_time"] = start if start else None
        return self._new_client()

    def end_time(self, end: Union[str, datetime, None]) -> "SearchRecent":
        """
        Define end_time of query. YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)

        NOTE: The end_time cannot be less than 10 seconds from "now"
        """
        if isinstance(end, datetime):
            end = to_ISO8601(end)
        elif end is not None and not is_ISO8601(end):
            raise ValueError("Datetime format expected: 'YYYY-MM-DDTHH:mm:ssZ'")
        self._fields["end_time"] = end if end else None
        return self._new_client()

    def since_id(self, since_id: Optional[str]) -> "SearchRecent":
        """Define since_id of query. Returns results with a Tweet ID greater than"""
        self._fields["since_id"] = since_id if since_id else None
        return self._new_client()

    def until_id(self, until_id: Optional[str]) -> "SearchRecent":
        """Define until_id of query. Returns results with a Tweet ID less than"""
        self._fields["until_id"] = until_id if until_id else None
        return self._new_client()

    def expansions(self, expansions: Optional[str]) -> "SearchRecent":
        """
        Define expansions of query. Comma seperated with no spaces:
            attachments.poll_ids, attachments.media_keys, author_id,
            entities.mentions.username, geo.place_id, in_reply_to_user_id,
            referenced_tweets.id, referenced_tweets.id.author_id
        """
        self._fields["expansions"] = expansions if expansions else None
        return self._new_client()

    def media_fields(self, media_fields: Optional[str]) -> "SearchRecent":
        """
        Define media_fields of query. Comma seperated with no spaces:
            duration_ms, height, media_key, preview_image_url,
            type, url, width, public_metrics, non_public_metrics,
            organic_metrics, promoted_metrics, alt_text
        """
        self._fields["media.fields"] = media_fields if media_fields else None
        return self._new_client()

    def place_fields(self, place_fields: Optional[str]) -> "SearchRecent":
        """
        Define place_fields of query. Comma seperated with no spaces:
            contained_within, country, country_code, full_name,
            geo, id, name, place_type
        """
        self._fields["place.fields"] = place_fields if place_fields else None
        return self._new_client()

    def poll_fields(self, poll_fields: Optional[str]) -> "SearchRecent":
        """
        Define poll_fields of query. Comma seperated with no spaces:
            duration_minutes, end_datetime, id, options, voting_status
        """
        self._fields["poll.fields"] = poll_fields if poll_fields else None
        return self._new_client()

    def tweet_fields(self, tweet_fields: Optional[str]) -> "SearchRecent":
        """
        Define tweet_fields of query. Comma seperated with no spaces:
            attachments, author_id, context_annotations, conversation_id,
            created_at, entities, geo, id, in_reply_to_user_id, lang,
            non_public_metrics, public_metrics, organic_metrics,
            promoted_metrics, possibly_sensitive, referenced_tweets,
            reply_settings, source, text, withheld
        """
        self._fields["tweet.fields"] = tweet_fields if tweet_fields else None
        return self._new_client()

    def user_fields(self, user_fields: Optional[str]) -> "SearchRecent":
        """
        Define user_fields of query. Comma seperated with no spaces:
            created_at, description, entities, id, location, name,
            pinned_tweet_id, profile_image_url, protected,
            public_metrics, url, username, verified, withheld
        """
        self._fields["user.fields"] = user_fields if user_fields else None
        return self._new_client()

    def max_results(self, max_results: Optional[int]) -> "SearchRecent":
        """A number between 10 and 100. By default, set at 10 results"""
        if max_results is not None and max_results not in range(10, 101):
            raise ValueError("max_results must be between 10 and 100")
        self._fields["max_results"] = max_results if max_results else None
        return self._new_client()

    def search(
        self,
        query: str,
        *,
        page_token: Optional[str] = None,
    ) -> Recent:
        """
        Search tweets from up to the last seven days. max size of results is 100

        For pagination; feed the `.next_token()` property into the
        `next_token` parameter. These default to None and can be
        safely referenced prior to, and after, searches.
        """
        self._fields["query"] = query
        self._fields["next_token"] = page_token
        result = Recent.build_from(self.http.get(self.URL, self.fields))
        self._next_token = result.meta.next_token
        return result

    def _new_client(self) -> "SearchRecent":
        """Used to create a new client with attributes carried forward"""
        new_client = SearchRecent()
        new_client._fields.update(self._fields)
        return new_client
