from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional

from twitterapiv2.fields import Fields
from twitterapiv2.http import Http
from twitterapiv2.model.tweet_count.tweet_count import TweetCount


class TweetsCounts:

    URL_RECENT = "https://api.twitter.com/2/tweets/counts/recent"
    URL_ALL = "https://api.twitter.com/2/tweets/counts/all"

    def __init__(
        self,
        end_point: Literal["recent", "all"] = "recent",
    ) -> None:
        """
        Create Tweets Counts client. Use methods to build query and .fetch() to run

        end_point allows use of `/counts/all` endpoint for Academic Research access

        The environment variable "TW_BEARER_TOKEN" is required; define with the
        applicaton bearer token. This can be defined manually or loaded with the
        use of AuthClient.set_bearer_token().
        """
        self.field_builder = Fields()
        self.http = Http()
        self._next_token: Optional[str] = None
        self._url = self.URL_ALL if end_point == "all" else self.URL_RECENT
        self.start_time = self.field_builder.start_time
        self.end_time = self.field_builder.end_time
        self.since_id = self.field_builder.since_id
        self.until_id = self.field_builder.until_id
        self.granularity = self.field_builder.granularity

    @property
    def fields(self) -> Dict[str, Any]:
        """Returns fields that have been defined"""
        return self.field_builder.fields

    @property
    def next_token(self) -> Optional[str]:
        """Return next_token for pagination or `None` when all results are polled"""
        return self._next_token

    def fetch(self, query: str, *, page_token: Optional[str] = None) -> TweetCount:
        """
        Fetches the count of Tweets from the last seven days that match a query

        Time-range can be controlled with start_time and end_time. Pagination
        only available with Acedemic research applications. `.next_token()` will
        be populated with the needed page_token on each call.
        """
        self.field_builder.query(query)
        self.field_builder.next_token(page_token)
        result = TweetCount.build_from(self.http.get(self._url, self.fields))
        self._next_token = result.meta.next_token
        return result
