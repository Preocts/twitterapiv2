from datetime import datetime
from typing import NamedTuple
from unittest.mock import MagicMock

import pytest
from twitterapiv2.client_intrfc import ClientIntrfc
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.model.httpresponse import HTTPResponse
from twitterapiv2.model.responseheader import ResponseHeader


def test_default_values() -> None:
    client = ClientIntrfc()
    assert client.limit_remaining == -1
    assert client.limit_reset is not None


def test_properties() -> None:
    client = ClientIntrfc()
    mock_resp = HTTPResponse(None)
    mock_headers = ResponseHeader()
    mock_headers.x_rate_limit_remaining = "10"
    mock_headers.x_rate_limit_reset = "1637818406"
    mock_resp._response_headers = mock_headers

    reset = datetime.utcfromtimestamp(1637818406)

    client._last_response = mock_resp

    assert client.limit_remaining == 10
    assert client.limit_reset == reset


def test_more() -> None:
    client = ClientIntrfc()
    assert not client.more
    client._next_token = "not null"
    assert client.more


def test_fields() -> None:
    client = ClientIntrfc()
    assert not len(client.fields)

    client.field_builder._fields = {
        "Valid": "Hello",
        "Invalid": None,
    }

    assert "Valid" in client.fields
    assert "Invalid" not in client.fields


def test_fetch_not_implemented() -> None:
    client = ClientIntrfc()
    with pytest.raises(NotImplementedError):
        client.fetch()


class MockReponse(NamedTuple):
    status: int = 200
    body: str = ""
    response_headers: MagicMock = MagicMock()


def test_response_handling_429() -> None:
    mock_resp = MockReponse(429, "")
    client = ClientIntrfc()
    with pytest.raises(ThrottledError):
        client.raise_on_response("https://", mock_resp)


def test_response_handling_401() -> None:
    mock_resp = MockReponse(401, "")
    client = ClientIntrfc()
    with pytest.raises(InvalidResponseError):
        client.raise_on_response("https://", mock_resp)


def test_response_handing_200() -> None:
    mock_resp = MockReponse(200, "")
    client = ClientIntrfc()
    client.raise_on_response("https://", mock_resp)
