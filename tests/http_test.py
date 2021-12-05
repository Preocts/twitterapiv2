import json
from unittest.mock import MagicMock
from unittest.mock import patch

from twitterapiv2.http import Http


# api_recorder = vcr.VCR(
#     filter_headers=["Authorization"],
#     record_mode="ONCE",
#     cassette_library_dir="tests/cassettes/http",
# )


# @api_recorder.use_cassette()
# def test_last_response_headers() -> None:
#     client = Http()
#     fields = {"max_results": 10, "query": "test"}

#     client.get("https://api.twitter.com/2/tweets/search/recent", fields)
#     assert client.last_response
#     assert client.last_response.x_rate_limit_remaining
#     assert client.last_response.x_rate_limit_reset

#     remaining = client.last_response.x_rate_limit_remaining
#     reset = client.last_response.x_rate_limit_reset
#     client.get("https://api.twitter.com/2/tweets/search/recent", fields)
#     assert client.last_response
#     assert client.last_response.x_rate_limit_remaining == str(int(remaining) - 1)
#     assert client.last_response.x_rate_limit_reset == reset


def test_mock_get() -> None:
    data = json.dumps({"test": "mock"}).encode()
    client = Http()
    resp = MagicMock(status=200, data=data)
    with patch.object(client.http, "request", MagicMock(return_value=resp)) as post:
        result = client.get("mockurl", {"payload": "test"}, {"header": "test"})
        post.assert_called_once_with(
            method="GET",
            url="mockurl",
            fields={"payload": "test"},
            headers={"header": "test"},
        )
        assert result.json == {"test": "mock"}


def test_mock_post() -> None:
    data = json.dumps({"test": "mock"}).encode()
    client = Http()
    resp = MagicMock(status=200, data=data)
    with patch.object(client.http, "request", MagicMock(return_value=resp)) as post:
        result = client.post("mockurl", {"payload": "test"}, {"header": "test"})
        post.assert_called_once_with(
            method="POST",
            url="mockurl",
            body='{"payload": "test"}',
            headers={"header": "test"},
        )
        assert result.json == {"test": "mock"}
