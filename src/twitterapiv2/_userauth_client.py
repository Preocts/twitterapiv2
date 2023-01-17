"""
User Auth client for obtaining and managing OAuth2 bearer token for v2 API

https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
"""
from __future__ import annotations

import base64
import hashlib
import logging
import os
import re

from authlib.integrations.httpx_client import OAuth2Client  # type: ignore  # no stubs
from twitterapiv2._auth_client import AuthClient
from twitterapiv2.model.client_auth import ClientAuth

TWITTER_AUTH = "https://twitter.com/i/oauth2/authorize"
TWITTER_TOKEN = "https://api.twitter.com/2/oauth2/token"

# TODO:
#   track expiry on bearer token
#   handle reauth request
#   handle revoke request


class UserAuthClient(AuthClient):

    logger = logging.getLogger(__name__)

    def __init__(self, auth_model: ClientAuth, scopes: list[str]) -> None:
        """Provide ClientAuth model for authentication."""
        self._keys = auth_model
        self._scopes = scopes
        self._bearer: str | None = None

    def get_bearer(self) -> str | None:
        """Aquire bearer token from Twitter, or return current."""
        if not self._bearer:
            self._get_bearer_token()
        return self._bearer

    def _get_bearer_token(self) -> None:
        """Get bearer token."""
        code_verifier = self._code_verifier()

        oauth = self._oauth2_client()

        auth_url, _ = oauth.create_authorization_url(
            url=TWITTER_AUTH,
            code_verifier=code_verifier,
            code_challenge=self._code_challenge(code_verifier),
            code_challenge_method="S256",
        )

        auth_response = self._get_authorization_response(auth_url)

        token = oauth.fetch_token(
            url=TWITTER_TOKEN,
            grant_type="authorization_code",
            authorization_response=auth_response,
            code_verifier=code_verifier,
        )

        self._bearer = token.get("access_token")

    def _oauth2_client(self) -> OAuth2Client:
        """Create oauth client."""
        return OAuth2Client(
            client_id=self._keys.client_id,
            client_secret=self._keys.client_secret,
            scope=self._scopes,
            redirect_uri=self._keys.redirect_uri,
        )

    @staticmethod
    def _get_authorization_response(auth_url: str) -> str:
        print("Click the following URL to authorize this app on your behalf:")
        print(auth_url)
        return input("Enter the full uri after accepting: ")

    @staticmethod
    def _code_verifier() -> str:
        """Create a code verifier."""
        code_verifier = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8")
        return re.sub("[^a-zA-Z0-9]+", "", code_verifier)

    @staticmethod
    def _code_challenge(code_verifier: str) -> str:
        """Create a code challenge."""
        code_byte = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        code_challenge = base64.urlsafe_b64encode(code_byte).decode("utf-8")
        return code_challenge.replace("=", "")
