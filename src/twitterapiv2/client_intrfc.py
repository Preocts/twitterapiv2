import os
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.fields import Fields
from twitterapiv2.http_client import HTTPClient
from twitterapiv2.model.response import Response


_BEARER_TOKEN = "TW_BEARER_TOKEN"


class ClientIntrfc:
    def __init__(self) -> None:
        self.field_builder = Fields()
        self.http = HTTPClient()
        self._last_response: Optional[Response] = None
        self._next_token: Optional[str] = None

    @property
    def limit_remaining(self) -> int:
        """Number of calls remaining before next limit reset"""
        if self._last_response is None:
            return -1
        return int(self._last_response.get_headers().x_rate_limit_remaining)

    @property
    def limit_reset(self) -> datetime:
        """Datetime of next limit reset as UTC unaware datetime"""
        if self._last_response is None:
            return datetime.now()
        ts = int(self._last_response.get_headers().x_rate_limit_reset)
        return datetime.utcfromtimestamp(ts)

    @property
    def fields(self) -> Dict[str, Any]:
        """Returns fields that have been defined (removed NoneTypes)"""
        fields = self.field_builder.fields
        fields["next_token"] = self._next_token
        return {key: value for key, value in fields.items() if value}

    @property
    def more(self) -> bool:
        """True if more pages exist. Always starts as False"""
        return bool(self._next_token)

    @property
    def headers(self) -> Dict[str, str]:
        """Build headers with TW_BEARER_TOKEN from environ"""
        return {"Authorization": "Bearer " + os.getenv(_BEARER_TOKEN, "")}

    def get(self, url: str) -> Dict[str, Any]:
        """Sends a GET request to url with defined fields encoded into URL"""
        self._last_response = self.http.get(url, self.fields, self.headers)
        self.raise_on_response(url, self._last_response)
        json_body = self._last_response.get_json() or {}
        meta = json_body.get("meta")
        self._next_token = meta.get("next_token") if meta else None
        return json_body

    def fetch(self) -> Any:
        """Override with specific implementation"""
        raise NotImplementedError  # pragma: no cover

    def raise_on_response(self, url: str, resp: Response) -> None:
        """Custom handling for Twitter status codes"""
        if resp.get_status() == 429:
            rst = resp.get_headers().x_rate_limit_reset
            raise ThrottledError(f"Throttled until '{rst}'")
        if not (200 <= resp.get_status() < 300):
            raise InvalidResponseError(
                f"{resp.get_status()}: {url} - '{resp.get_body()}"
            )
