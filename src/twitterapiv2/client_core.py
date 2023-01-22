"""Core class inherited by client classes."""
from __future__ import annotations

from datetime import datetime
from typing import Any

import httpx
from twitterapiv2._appauth_client import AppAuthClient
from twitterapiv2._auth_client import AuthClient
from twitterapiv2._userauth_client import UserAuthClient
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.fields import Fields
from twitterapiv2.model.application_auth import ApplicationAuth
from twitterapiv2.model.client_auth import ClientAuth


class ClientCore:
    scopes: list[str] = []

    def __init__(self, auth_client: AuthClient) -> None:
        """Define a ClientCore, contains `.field_builder()` and http client."""
        self.http = httpx.Client()
        self.field_builder = Fields()
        self.auth_client = auth_client
        self._last_response: httpx.Response | None = None
        self._next_token: str | None = None

    @classmethod
    def from_model(cls, auth_model: ApplicationAuth | ClientAuth) -> ClientCore:
        """Build with auth client respective of auth model provided."""
        if isinstance(auth_model, ApplicationAuth):
            return cls(AppAuthClient(auth_model, ClientCore.scopes))
        elif isinstance(auth_model, ClientAuth):
            return cls(UserAuthClient(auth_model, ClientCore.scopes))
        else:
            raise ValueError(f"Unknown auth model type: {type(auth_model).__name__}")

    @property
    def limit_remaining(self) -> int:
        """Number of calls remaining before next limit reset."""
        if self._last_response is None:
            return -1
        return int(self._last_response.headers["x-rate-limit-remaining"])

    @property
    def limit_reset(self) -> datetime:
        """Datetime of next limit reset as UTC unaware datetime."""
        if self._last_response is None:
            return datetime.now()
        rst = self._last_response.headers["x-rate-limit-reset"]
        return datetime.utcfromtimestamp(int(rst))

    @property
    def fields(self) -> dict[str, Any]:
        """Field values that have been defined. (removes 'None' values)"""
        fields = self.field_builder.fields
        fields["next_token"] = self._next_token
        return {key: value for key, value in fields.items() if value}

    @property
    def more(self) -> bool:
        """True if more pages exist, default is False."""
        return bool(self._next_token)

    @property
    def headers(self) -> dict[str, str]:
        """Build headers with TW_BEARER_TOKEN from environ."""
        return {"Authorization": f"Bearer {self.auth_client.get_bearer()}"}

    def get(self, url: str) -> Any:
        """
        Send GET request to url with defined fields encoded into URL.

        Args:
            url: Target Twitter API URL

        Returns:
            JSON response as Any
        """
        self._last_response = self.http.get(
            url=url,
            params=self.fields,
            headers=self.headers,
        )
        self.raise_on_response(url, self._last_response)
        json_body = self._last_response.json()
        meta = json_body.get("meta")
        self._next_token = meta.get("next_token") if meta else None
        return json_body

    def post(self, url: str, json: dict[str, Any]) -> Any:
        """
        Send POST request to url with defined fields encoded into URL.

        Args:
            url: Target Twitter API URL
            json: JSON body to send

        Returns:
            JSON response as Any
        """
        self._last_response = self.http.post(url=url, headers=self.headers, json=json)
        self.raise_on_response(url, self._last_response)
        return self._last_response.json()

    def delete(self, url: str) -> Any:
        """
        Send DELETE request to url with defined fields encoded into URL.

        Args:
            url: Target Twitter API URL

        Returns:
            JSON response as Any
        """
        self._last_response = self.http.delete(url=url, headers=self.headers)
        self.raise_on_response(url, self._last_response)
        return self._last_response.json()

    def fetch(self) -> Any:
        """Override with specific implementation"""
        raise NotImplementedError

    def raise_on_response(self, url: str, resp: httpx.Response) -> None:
        """
        Custom handling for Twitter status codes.

        Args:
            url: url response came from
            resp: Response object

        Returns:
            None
        """
        if resp.status_code == 429:
            rst = resp.headers["x-rate-limit-reset"]
            raise ThrottledError(f"Throttled until '{rst}'")
        if not (200 <= resp.status_code < 300):
            raise InvalidResponseError(f"{resp.status_code}: {url} - '{resp.text}")
