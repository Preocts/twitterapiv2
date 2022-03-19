from __future__ import annotations

import json
from typing import Any

from urllib3.response import HTTPResponse

HEADERS = {
    "api-version": "2.30",
    "cache-control": "no-cache, no-store, max-age=0",
    "content-disposition": "attachment; filename=json.json",
    "content-length": "15255",
    "content-type": "application/json; charset=utf-8",
    "date": "Sun, 21 Nov 2021 21:33:28 UTC",
    "server": "tsa_b",
    "set-cookie": "guest_id_marketing=v1%3A163753040803940976; Max-Age=63072000; Expires=Tue, 21 Nov 2023 21:33:28 GMT; Path=/; Domain=.twitter.com; Secure; SameSite=None"  # noqa E501
    "guest_id_ads=v1%3A163753040803940976; Max-Age=63072000; Expires=Tue, 21 Nov 2023 21:33:28 GMT; Path=/; Domain=.twitter.com; Secure; SameSite=None"  # noqa E501
    'personalization_id="v1_kZV0Xt7vrXTZYjZvjI3jhg=="; Max-Age=63072000; Expires=Tue, 21 Nov 2023 21:33:28 GMT; Path=/; Domain=.twitter.com; Secure; SameSite=None'  # noqa E501
    "guest_id=v1%3A163753040803940976; Max-Age=63072000; Expires=Tue, 21 Nov 2023 21:33:28 GMT; Path=/; Domain=.twitter.com; Secure; SameSite=None",  # noqa E501
    "strict-transport-security": "max-age=631138519",
    "x-access-level": "read",
    "x-connection-hash": "ed3dcd3858df7ca27da8474b444d508a63f97eb01bafcaa23f0cea0148735f30",  # noqa E501
    "x-content-type-options": "nosniff",
    "x-frame-options": "SAMEORIGIN",
    "x-rate-limit-limit": "300",
    "x-rate-limit-remaining": "299",
    "x-rate-limit-reset": "1637531308",
    "x-response-time": "157",
    "x-xss-protection": "0",
}


class MockHTTP:
    def __init__(self) -> None:
        self._urls: list[str] = []
        self._responses: list[dict[str, Any] | str] = []
        self._status: list[int]

    def add(self, url: str, response: dict[str, Any] | str, status: int) -> None:
        """Add response to mock. They will be replayed in order of creation"""
        self._urls.append(url)
        self._responses.append(response)
        self._status.append(status)

    def _check_call(self, **kwargs: Any) -> HTTPResponse | None:
        """Check that url is expected, return response or None"""
        resp = HTTPResponse(
            body=json.dumps(self._responses.pop(0)).encode(),
            headers=HEADERS,
            status=self._status.pop(0),
        )
        url = self._urls.pop(0)
        return resp if kwargs.get("url", "") == url else None

    def get(self, **kwargs: Any) -> None:
        """Mocks http_client method"""
        self._check_call(**kwargs)

    def put(self, **kwargs: Any) -> None:
        """Mocks http_client method"""
        self._check_call(**kwargs)

    def post(self, **kwargs: Any) -> None:
        """Mocks http_client method"""
        self._check_call(**kwargs)

    def patch(self, **kwargs: Any) -> None:
        """Mocks http_client method"""
        self._check_call(**kwargs)

    def delete(self, **kwargs: Any) -> None:
        """Mocks http_client method"""
        self._check_call(**kwargs)
