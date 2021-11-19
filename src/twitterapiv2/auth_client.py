"""
Application auth client for obtaining and managing OAuth bearer token for v2 API

https://developer.twitter.com/en/docs/authentication/oauth-2-0/application-only
"""
import logging
import os
from base64 import b64encode
from urllib import parse

from twitterapiv2.http import Http


class AuthClient(Http):
    """
    Authentication requires the following environment variables exist:
        TW_CONSUMER_KEY
        TW_CONSUMER_SECRET

    A 'TW_BEARER_TOKEN' will be created in the environment on successful
    authentication. This key should be stored securely and loaded to the
    environment on subsequent calls. When this token already exists, the
    request for a bearer token can be skipped.
    """

    TWITTER_API = "https://api.twitter.com"

    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self.http = super().connection()

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
        """Set the `TW_BEARER_TOKEN` environment variable"""
        # Twitter does not frequently auto-expire bearer tokens. This will not
        # return a new (changed) bearer once one is granted until that token
        # is revoked.
        self.log.debug("Requesting bearer token with consumer credentials...")
        headers = {
            "Content-Type": "applicaton/x-www-form-urlencoded;charset=UTF-8",
            "Authorization": "Basic " + self.encoded_credentials(),
        }
        fields = {"grant_type": "client_credentials"}
        url = self.TWITTER_API + "/oauth2/token"

        # Override urllib3's preference to encode body on POST
        resp = self.http.request_encode_url(
            "POST",
            url=url,
            fields=fields,
            headers=headers,
        )
        result = super()._data2dict(resp.data)

        if result.get("token_type", "") != "bearer":
            self.log.error(result)
            raise ValueError(f"Invalid token_type: '{result.get('token_type')}'")

        if not result.get("access_token"):
            self.log.error(result)
            raise ValueError("No bearer token returned")

        os.environ["TW_BEARER_TOKEN"] = result.get("access_token", "")
        self.log.debug("Bearer token loaded to 'TW_BEARER_TOKEN'")
