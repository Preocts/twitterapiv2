import json
import logging
from typing import Any
from typing import Dict
from typing import Optional

import urllib3
from twitterapiv2.model.httpresponse import HTTPResponse


class Http:
    """
    Provides HTTPS connection pool and REST methods

    Raises:
        ThrottledError - Raise on 429 Throttle error
        InvalidResponseError - Raised on all other failed status codes
    """

    def __init__(self, num_pools: int = 10) -> None:
        self.log = logging.getLogger(__name__)
        self.http = self.connection(num_pools)

    def connection(self, num_pools: int = 10) -> urllib3.PoolManager:
        """Returns HTTP pool manager with retries and backoff"""
        return urllib3.PoolManager(
            num_pools=num_pools,
            retries=urllib3.Retry(
                total=3,
                backoff_factor=2,
                raise_on_status=False,
                raise_on_redirect=True,
                status_forcelist=[500, 502, 503, 504],
                allowed_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            ),
        )

    def get(
        self,
        url: str,
        fields: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> HTTPResponse:
        """GET method with HTTPResponse model returned"""
        resp = HTTPResponse(
            self.http.request(
                method="GET",
                url=url,
                fields=fields,
                headers=headers,
            )
        )
        return resp

    def post(
        self,
        url: str,
        payload: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> HTTPResponse:
        """POST method with HTTPResponse model returned"""
        resp = HTTPResponse(
            self.http.request(
                method="POST",
                url=url,
                body=json.dumps(payload),
                headers=headers,
            )
        )
        return resp

    def put(self) -> None:
        """Override for specific implementations"""
        raise NotImplementedError  # pragma: no cover

    def patch(self) -> None:
        """Override for specific implementations"""
        raise NotImplementedError  # pragma: no cover

    def delete(self) -> None:
        """Override for specific implementations"""
        raise NotImplementedError  # pragma: no cover
