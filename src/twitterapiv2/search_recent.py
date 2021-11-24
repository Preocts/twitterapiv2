from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.fields import Fields
from twitterapiv2.http import Http
from twitterapiv2.model.recent.recent import Recent


class SearchRecent:

    URL = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self) -> None:
        """
        Create Search Recent client. Use methods to build query and .fetch() to run

        The environment variable "TW_BEARER_TOKEN" is required; define with the
        applicaton bearer token. This can be defined manually or loaded with the
        use of AuthClient.set_bearer_token().
        """
        self.field_builder = Fields()
        self.http = Http()
        self._next_token: Optional[str] = None
        self.start_time = self.field_builder.start_time
        self.end_time = self.field_builder.end_time
        self.since_id = self.field_builder.since_id
        self.until_id = self.field_builder.until_id
        self.expansions = self.field_builder.expansions
        self.media_fields = self.field_builder.media_fields
        self.place_fields = self.field_builder.place_fields
        self.poll_fields = self.field_builder.poll_fields
        self.tweet_fields = self.field_builder.tweet_fields
        self.user_fields = self.field_builder.user_fields
        self.max_results = self.field_builder.max_results

    @property
    def fields(self) -> Dict[str, Any]:
        """Returns fields that have been defined"""
        return self.field_builder.fields

    @property
    def next_token(self) -> Optional[str]:
        """Return next_token for pagination or `None` when all results are polled"""
        return self._next_token

    def fetch(
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
        self.field_builder.query(query)
        self.field_builder.next_token(page_token)
        result = Recent.build_from(self.http.get(self.URL, self.fields))
        self._next_token = result.meta.next_token
        return result
