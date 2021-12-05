import os
from datetime import datetime
from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.fields import Fields
from twitterapiv2.http import Http

_BEARER_TOKEN = "TW_BEARER_TOKEN"


class ClientIntrfc:
    def __init__(self) -> None:
        super().__init__()
        self.field_builder = Fields()
        self.http = Http()
        self._next_token: Optional[str] = None

    @property
    def limit_remaining(self) -> int:
        """Number of calls remaining before next limit reset"""
        if self.http.last_response is None:
            return -1
        else:
            return int(self.http.last_response.x_rate_limit_remaining)

    @property
    def limit_reset(self) -> datetime:
        """Datetime of next limit reset as UTC unaware datetime"""
        if self.http.last_response is None:
            return datetime.now()
        else:
            ts = int(self.http.last_response.x_rate_limit_reset)
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
        result = self.http.get(url, self.fields, self.headers)
        meta = result.get("meta")
        self._next_token = meta.get("next_token") if meta else None
        return result

    def fetch(self) -> Any:
        """Override with specific implementation"""
        raise NotImplementedError  # pragma: no cover
