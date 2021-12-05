import json
from typing import NamedTuple
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
import vcr
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.http import Http


api_recorder = vcr.VCR(
    filter_headers=["Authorization"],
    record_mode="ONCE",
    cassette_library_dir="tests/cassettes/http",
)


class MockReponse(NamedTuple):
    status: int
    data: bytes


def test_data2dict() -> None:
    client = Http()
    good_data = b'{"test": "value"}'
    bad_data = b"error data"
    assert client.data2dict(good_data) == {"test": "value"}
    assert client.data2dict(bad_data) == {"error": bad_data}


def test_response_handling_429() -> None:
    mock_resp = MockReponse(429, b"")
    client = Http()
    with pytest.raises(ThrottledError):
        client.raise_on_response(mock_resp, "")


def test_response_handling_401() -> None:
    mock_resp = MockReponse(401, b"")
    client = Http()
    with pytest.raises(InvalidResponseError):
        client.raise_on_response(mock_resp, "")


def test_response_handing_200() -> None:
    mock_resp = MockReponse(200, b"")
    client = Http()
    client.raise_on_response(mock_resp, "")


@api_recorder.use_cassette()
def test_last_response_headers() -> None:
    client = Http()
    fields = {"max_results": 10, "query": "test"}

    client.get("https://api.twitter.com/2/tweets/search/recent", fields)
    assert client.last_response
    assert client.last_response.x_rate_limit_remaining
    assert client.last_response.x_rate_limit_reset

    remaining = client.last_response.x_rate_limit_remaining
    reset = client.last_response.x_rate_limit_reset
    client.get("https://api.twitter.com/2/tweets/search/recent", fields)
    assert client.last_response
    assert client.last_response.x_rate_limit_remaining == str(int(remaining) - 1)
    assert client.last_response.x_rate_limit_reset == reset


def test_mock_post() -> None:
    data = json.dumps({"test": "mock"}).encode()
    client = Http()
    resp = MagicMock(status=200, data=data)
    with patch.object(client.http, "request", MagicMock(return_value=resp)) as post:
        result = client.post("mockurl", {"payload": "test"}, {"header": "test"})
        post.assert_called_once_with(
            "POST",
            "mockurl",
            body='{"payload": "test"}',
            headers={"header": "test"},
        )
        assert result == {"test": "mock"}
