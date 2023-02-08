"""
Application auth client for obtaining and managing OAuth bearer token for v2 API

https://developer.twitter.com/en/docs/authentication/oauth-2-0/application-only
"""
from __future__ import annotations

import logging
from base64 import b64encode
from typing import Any
from urllib import parse

import httpx
from twitterapiv2._auth_client import AuthClient
from twitterapiv2.model.application_auth import ApplicationAuth


class AppAuthClient(AuthClient):
    logger = logging.getLogger(__name__)

    twitter_api = "https://api.twitter.com"

    def __init__(self, auth_model: ApplicationAuth, scopes: list[str]) -> None:
        """Provide ApplicatoinAuth model for authentication."""
        self.http = httpx.Client()
        self._keys = auth_model
        self._scopes = scopes.copy()

    def get_bearer(self) -> str | None:
        """Aquire bearer token from Twitter, or return current."""
        if not self._keys.consumer_bearer:
            self._get_bearer_token()
        return self._keys.consumer_bearer

    def _encoded_credentials(self) -> str:
        """Create encoded token credential string."""
        if not self._keys.consumer_key or not self._keys.consumer_secret:
            raise KeyError("Missing one or both consumer environment variables!")

        key = parse.quote_plus(self._keys.consumer_key)
        secret = parse.quote_plus(self._keys.consumer_secret)
        union = ":".join([key, secret]).encode()
        return b64encode(union).decode()

    def _get_bearer_token(self) -> None:
        """Get bearer token for Twitter API v2, uses provided if exists."""
        # Twitter does not frequently auto-expire bearer tokens. This will not
        # return a new (changed) bearer once one is granted until that token
        # is revoked.
        self.logger.debug("Requesting bearer token with consumer credentials")
        url = self.twitter_api + "/oauth2/token"
        fields = {"grant_type": "client_credentials"}

        result = self._post_request(url=url, fields=fields)

        if "token_type" not in result or "access_token" not in result:
            self.logger.debug("Invalid response: %s", result)
            raise ValueError("Unexpected Authentication response.")

        self._keys.consumer_bearer = result["access_token"]

    def _post_request(self, url: str, fields: dict[str, str]) -> dict[str, Any]:
        """Internal use: makes validate and invalidate calls, returns result"""
        headers = {
            "Content-Type": "applicaton/x-www-form-urlencoded;charset=UTF-8",
            "Authorization": "Basic " + self._encoded_credentials(),
        }
        resp = self.http.post(url=url, params=fields, headers=headers)

        return resp.json() if resp.is_success else {}
