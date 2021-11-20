from datetime import datetime
from typing import NamedTuple

import pytest
import vcr
from twitterapiv2.exceptions import InvalidResponseError
from twitterapiv2.exceptions import ThrottledError
from twitterapiv2.http import Http
from urllib3 import PoolManager


api_recorder = vcr.VCR(
    filter_headers=["Authorization"],
    record_mode="ONCE",
    cassette_library_dir="tests/cassettes/http",
)


class MockReponse(NamedTuple):
    status: int
    data: bytes


def test_default_values() -> None:
    client = Http()

    assert client.limit_remaining == -1
    assert client.limit_reset < datetime.now()
    assert isinstance(client.http, PoolManager)


def test_data2dict() -> None:
    client = Http()
    good_data = b'{"test": "value"}'
    bad_data = b"error data"
    assert client._data2dict(good_data) == {"test": "value"}
    assert client._data2dict(bad_data) == {"error": bad_data}


def test_response_handling_429() -> None:
    mock_resp = MockReponse(429, b"")
    client = Http()
    with pytest.raises(ThrottledError):
        client._raise_on_response(mock_resp, "")


def test_response_handling_401() -> None:
    mock_resp = MockReponse(401, b"")
    client = Http()
    with pytest.raises(InvalidResponseError):
        client._raise_on_response(mock_resp, "")


def test_response_handing_200() -> None:
    mock_resp = MockReponse(200, b"")
    client = Http()
    client._raise_on_response(mock_resp, "")


@api_recorder.use_cassette()
def test_last_response_headers() -> None:
    client = Http()
    fields = {"max_results": 10, "query": "test"}
    remaining = client.limit_remaining
    reset = client.limit_reset
    client.get("https://api.twitter.com/2/tweets/search/recent", fields)
    assert client.limit_remaining > remaining
    assert client.limit_reset != reset

    remaining = client.limit_remaining
    reset = client.limit_reset
    client.get("https://api.twitter.com/2/tweets/search/recent", fields)
    assert client.limit_remaining == remaining - 1
    assert client.limit_reset == reset
