from __future__ import annotations

from datetime import datetime

import pytest
from httpx import Response
from twitterapiv2.client_core import ClientCore
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError

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

MOCK_RESPONSE = Response(200, content=BODY, headers=HEADERS)


def test_default_values() -> None:
    client = ClientCore()
    assert client.limit_remaining == -1
    assert client.limit_reset is not None


def test_properties() -> None:
    client = ClientCore()
    expected_remaining = MOCK_RESPONSE.headers["x-rate-limit-remaining"]
    reset = MOCK_RESPONSE.headers["x-rate-limit-reset"]
    expected_reset = datetime.utcfromtimestamp(int(reset))
    client._last_response = MOCK_RESPONSE

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


def test_response_handling_429() -> None:
    mock_resp = Response(429, headers=HEADERS)
    client = ClientCore()
    with pytest.raises(ThrottledError):
        client.raise_on_response("https://", mock_resp)


def test_response_handling_401() -> None:
    mock_resp = Response(401, headers=HEADERS)
    client = ClientCore()
    with pytest.raises(InvalidResponseError):
        client.raise_on_response("https://", mock_resp)


def test_response_handling_invalid() -> None:
    mock_resp = Response(42, headers=HEADERS)
    client = ClientCore()
    with pytest.raises(InvalidResponseError):
        client.raise_on_response("https://", mock_resp)


def test_response_handing_200() -> None:
    mock_resp = Response(200, headers=HEADERS)
    client = ClientCore()
    client.raise_on_response("https://", mock_resp)
