"""
Get a user's liked tweets or a tweet's liking users. Like or unlike a tweet.

https://developer.twitter.com/en/docs/twitter-api/tweets/manage-tweets/introduction
"""
from __future__ import annotations

from typing import Any

from twitterapiv2._auth_client import AuthClient
from twitterapiv2.client_core import ClientCore

URL_BASE = "https://api.twitter.com/2/users"


class Likes(ClientCore):
    """Get a user's liked tweets or a tweet's liking users. Like or unlike a tweet."""

    scopes = ["tweet.read", "tweet.write", "users.read"]

    def __init__(self, auth_client: AuthClient) -> None:
        """Create a Likes client."""
        super().__init__(auth_client)
        self._url = URL_BASE
        self._user_id: str | None = None

    @property
    def user_id(self) -> str:
        """Get the user id."""
        if self._user_id is None:
            self._user_id = self.get_user().id
        return self._user_id

    def unlike(self, tweet_id: str) -> bool:
        """Unlike a tweet."""
        url = f"{self._url}/{self.user_id}/likes/{tweet_id}"
        return self.unlike(url)

    def like(self, tweet_id: str) -> bool:
        """Like a tweet."""
        url = f"{self._url}/{self.user_id}/likes"
        payload = {"tweet_id": tweet_id}
        return self.post(url, payload)

    # TODO: Add support for fields
    def get_likes(self) -> Any:
        """Get a user's liked tweets."""
        url = f"{self._url}/{self.user_id}/liked_tweets"
        return self.get(url)

    # TODO: Add support for fields
    def get_liking_users(self, tweet_id: str) -> Any:
        """Get a tweet's liking users."""
        url = f"https://api.twitter.com/2/tweets/{tweet_id}/liking_users"
        return self.get(url)
