from __future__ import annotations

from twitterapiv2.client_core import ClientCore
from twitterapiv2.model.recent import Recent

URL = "https://api.twitter.com/2/tweets/search/recent"


class SearchRecent(ClientCore):
    def __init__(self) -> None:
        """
        Create Search Recent client. Use methods to build query and .fetch() to run

        The environment variable "TW_BEARER_TOKEN" is required; define with the
        applicaton bearer token. This can be defined manually or loaded with the
        use of AuthClient.set_bearer_token().
        """
        super().__init__()

        # Define field builder methods
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
        self.query = self.field_builder.query

    def fetch(self) -> Recent:
        """
        Search tweets from up to the last seven days. max size of results is 100

        Pagination is handled internally with the `next_token` being applied
        to the query fields after successful fetch. The property `.next_token`
        can be used to determine when no further results remain (is None)
        """
        if not self.fields.get("query"):
            raise ValueError(".query() is a required field to be defined.")
        return self.get(URL)  # type: ignore
