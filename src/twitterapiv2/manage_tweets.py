from __future__ import annotations

from typing import Any

from twitterapiv2._auth_client import AuthClient
from twitterapiv2.client_core import ClientCore
from twitterapiv2.model.tweet import Tweet

URL_BASE = "https://api.twitter.com/2/tweets"


class ManageTweets(ClientCore):
    scopes = ["tweet.read", "tweet.write", "users.read", "offline.access"]

    def __init__(self, auth_client: AuthClient) -> None:
        """Create a ManageTweets client for sending and deleting Tweets."""
        super().__init__(auth_client)
        self._url = URL_BASE

    def new_tweet(self, *, auto_truncate: bool = False) -> Tweet:
        """Create a new Tweet object."""
        return Tweet(auto_truncate=auto_truncate)

    def send_tweet(self, tweet: Tweet) -> dict[str, Any]:
        """Send a Tweet."""
        return self.post(self._url, json=tweet.data)

    def delete_tweet(self, tweet_id: str) -> dict[str, Any]:
        """Delete a Tweet."""
        return self.delete(f"{self._url}/{tweet_id}")
