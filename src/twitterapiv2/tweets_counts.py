from __future__ import annotations

from typing import TYPE_CHECKING

from twitterapiv2.client_core import ClientCore
from twitterapiv2.model.tweet_count.tweet_count import TweetCount

if TYPE_CHECKING:
    from typing import Literal

URL_RECENT = "https://api.twitter.com/2/tweets/counts/recent"
URL_ALL = "https://api.twitter.com/2/tweets/counts/all"


class TweetsCounts(ClientCore):
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
        super().__init__()
        self._url = URL_ALL if end_point == "all" else URL_RECENT

        # Define builder methods
        self.start_time = self.field_builder.start_time
        self.end_time = self.field_builder.end_time
        self.since_id = self.field_builder.since_id
        self.until_id = self.field_builder.until_id
        self.granularity = self.field_builder.granularity
        self.query = self.field_builder.query

    def fetch(self) -> TweetCount:
        """
        Fetches the count of Tweets from the last seven days that match a query

        Time-range can be controlled with start_time and end_time. Pagination
        only available with Acedemic research applications. `.next_token()` will
        be populated with the needed page_token on each call.
        """
        if not self.fields.get("query"):
            raise ValueError(".query() is a required field to be defined.")

        return TweetCount.build_from(self.get(self._url))
