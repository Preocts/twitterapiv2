from __future__ import annotations

from twitterapiv2._appauth_client import AppAuthClient
from twitterapiv2.client_core import ClientCore
from twitterapiv2.model.application_auth import ApplicationAuth
from twitterapiv2.model.recent import Data

URL = "https://api.twitter.com/2/tweets"


class TweetsLookup(ClientCore):
    def __init__(self, application_auth: ApplicationAuth) -> None:
        """Lookup information about Tweet(s) specified by requested ID(s)."""
        super().__init__(AppAuthClient(application_auth))

        # Define field builder methods
        self.expansions = self.field_builder.expansions
        self.media_fields = self.field_builder.media_fields
        self.place_fields = self.field_builder.place_fields
        self.poll_fields = self.field_builder.poll_fields
        self.tweet_fields = self.field_builder.tweet_fields
        self.user_fields = self.field_builder.user_fields
        self.ids = self.field_builder.ids

    def fetch(self) -> list[Data]:
        """
        Return information about Tweet(s) specified by requested ID(s).

        TweetsLookup.ids("") is a required field. A maximum of 100 IDs can
        be provided. There is no pagination for this client.
        """
        if not self.fields.get("ids"):
            raise ValueError(".ids() is a required field to be defined.")
        results = self.get(URL)
        return results.get("data") or []
