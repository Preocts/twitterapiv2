"""Core class inherited by client classes."""
from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from http_overeasy.http_client import HTTPClient
from http_overeasy.response import Response
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.fields import Fields
from twitterapiv2.model.responseheader import ResponseHeader


_BEARER_TOKEN = "TW_BEARER_TOKEN"


class ClientCore:
    def __init__(self) -> None:
        """Define a ClientCore, contains `.field_builder()` and http client."""
        self.field_builder = Fields()
        self.http = HTTPClient()
        self._last_response: Response | None = None
        self._next_token: str | None = None

    @property
    def limit_remaining(self) -> int:
        """Number of calls remaining before next limit reset."""
        if self._last_response is None:
            return -1
        last_headers = ResponseHeader.build_from(self._last_response.get_headers())
        return int(last_headers.x_rate_limit_remaining)

    @property
    def limit_reset(self) -> datetime:
        """Datetime of next limit reset as UTC unaware datetime."""
        if self._last_response is None:
            return datetime.now()
        last_headers = ResponseHeader.build_from(self._last_response.get_headers())
        return datetime.utcfromtimestamp(int(last_headers.x_rate_limit_reset))

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
        return {"Authorization": "Bearer " + os.getenv(_BEARER_TOKEN, "")}

    def get(self, url: str) -> dict[str, Any]:
        """
        Send GET request to url with defined fields encoded into URL.

        Args:
            url: Target Twitter API URL

        Returns:
            JSON response as dict[str, Any]
        """
        self._last_response = self.http.get(url, self.fields, self.headers)
        self.raise_on_response(url, self._last_response)
        json_body = self._last_response.get_json() or {}
        meta = json_body.get("meta")
        self._next_token = meta.get("next_token") if meta else None
        return json_body

    def fetch(self) -> Any:
        """Override with specific implementation"""
        raise NotImplementedError

    def raise_on_response(self, url: str, resp: Response) -> None:
        """
        Custom handling for Twitter status codes.

        Args:
            url: url response came from
            resp: Response object

        Returns:
            None
        """
        if resp.get_status() == 429:
            rst = resp.get_headers().x_rate_limit_reset
            raise ThrottledError(f"Throttled until '{rst}'")
        if not (200 <= resp.get_status() < 300):
            raise InvalidResponseError(
                f"{resp.get_status()}: {url} - '{resp.get_body()}"
            )
