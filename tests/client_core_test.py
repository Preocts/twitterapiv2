from __future__ import annotations

from datetime import datetime
from unittest.mock import MagicMock

import pytest
from http_overeasy.http_client import urllib3
from http_overeasy.response import Response
from twitterapiv2.client_core import ClientCore
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError

HTTPResponse = urllib3.HTTPResponse


BODY = b'{"data":[{"id":"1461880347478528007","text":"MOCK"}]}'
HEADERS = {
    "api-version": "2.30",
    "cache-control": "no-cache, no-store, max-age=0",
    "content-disposition": " attachment; filename=json.json",
    "content-length": "248",
    "content-type": "application/json; charset=utf-8",
    "date": "Fri, 26 Nov 2021 09:04:24 UTC",
    "server": "tsa_b",
    "set-cookie": "",
    "strict-transport-security": "max-age=631138519",
    "x-access-level": "read",
    "x-connection-hash": "025826e4ff9a90bd701f81d6380501dd64c46f17c69ca21dec15a7c52",
    "x-content-type-options": "nosniff",
    "x-frame-options": "SAMEORIGIN",
    "x-rate-limit-limit": "300",
    "x-rate-limit-remaining": "297",
    "x-rate-limit-reset": "1637917876",
    "x-response-time": "62",
    "x-xss-protection": "0",
}

MOCK_RESPONSE = HTTPResponse(body=BODY, headers=HEADERS, status=200)


def test_default_values() -> None:
    client = ClientCore()
    assert client.limit_remaining == -1
    assert client.limit_reset is not None


def test_properties() -> None:
    client = ClientCore()
    expected_remaining = MOCK_RESPONSE.headers["x-rate-limit-remaining"]
    reset = MOCK_RESPONSE.headers["x-rate-limit-reset"]
    expected_reset = datetime.utcfromtimestamp(int(reset))
    mock_resp = Response(MOCK_RESPONSE)
    client._last_response = mock_resp

    assert client.limit_remaining == int(expected_remaining)
    assert client.limit_reset == expected_reset


def test_more() -> None:
    client = ClientCore()
    assert not client.more
    client._next_token = "not null"
    assert client.more


def test_fields() -> None:
    client = ClientCore()
    assert not len(client.fields)

    client.field_builder._fields = {
        "Valid": "Hello",
        "Invalid": None,
    }

    assert "Valid" in client.fields
    assert "Invalid" not in client.fields


def test_fetch_not_implemented() -> None:
    client = ClientCore()
    with pytest.raises(NotImplementedError):
        client.fetch()


class MockReponse:
    def __init__(self, status: int, body: str) -> None:
        self.status = status
        self.body = body
        self.response_headers = MagicMock()

    def get_status(self) -> int:
        return self.status

    def get_body(self) -> str:
        return self.body

    def get_headers(self) -> MagicMock:
        return self.response_headers


def test_response_handling_429() -> None:
    mock_resp = MockReponse(429, "")
    client = ClientCore()
    with pytest.raises(ThrottledError):
        client.raise_on_response("https://", mock_resp)


def test_response_handling_401() -> None:
    mock_resp = MockReponse(401, "")
    client = ClientCore()
    with pytest.raises(InvalidResponseError):
        client.raise_on_response("https://", mock_resp)


def test_response_handling_invalid() -> None:
    mock_resp = MockReponse(42, "")
    client = ClientCore()
    with pytest.raises(InvalidResponseError):
        client.raise_on_response("https://", mock_resp)


def test_response_handing_200() -> None:
    mock_resp = MockReponse(200, "")
    client = ClientCore()
    client.raise_on_response("https://", mock_resp)
