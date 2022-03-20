"""
Application auth client for obtaining and managing OAuth bearer token for v2 API

https://developer.twitter.com/en/docs/authentication/oauth-2-0/application-only
"""
from __future__ import annotations

import logging
import os
from base64 import b64encode
from typing import Any
from urllib import parse

from twitterapiv2.http_client import HTTPClient


class AppAuthClient:
    """
    Authentication requires the following environment variables exist:
        TW_CONSUMER_KEY
        TW_CONSUMER_SECRET

    A 'TW_BEARER_TOKEN' will be created in the environment on successful
    authentication. This key should be stored securely and loaded to the
    environment on subsequent calls. When this token already exists, the
    request for a bearer token can be skipped.
    """

    twitter_api = "https://api.twitter.com"

    def __init__(self) -> None:
        self.http = HTTPClient()
        self.log = logging.getLogger(__name__)

    def encoded_credentials(self) -> str:
        """Creates an encoded bear token credential string"""
        key = os.getenv("TW_CONSUMER_KEY", None)
        secret = os.getenv("TW_CONSUMER_SECRET", None)

        if key is None or secret is None:
            raise KeyError("Missing one or both consumer environment variables!")

        key = parse.quote_plus(key)
        secret = parse.quote_plus(secret)
        union = ":".join([key, secret]).encode()
        return b64encode(union).decode()

    def set_bearer_token(self) -> None:
        """Fetches bearer token, setting it to `TW_BEARER_TOKEN` in environment"""
        os.environ["TW_BEARER_TOKEN"] = self.fetch_bearer_token()
        self.log.debug("Bearer token loaded to 'TW_BEARER_TOKEN'")

    def fetch_bearer_token(self) -> str:
        """Return bearer token for Twitter API v2"""
        # Twitter does not frequently auto-expire bearer tokens. This will not
        # return a new (changed) bearer once one is granted until that token
        # is revoked.
        self.log.debug("Requesting bearer token with consumer credentials...")
        url = self.twitter_api + "/oauth2/token"
        fields = {"grant_type": "client_credentials"}

        result = self._post_request(url=url, fields=fields)

        if result.get("token_type", "") != "bearer":
            self.log.error(result)
            raise ValueError(f"Invalid token_type: '{result.get('token_type')}'")

        if not result.get("access_token"):
            self.log.error(result)
            raise ValueError("No bearer token returned")

        return result["access_token"]

    # def revoke_bearer_token(self) -> None:
    #     """Revoke and delete token in `TW_BEARER_TOKEN` environ variable"""
    #     raise NotImplementedError("Twitter functionality missing. Use the dashboard!")
    #     token = os.getenv("TW_BEARER_TOKEN")
    #     if not token:
    #         raise ValueError(f"No bearer token loaded: TW_BEARER_TOKEN={token}")

    #     url = self.TWITTER_API + "/oauth2/invalidate_token"
    #     fields = {"access_token": token}
    #     result = self._post_request(url=url, fields=fields)

    #     if "access_token" not in result or result.get("access_token") != token:
    #         self.log.error("Unexpected response: '%s'", result)
    #         raise ValueError("Unexpected response! Token may still be active.")

    def _post_request(self, url: str, fields: dict[str, str]) -> dict[str, Any]:
        """Internal use: makes validate and invalidate calls, returns result"""
        headers = {
            "Content-Type": "applicaton/x-www-form-urlencoded;charset=UTF-8",
            "Authorization": "Basic " + self.encoded_credentials(),
        }
        resp = self.http.post(
            url=url,
            body=fields,
            headers=headers,
            urlencode=True,
        )

        return resp.get_json() or {} if resp.has_success() else {}
