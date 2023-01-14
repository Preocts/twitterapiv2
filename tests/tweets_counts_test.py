from __future__ import annotations

import json
from collections.abc import Generator
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest
from twitterapiv2.tweets_counts import TweetsCounts
from twitterapiv2.tweets_counts import URL_RECENT

from tests.fixtures.clientmocker import ClientMocker
from tests.fixtures.mock_headers import HEADERS

MOCK_BODY = {
    "data": [
        {
            "end": "2021-11-14T22:00:00.000Z",
            "start": "2021-11-14T21:33:18.000Z",
            "tweet_count": 6072,
        },
        {
            "end": "2021-11-14T23:00:00.000Z",
            "start": "2021-11-14T22:00:00.000Z",
            "tweet_count": 13189,
        },
    ],
    "meta": {"total_tweet_count": 3220041},
}


@pytest.fixture
def client() -> Generator[TweetsCounts, None, None]:
    tweetclient = TweetsCounts(MagicMock())
    with patch.object(tweetclient, "http", ClientMocker()):
        yield tweetclient


def test_valid_count(client: TweetsCounts) -> None:
    client.http.add_response(json.dumps(MOCK_BODY), HEADERS, 200, URL_RECENT)

    client.query("hello")

    result = client.fetch()
    assert result["meta"]["total_tweet_count"]
    assert not client.more


def test_query_field_is_required() -> None:
    client = TweetsCounts(MagicMock())
    with pytest.raises(ValueError):
        client.fetch()
