from datetime import datetime
from unittest.mock import MagicMock

import pytest
from twitterapiv2.client_core import ClientCore
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.model.response import Response

from tests.response_test import MOCK_RESPONSE


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
