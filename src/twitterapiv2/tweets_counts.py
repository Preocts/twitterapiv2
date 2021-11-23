from datetime import datetime
from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional
from typing import Union

from twitterapiv2.http import Http
from twitterapiv2.model.tweet_count.tweet_count import TweetCount
from twitterapiv2.util.rules import is_ISO8601
from twitterapiv2.util.rules import to_ISO8601


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
        self.http = Http()
        self._fields: Dict[str, Any] = {}
        self._next_token: Optional[str] = None
        self._url = self.URL_ALL if end_point == "all" else self.URL_RECENT

    @property
    def fields(self) -> Dict[str, Any]:
        """Returns fields that have been defined"""
        return {key: str(value) for key, value in self._fields.items() if value}

    @property
    def next_token(self) -> Optional[str]:
        """Return next_token for pagination or `None` when all results are polled"""
        return self._next_token

    def start_time(self, start: Union[str, datetime, None]) -> "TweetsCounts":
        """Define start_time of query. YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)"""
        if isinstance(start, datetime):
            start = to_ISO8601(start)
        elif start is not None and not is_ISO8601(start):
            raise ValueError("Datetime format expected: 'YYYY-MM-DDTHH:mm:ssZ'")
        self._fields["start_time"] = start
        return self._new_client()

    def end_time(self, end: Union[str, datetime, None]) -> "TweetsCounts":
        """
        Define end_time of query. YYYY-MM-DDTHH:mm:ssZ (ISO 8601/RFC 3339)

        NOTE: The end_time cannot be less than 10 seconds from "now"
        """
        if isinstance(end, datetime):
            end = to_ISO8601(end)
        elif end is not None and not is_ISO8601(end):
            raise ValueError("Datetime format expected: 'YYYY-MM-DDTHH:mm:ssZ'")
        self._fields["end_time"] = end
        return self._new_client()

    def since_id(self, since_id: Optional[str]) -> "TweetsCounts":
        """Define since_id of query. Returns results with a Tweet ID greater than"""
        self._fields["since_id"] = since_id if since_id else None
        return self._new_client()

    def until_id(self, until_id: Optional[str]) -> "TweetsCounts":
        """Define until_id of query. Returns results with a Tweet ID less than"""
        self._fields["until_id"] = until_id if until_id else None
        return self._new_client()

    def granularity(
        self,
        granularity: Optional[Literal["minute", "hour", "day"]],
    ) -> "TweetsCounts":
        """Define the granularity that you want the timeseries count data grouped"""
        self._fields["granularity"] = granularity if granularity else None
        return self._new_client()

    def fetch(self, query: str, *, page_token: Optional[str] = None) -> TweetCount:
        """
        Fetches the count of Tweets from the last seven days that match a query

        Time-range can be controlled with start_time and end_time. Pagination
        only available with Acedemic research applications. `.next_token()` will
        be populated with the needed page_token on each call.
        """
        self._fields["query"] = query
        self._fields["next_token"] = page_token
        result = TweetCount.build_from(self.http.get(self._url, self.fields))
        self._next_token = result.meta.next_token
        return result

    def _new_client(self) -> "TweetsCounts":
        """Used to create a new client with attributes carried forward"""
        new_client = TweetsCounts()
        new_client._fields.update(self._fields)
        return new_client
