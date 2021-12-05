import json
from typing import Any
from typing import Dict
from typing import Optional

from twitterapiv2.model.responseheader import ResponseHeader


class HTTPResponse:
    """Models urllib3 response objects"""

    def __init__(self, response: Any) -> None:
        """Models urllib3 response object"""
        self._response = response
        self._response_headers: Optional[ResponseHeader] = None
        self._body: Optional[str] = None
        self._status: Optional[int] = None

    @property
    def response_headers(self) -> ResponseHeader:
        """Models Twitter API response headers"""
        if self._response_headers is None:
            self._response_headers = ResponseHeader.build_from(self._response)
        return self._response_headers

    @property
    def status(self) -> int:
        """Status code response"""
        if self._status is None:
            self._status = self._response.status
        return self._status

    @property
    def has_success(self) -> bool:
        """Was the status code successful"""
        return self.status in range(200, 300)

    @property
    def body(self) -> str:
        """Response body decoded in UTF-8"""
        if self._body is None:
            self._body = self._response.data.decode("utf-8")
        return self._body

    @property
    def json(self) -> Dict[str, Any]:
        """Response body as a dictionary. Will raise on decode error."""
        return json.loads(self.body)

    @property
    def error(self) -> str:
        """Returns body containing error, same as `body`"""
        return self.body
