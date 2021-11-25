from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.fields import Fields
from twitterapiv2.http import Http


class ClientIntrfc:
    def __init__(self) -> None:
        super().__init__()
        self.field_builder = Fields()
        self.http = Http()
        self._next_token: Optional[str] = None

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

    def get(self, url: str) -> Dict[str, Any]:
        """Sends a GET request to url with defined fields encoded into URL"""
        result = self.http.get(url, self.fields)
        meta = result.get("meta")
        self._next_token = meta.get("next_token") if meta else None
        return result

    def fetch(self) -> Any:
        """Override with specific implementation"""
        raise NotImplementedError
